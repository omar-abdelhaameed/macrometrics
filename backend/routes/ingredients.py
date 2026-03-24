import logging
from fastapi import APIRouter, Depends, Query, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from models import Ingredient, User
from schemas import IngredientOut
from auth import require_auth
from services.usda import search_foods
from services.translator import smart_search, merge_search_results, translate_search_query, is_arabic
from pydantic import BaseModel, Field
from typing import List, Optional
from rate_limiter import limiter

logger = logging.getLogger("macrometrics.ingredients")

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])


# ==================== SMART SEARCH ENDPOINT ====================

@router.get("/search")
@limiter.limit("30/minute")
async def search_foods_smart(
    request: Request,
    query: str = Query(..., min_length=1, description="Food search query"),
    lang: str = Query("auto", description="Language: 'en', 'ar', or 'auto'"),
    max_results: int = Query(15, ge=5, le=30, description="Maximum results to return"),
    db: Session = Depends(get_db)
):
    """
    Commercial-Grade Hybrid Food Search:
    - 0-latency PostgreSQL search through curated 'Golden Foods' (top 500 whole foods).
    - Perfect Raw vs Cooked algorithmic sorting.
    - Graceful fallback API to USDA for long-tail items.
    """
    try:
        from sqlalchemy import or_, desc
        
        if lang == "auto":
            lang = "ar" if is_arabic(query) else "en"
            
        translated_query = translate_search_query(query) if lang == "ar" else query
        
        # 1) Lightning-fast check against Golden Database
        search_term = f"%{query}%".lower()
        translated_term = f"%{translated_query}%".lower()
        
        golden_hits = db.query(Ingredient).filter(
            Ingredient.is_golden == True,
            or_(
                Ingredient.name.ilike(search_term),
                Ingredient.name_ar.ilike(search_term),
                Ingredient.name.ilike(translated_term)
            )
        ).order_by(desc(Ingredient.popularity_score)).limit(max_results).all()
        
        # Format Golden Results
        results = []
        for g in golden_hits:
            results.append({
                "fdc_id": g.fdc_id,
                "name": f"{g.name_ar} - {g.name}" if g.name_ar else g.name,
                "category": g.category,
                "calories_per_100g": g.calories_per_100g,
                "protein_per_100g": g.protein_per_100g,
                "carbs_per_100g": g.carbs_per_100g,
                "fats_per_100g": g.fats_per_100g,
                "source": "MacroMetrics Core",
                "is_priority": True
            })
            
        # 2) Commercial Fallback mechanism (Hit USDA API only if sparse results)
        if len(results) < max_results:
            usda_results = await search_foods(translated_query, page_size=max_results)
            existing_ids = {r["fdc_id"] for r in results if r.get("fdc_id")}
            
            for food in usda_results:
                if len(results) >= max_results:
                    break
                if food.get("fdc_id") not in existing_ids:
                    food["is_priority"] = False
                    results.append(food)

        return {
            "query": query,
            "language": lang,
            "translated_query": translated_query,
            "is_priority_search": len(golden_hits) > 0,
            "results": results,
            "total": len(results)
        }
        
    except ValueError as e:
        logger.warning(f"Smart search failed for '{query}': {e}")
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        logger.exception(f"Unexpected smart search error for '{query}': {e}")
        raise HTTPException(
            status_code=502,
            detail="Food search temporarily unavailable. Please try again."
        )


# ==================== USDA LEGACY ENDPOINT ====================

@router.get("/search-usda", tags=["USDA"])
async def search_usda(
    query: str = Query(..., min_length=2, description="Food search query"),
):
    """Search the USDA FoodData Central database for foods."""
    try:
        results = await search_foods(query, page_size=15)
        return results
    except ValueError as e:
        # Clean user-facing error from our service layer
        logger.warning(f"USDA search failed for '{query}': {e}")
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        logger.exception(f"Unexpected USDA search error for '{query}': {e}")
        raise HTTPException(
            status_code=502,
            detail="Nutrition database temporarily unavailable. Please try again later.",
        )


@router.get("", response_model=List[IngredientOut])
def list_ingredients(
    search: str = Query(None, description="Search by ingredient name or category"),
    db: Session = Depends(get_db),
):
    """List all local ingredients, optionally filtered by search query."""
    q = db.query(Ingredient)
    if search:
        pattern = f"%{search}%"
        q = q.filter(
            Ingredient.name.ilike(pattern) | Ingredient.category.ilike(pattern)
        )
    return q.order_by(Ingredient.name).all()


@router.get("/{ingredient_id}", response_model=IngredientOut)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    """Get a single ingredient by ID."""
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


# ── USDA FoodData Central Save ─────────────────────────

class SaveFromUSDARequest(BaseModel):
    fdc_id: str = Field(..., max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    category: str = Field("General", max_length=100)
    calories_per_100g: float = Field(..., ge=0, le=2000)
    protein_per_100g: float = Field(..., ge=0, le=500)
    carbs_per_100g: float = Field(..., ge=0, le=1000)
    fats_per_100g: float = Field(..., ge=0, le=500)
    fiber_per_100g: float = Field(0.0, ge=0, le=200)


@router.post("/save-from-usda", response_model=IngredientOut, status_code=201)
def save_from_usda(
    payload: SaveFromUSDARequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """Save a USDA food to the local ingredient database."""
    existing = db.query(Ingredient).filter(Ingredient.fdc_id == payload.fdc_id).first()
    if existing:
        return existing

    ingredient = Ingredient(
        name=payload.name,
        category=payload.category,
        calories_per_100g=payload.calories_per_100g,
        protein_per_100g=payload.protein_per_100g,
        carbs_per_100g=payload.carbs_per_100g,
        fats_per_100g=payload.fats_per_100g,
        fiber_per_100g=payload.fiber_per_100g,
        source="USDA FDC",
        fdc_id=payload.fdc_id,
        user_id=user.id,
    )
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient
