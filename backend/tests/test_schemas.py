import pytest
from pydantic import BaseModel, Field, ValidationError
from typing import Literal, Optional, List


class MealIngredientIn(BaseModel):
    ingredient_id: int = Field(..., gt=0)
    serving_size_g: float = Field(100.0, gt=0, le=5000)


class MealIn(BaseModel):
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    meal_type: Literal["breakfast", "lunch", "dinner", "snack"] = "lunch"
    ingredients: List[MealIngredientIn] = Field(..., min_length=1, max_length=50)


class DailyLogPatch(BaseModel):
    is_refeed_day: Optional[bool] = None
    is_rest_day: Optional[bool] = None
    notes: Optional[str] = Field(None, max_length=1000)
    calorie_target_override: Optional[int] = Field(None, ge=500, le=10000)
    weight_lbs: Optional[float] = Field(None, ge=30, le=700)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=10, le=120)
    gender: Optional[Literal["male", "female", "other"]] = None
    activity_level: Optional[Literal["sedentary", "light", "moderate", "active", "very_active"]] = None
    primary_goal: Optional[Literal["cut", "maintain", "bulk"]] = None
    preferred_unit: Optional[Literal["metric", "imperial"]] = None
    current_weight_lbs: Optional[float] = Field(None, ge=30, le=700)


class TestMealIn:
    def test_valid_meal(self):
        meal = MealIn(
            date="2024-01-15",
            meal_type="lunch",
            ingredients=[{"ingredient_id": 1, "serving_size_g": 100.0}]
        )
        assert meal.date == "2024-01-15"
        assert meal.meal_type == "lunch"

    def test_invalid_date_format(self):
        with pytest.raises(ValidationError):
            MealIn(
                date="15-01-2024",
                meal_type="lunch",
                ingredients=[{"ingredient_id": 1, "serving_size_g": 100.0}]
            )

    def test_invalid_meal_type(self):
        with pytest.raises(ValidationError):
            MealIn(
                date="2024-01-15",
                meal_type="invalid",
                ingredients=[{"ingredient_id": 1, "serving_size_g": 100.0}]
            )

    def test_empty_ingredients(self):
        with pytest.raises(ValidationError):
            MealIn(
                date="2024-01-15",
                meal_type="lunch",
                ingredients=[]
            )


class TestDailyLogPatch:
    def test_valid_patch(self):
        patch = DailyLogPatch(
            is_refeed_day=True,
            notes="Feeling good",
            weight_lbs=180.5
        )
        assert patch.is_refeed_day is True
        assert patch.weight_lbs == 180.5

    def test_notes_too_long(self):
        with pytest.raises(ValidationError):
            DailyLogPatch(notes="x" * 1001)

    def test_calorie_override_bounds(self):
        with pytest.raises(ValidationError):
            DailyLogPatch(calorie_target_override=100)

        with pytest.raises(ValidationError):
            DailyLogPatch(calorie_target_override=20000)


class TestUserUpdate:
    def test_valid_update(self):
        update = UserUpdate(
            name="Updated Name",
            age=30,
            activity_level="active",
            primary_goal="cut"
        )
        assert update.name == "Updated Name"
        assert update.age == 30

    def test_invalid_activity_level(self):
        with pytest.raises(ValidationError):
            UserUpdate(activity_level="invalid")

    def test_weight_bounds(self):
        with pytest.raises(ValidationError):
            UserUpdate(current_weight_lbs=10)

        with pytest.raises(ValidationError):
            UserUpdate(current_weight_lbs=1000)
