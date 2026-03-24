from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import DailyLog, Meal, MealIngredient, User
from schemas import DailySummary, DailyLogPatch, MealOut, MealIngredientOut
from auth import require_auth
from datetime import date as date_type

router = APIRouter(tags=["Daily"])


def _compute_summary(daily_log: DailyLog, user: User) -> dict:
    """Compute total consumed and remaining macros for a daily log."""
    total_cal = total_p = total_c = total_f = 0.0
    meals_out = []

    for meal in daily_log.meals:
        meal_cal = meal_p = meal_c = meal_f = 0.0
        ings_out = []

        for mi in meal.meal_ingredients:
            ing = mi.ingredient
            factor = mi.serving_size_g / 100.0
            cal = round(ing.calories_per_100g * factor, 1)
            p = round(ing.protein_per_100g * factor, 1)
            c = round(ing.carbs_per_100g * factor, 1)
            f = round(ing.fats_per_100g * factor, 1)

            meal_cal += cal
            meal_p += p
            meal_c += c
            meal_f += f

            ings_out.append(MealIngredientOut(
                ingredient_id=ing.id,
                ingredient_name=ing.name,
                serving_size_g=mi.serving_size_g,
                calories=cal, protein=p, carbs=c, fats=f,
            ))

        total_cal += meal_cal
        total_p += meal_p
        total_c += meal_c
        total_f += meal_f

        meals_out.append(MealOut(
            id=meal.id,
            meal_type=meal.meal_type,
            time_logged=meal.time_logged,
            ingredients=ings_out,
            total_calories=round(meal_cal, 1),
            total_protein=round(meal_p, 1),
            total_carbs=round(meal_c, 1),
            total_fats=round(meal_f, 1),
        ))

    cal_target = daily_log.calorie_target_override or user.daily_calorie_target
    p_target = daily_log.protein_target_override or user.protein_target_g
    c_target = daily_log.carbs_target_override or user.carbs_target_g
    f_target = daily_log.fats_target_override or user.fats_target_g

    return {
        "date": daily_log.date.isoformat(),
        "calories_consumed": round(total_cal, 1),
        "calories_target": cal_target,
        "calories_remaining": round(cal_target - total_cal, 1),
        "protein_consumed": round(total_p, 1),
        "protein_target": p_target,
        "protein_remaining": round(p_target - total_p, 1),
        "carbs_consumed": round(total_c, 1),
        "carbs_target": c_target,
        "carbs_remaining": round(c_target - total_c, 1),
        "fats_consumed": round(total_f, 1),
        "fats_target": f_target,
        "fats_remaining": round(f_target - total_f, 1),
        "is_refeed_day": daily_log.is_refeed_day,
        "meals": meals_out,
    }


@router.get("/daily-summary", response_model=DailySummary)
def get_daily_summary(
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """Get a comprehensive daily macro summary with all meals."""
    try:
        log_date = date_type.fromisoformat(date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    daily_log = db.query(DailyLog).options(
        joinedload(DailyLog.meals)
        .joinedload(Meal.meal_ingredients)
        .joinedload(MealIngredient.ingredient)
    ).filter(
        DailyLog.user_id == user.id,
        DailyLog.date == log_date,
    ).first()

    if not daily_log:
        return DailySummary(
            date=date,
            calories_consumed=0, calories_target=user.daily_calorie_target,
            calories_remaining=user.daily_calorie_target,
            protein_consumed=0, protein_target=user.protein_target_g,
            protein_remaining=user.protein_target_g,
            carbs_consumed=0, carbs_target=user.carbs_target_g,
            carbs_remaining=user.carbs_target_g,
            fats_consumed=0, fats_target=user.fats_target_g,
            fats_remaining=user.fats_target_g,
            is_refeed_day=False,
            meals=[],
        )

    return _compute_summary(daily_log, user)


@router.patch("/daily-log/{log_id}/toggle-refeed")
def toggle_refeed(
    log_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """Toggle the refeed day flag on a daily log."""
    daily_log = db.query(DailyLog).filter(
        DailyLog.id == log_id,
        DailyLog.user_id == user.id,
    ).first()
    if not daily_log:
        raise HTTPException(status_code=404, detail="Daily log not found")
    daily_log.is_refeed_day = not daily_log.is_refeed_day
    db.commit()
    return {"id": daily_log.id, "is_refeed_day": daily_log.is_refeed_day}
