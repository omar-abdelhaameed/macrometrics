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

def normalize_arabic_search(text: str) -> str:
    """Normalize Arabic text for search: أ/إ/ا -> ا, ة -> ه"""
    if not text:
        return text
    text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
    text = text.replace('ة', 'ه')
    return text


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
    - 0-latency PostgreSQL search through ALL local foods (Golden + Egyptian + USDA + User).
    - Arabic text normalization for better matching.
    - Graceful fallback to USDA API for long-tail items.
    """
    try:
        from sqlalchemy import or_, desc, func
        
        if lang == "auto":
            lang = "ar" if is_arabic(query) else "en"
        
        # Normalize Arabic search query
        normalized_query = normalize_arabic_search(query) if lang == "ar" else query
        search_term = f"%{query}%"
        normalized_term = f"%{normalized_query}%"
        
        # 1) Search ALL foods in database (not just golden)
        # Include: name, name_ar, and handle Arabic normalization
        all_hits = db.query(Ingredient).filter(
            or_(
                func.lower(Ingredient.name).ilike(search_term.lower()),
                func.lower(Ingredient.name_ar).ilike(search_term.lower()),
                func.lower(Ingredient.name).ilike(normalized_term.lower()),
                func.lower(Ingredient.name_ar).ilike(normalized_term.lower()),
                func.lower(Ingredient.name_ar).ilike(normalized_query.lower() + "%")
            )
        ).order_by(desc(Ingredient.popularity_score)).limit(max_results).all()
        
        # Separate golden/priority foods from regular
        golden_hits = [h for h in all_hits if h.is_golden]
        regular_hits = [h for h in all_hits if not h.is_golden]
        
        # Format all results
        results = []
        
        # First add golden/priority foods
        for g in golden_hits:
            results.append({
                "fdc_id": g.fdc_id,
                "name": f"{g.name_ar} - {g.name}" if g.name_ar else g.name,
                "category": g.category,
                "calories_per_100g": g.calories_per_100g or 0,
                "protein_per_100g": g.protein_per_100g or 0,
                "carbs_per_100g": g.carbs_per_100g or 0,
                "fats_per_100g": g.fats_per_100g or 0,
                "source": g.source or "Local",
                "is_priority": True
            })
        
        # Then add regular foods (Egyptian, USDA, user-saved)
        for r in regular_hits:
            results.append({
                "fdc_id": r.fdc_id,
                "name": f"{r.name_ar} - {r.name}" if r.name_ar else r.name,
                "category": r.category,
                "calories_per_100g": r.calories_per_100g or 0,
                "protein_per_100g": r.protein_per_100g or 0,
                "carbs_per_100g": r.carbs_per_100g or 0,
                "fats_per_100g": r.fats_per_100g or 0,
                "source": r.source or "Local",
                "is_priority": False
            })
            
        # 2) Commercial Fallback mechanism (Hit USDA API only if sparse results)
        if len(results) < max_results:
            usda_results = await search_foods(normalized_query, page_size=max_results)
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
            "normalized_query": normalized_query,
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
