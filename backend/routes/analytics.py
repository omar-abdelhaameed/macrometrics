from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from database import get_db
from models import DailyLog, Meal, MealIngredient, Ingredient, User
from auth import require_auth
from datetime import date, timedelta

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
def analytics_summary(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """Aggregate stats: avg daily calories, weight change, logging streak."""
    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    logs = db.query(DailyLog).options(
        joinedload(DailyLog.meals)
        .joinedload(Meal.meal_ingredients)
        .joinedload(MealIngredient.ingredient)
    ).filter(
        DailyLog.user_id == user.id,
        DailyLog.date >= start_date,
        DailyLog.date <= end_date,
    ).order_by(DailyLog.date).all()

    if not logs:
        return {
            "avg_daily_calories": 0,
            "total_weight_change": 0,
            "streak": 0,
            "logged_days": 0,
            "period_days": days,
        }

    daily_cals = []
    for log in logs:
        total = 0
        for meal in log.meals:
            for mi in meal.meal_ingredients:
                total += mi.ingredient.calories_per_100g * mi.serving_size_g / 100
        daily_cals.append(total)

    avg_cal = round(sum(daily_cals) / len(daily_cals), 0) if daily_cals else 0

    weights = [log.weight_lbs for log in logs if log.weight_lbs]
    weight_change = round(weights[-1] - weights[0], 1) if len(weights) >= 2 else 0

    streak = 0
    check_date = end_date
    log_dates = {log.date for log in logs if log.meals}
    while check_date in log_dates:
        streak += 1
        check_date -= timedelta(days=1)

    return {
        "avg_daily_calories": avg_cal,
        "total_weight_change": weight_change,
        "streak": streak,
        "logged_days": len(logs),
        "period_days": days,
    }


@router.get("/weight-trend")
def weight_trend(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """Daily weight + calorie data for charting."""
    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    logs = db.query(DailyLog).options(
        joinedload(DailyLog.meals)
        .joinedload(Meal.meal_ingredients)
        .joinedload(MealIngredient.ingredient)
    ).filter(
        DailyLog.user_id == user.id,
        DailyLog.date >= start_date,
    ).order_by(DailyLog.date).all()

    results = []
    for log in logs:
        cal_total = 0
        for meal in log.meals:
            for mi in meal.meal_ingredients:
                cal_total += mi.ingredient.calories_per_100g * mi.serving_size_g / 100
        results.append({
            "date": log.date.isoformat(),
            "weight": log.weight_lbs,
            "calories": round(cal_total, 0),
        })

    return results


@router.get("/macro-composition")
def macro_composition(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """Macro percentage breakdown over period."""
    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    logs = db.query(DailyLog).options(
        joinedload(DailyLog.meals)
        .joinedload(Meal.meal_ingredients)
        .joinedload(MealIngredient.ingredient)
    ).filter(
        DailyLog.user_id == user.id,
        DailyLog.date >= start_date,
    ).all()

    total_p = total_c = total_f = 0.0
    for log in logs:
        for meal in log.meals:
            for mi in meal.meal_ingredients:
                factor = mi.serving_size_g / 100
                total_p += mi.ingredient.protein_per_100g * factor
                total_c += mi.ingredient.carbs_per_100g * factor
                total_f += mi.ingredient.fats_per_100g * factor

    total = total_p + total_c + total_f
    if total == 0:
        return [
            {"name": "Protein", "value": 33},
            {"name": "Carbs", "value": 34},
            {"name": "Fats", "value": 33},
        ]

    return [
        {"name": "Protein", "value": round(total_p / total * 100)},
        {"name": "Carbs", "value": round(total_c / total * 100)},
        {"name": "Fats", "value": round(total_f / total * 100)},
    ]


@router.get("/weight-plateau")
def check_weight_plateau(
    days: int = Query(7, ge=3, le=30),
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """
    Detect weight plateaus - returns plateau detection and refeed suggestions.
    Checks if weight has been stagnant for specified days (default 7).
    """
    today = date.today()
    start_date = today - timedelta(days=days)
    
    logs = db.query(DailyLog).filter(
        DailyLog.user_id == user.id,
        DailyLog.date >= start_date,
        DailyLog.date <= today,
        DailyLog.weight_lbs.isnot(None)
    ).order_by(DailyLog.date.desc()).all()
    
    if len(logs) < 3:
        return {
            "is_plateau": False,
            "days_stagnant": 0,
            "current_weight": logs[0].weight_lbs if logs else None,
            "suggestion": None
        }
    
    weights = [log.weight_lbs for log in logs if log.weight_lbs]
    if not weights:
        return {"is_plateau": False, "days_stagnant": 0, "current_weight": None, "suggestion": None}
    
    weight_variance = max(weights) - min(weights)
    current_weight = weights[0]
    
    is_plateau = weight_variance < 0.5
    
    if is_plateau:
        if user.primary_goal == "cut":
            suggestion = (
                f"Weight plateau detected after {days} days. "
                "Consider a refeed day: increase calories by 20-30% (focus on carbs) "
                "for 1-2 days to reset metabolism."
            )
        elif user.primary_goal == "bulk":
            suggestion = (
                "Weight plateau detected. Consider increasing daily calories by 100-200 "
                "or adding an extra meal."
            )
        else:
            suggestion = (
                "Weight plateau detected. Consider varying your macros or activity level."
            )
        
        return {
            "is_plateau": True,
            "days_stagnant": days,
            "current_weight": current_weight,
            "suggestion": suggestion,
            "refeed_recommendation": {
                "calorie_increase": "20-30%",
                "focus_nutrient": "carbs",
                "duration": "1-2 days",
                "target_calories": int(user.daily_calorie_target * 1.25)
            }
        }
    
    return {"is_plateau": False, "days_stagnant": 0, "current_weight": current_weight, "suggestion": None}
