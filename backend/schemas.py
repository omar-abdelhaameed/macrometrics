from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List, Literal
from datetime import date, datetime


# ── Ingredient Schemas ─────────────────────────────────
class IngredientOut(BaseModel):
    id: int
    name: str
    category: str
    calories_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float
    fats_per_100g: float
    fiber_per_100g: float
    source: str
    fdc_id: Optional[str] = None

    class Config:
        from_attributes = True


# ── Meal Schemas ───────────────────────────────────────
class MealIngredientIn(BaseModel):
    ingredient_id: int = Field(..., gt=0)
    serving_size_g: float = Field(100.0, gt=0, le=5000)


class MealIn(BaseModel):
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    meal_type: Literal["breakfast", "lunch", "dinner", "snack"] = "lunch"
    ingredients: List[MealIngredientIn] = Field(..., min_length=1, max_length=50)


class MealIngredientOut(BaseModel):
    ingredient_id: int
    ingredient_name: str
    serving_size_g: float
    calories: float
    protein: float
    carbs: float
    fats: float


class MealOut(BaseModel):
    id: int
    meal_type: str
    time_logged: Optional[datetime] = None
    ingredients: List[MealIngredientOut]
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fats: float

    class Config:
        from_attributes = True


# ── Daily Summary Schema ──────────────────────────────
class DailySummary(BaseModel):
    date: str
    calories_consumed: float
    calories_target: int
    calories_remaining: float
    protein_consumed: float
    protein_target: float
    protein_remaining: float
    carbs_consumed: float
    carbs_target: float
    carbs_remaining: float
    fats_consumed: float
    fats_target: float
    fats_remaining: float
    is_refeed_day: bool
    meals: List[MealOut]


# ── DailyLog Patch ────────────────────────────────────
class DailyLogPatch(BaseModel):
    is_refeed_day: Optional[bool] = None
    is_rest_day: Optional[bool] = None
    notes: Optional[str] = Field(None, max_length=1000)
    calorie_target_override: Optional[int] = Field(None, ge=500, le=10000)
    weight_lbs: Optional[float] = Field(None, ge=30, le=700)


# ── User Schemas ──────────────────────────────────────
class UserOut(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    daily_calorie_target: int
    protein_target_g: float
    carbs_target_g: float
    fats_target_g: float
    goal_weight_lbs: Optional[float] = None
    current_weight_lbs: Optional[float] = None
    height_cm: Optional[float] = None
    body_fat_pct: Optional[float] = None
    activity_level: str
    primary_goal: str
    preferred_unit: str
    theme_mode: str
    theme_accent: str
    
    # SaaS
    is_pro_user: bool = False
    stripe_customer_id: Optional[str] = None
    subscription_end_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=10, le=120)
    gender: Optional[Literal["male", "female", "other"]] = None
    daily_calorie_target: Optional[int] = Field(None, ge=500, le=10000)
    protein_target_g: Optional[float] = Field(None, ge=0, le=500)
    carbs_target_g: Optional[float] = Field(None, ge=0, le=1000)
    fats_target_g: Optional[float] = Field(None, ge=0, le=500)
    goal_weight_lbs: Optional[float] = Field(None, ge=30, le=700)
    current_weight_lbs: Optional[float] = Field(None, ge=30, le=700)
    height_cm: Optional[float] = Field(None, ge=50, le=300)
    body_fat_pct: Optional[float] = Field(None, ge=1, le=60)
    activity_level: Optional[Literal["sedentary", "light", "moderate", "active", "very_active"]] = None
    primary_goal: Optional[Literal["cut", "maintain", "bulk"]] = None
    preferred_unit: Optional[Literal["metric", "imperial"]] = None
    theme_mode: Optional[Literal["light", "dark", "system"]] = None
    theme_accent: Optional[str] = Field(None, max_length=50)
    is_pro_user: Optional[bool] = None
