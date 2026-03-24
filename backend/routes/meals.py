from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Meal, MealIngredient, DailyLog, Ingredient, User
from schemas import MealIn, MealOut, MealIngredientOut
from auth import require_auth
from typing import List
from datetime import date as date_type, datetime

router = APIRouter(prefix="/meals", tags=["Meals"])


def _build_meal_out(meal: Meal) -> dict:
    """Convert a Meal ORM object to MealOut-compatible dict."""
    ingredients_out = []
    total_cal = total_p = total_c = total_f = 0.0

    for mi in meal.meal_ingredients:
        ing = mi.ingredient
        factor = mi.serving_size_g / 100.0
        cal = round(ing.calories_per_100g * factor, 1)
        p = round(ing.protein_per_100g * factor, 1)
        c = round(ing.carbs_per_100g * factor, 1)
        f = round(ing.fats_per_100g * factor, 1)

        total_cal += cal
        total_p += p
        total_c += c
        total_f += f

        ingredients_out.append(MealIngredientOut(
            ingredient_id=ing.id,
            ingredient_name=ing.name,
            serving_size_g=mi.serving_size_g,
            calories=cal,
            protein=p,
            carbs=c,
            fats=f,
        ))

    return {
        "id": meal.id,
        "meal_type": meal.meal_type,
        "time_logged": meal.time_logged,
        "ingredients": ingredients_out,
        "total_calories": round(total_cal, 1),
        "total_protein": round(total_p, 1),
        "total_carbs": round(total_c, 1),
        "total_fats": round(total_f, 1),
    }


@router.post("", response_model=MealOut)
def log_meal(
    payload: MealIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """Log a new meal with ingredients and serving sizes."""
    try:
        log_date = date_type.fromisoformat(payload.date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, use YYYY-MM-DD")

    # Get or create daily log
    daily_log = db.query(DailyLog).filter(
        DailyLog.user_id == user.id,
        DailyLog.date == log_date,
    ).first()

    if not daily_log:
        daily_log = DailyLog(user_id=user.id, date=log_date)
        db.add(daily_log)
        db.flush()

    # Create meal
    meal = Meal(
        daily_log_id=daily_log.id,
        meal_type=payload.meal_type,
        time_logged=datetime.utcnow(),
    )
    db.add(meal)
    db.flush()

    # Add ingredients
    for item in payload.ingredients:
        ingredient = db.query(Ingredient).filter(Ingredient.id == item.ingredient_id).first()
        if not ingredient:
            raise HTTPException(
                status_code=404,
                detail=f"Ingredient ID {item.ingredient_id} not found"
            )
        mi = MealIngredient(
            meal_id=meal.id,
            ingredient_id=item.ingredient_id,
            serving_size_g=item.serving_size_g,
        )
        db.add(mi)

    db.commit()
    db.refresh(meal)

    # Re-query with joins
    meal = db.query(Meal).options(
        joinedload(Meal.meal_ingredients).joinedload(MealIngredient.ingredient)
    ).filter(Meal.id == meal.id).first()

    return _build_meal_out(meal)


@router.get("", response_model=List[MealOut])
def list_meals(
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """List all meals for a given date."""
    try:
        log_date = date_type.fromisoformat(date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    daily_log = db.query(DailyLog).filter(
        DailyLog.user_id == user.id,
        DailyLog.date == log_date,
    ).first()

    if not daily_log:
        return []

    meals = db.query(Meal).options(
        joinedload(Meal.meal_ingredients).joinedload(MealIngredient.ingredient)
    ).filter(Meal.daily_log_id == daily_log.id).order_by(Meal.time_logged).all()

    return [_build_meal_out(m) for m in meals]
