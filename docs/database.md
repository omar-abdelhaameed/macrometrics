# Database Architecture

MacroMetrics uses PostgreSQL as its primary datastore, managed via SQLAlchemy ORM and Alembic migrations.

## ERD Overview
The core entities revolve around the `User`, their `DailyLog`, the `Meal`s recorded on those logs, and the `Ingredient`s that make up those meals.

---

## Models

### 1. User
Stores authentication details, demographics, bodybuilding tracking configurations, and app preferences.
- **id**: Primary Key (`Integer`)
- **name**: `String(100)`
- **email**: `String(255)`, unique
- **password_hash**: `String(255)`
- **Demographics**: `age` (`Integer`), `gender` (`String`)
- **Daily Targets**: `daily_calorie_target`, `protein_target_g`, `carbs_target_g`, `fats_target_g` 
- **Tracking/Goals**: 
  - `current_weight_lbs`, `goal_weight_lbs` (`Float`)
  - `height_cm` (`Float`)
  - `body_fat_pct` (`Float`)
  - `activity_level` (`String`) (e.g., sedentary, moderate, active)
  - `primary_goal` (`String`) (cut, maintain, bulk)
- **Preferences**:
  - `preferred_unit` (`String`: metric, imperial)
  - `theme_mode` (`String`: dark, light)
  - `theme_accent` (`String`: green, blue, orange, purple)
- **Relationships**: One-to-Many with `DailyLog`.

### 2. DailyLog
Represents a single day of tracking for a specific user.
- **id**: Primary Key (`Integer`)
- **user_id**: Foreign Key to `users.id`
- **date**: Date of the log (`Date`)
- **weight_lbs**: Logged weight for the day (`Float`)
- **Flags**: `is_refeed_day`, `is_rest_day` (`Boolean`)
- **Overrides**: Optional manual targets for a specific day (`calorie_target_override`, etc.)
- **Relationships**: One-to-Many with `Meal`.

### 3. Meal
Represents a meal event within a `DailyLog`.
- **id**: Primary Key (`Integer`)
- **daily_log_id**: Foreign Key to `daily_logs.id`
- **meal_type**: e.g., "breakfast", "lunch", "dinner", "snack" (`String(50)`)
- **time_logged**: Timestamp of the entry (`DateTime`)
- **Relationships**: One-to-Many with `MealIngredient`.

### 4. Ingredient
Stores nutritional macro data for a food item. Can be sourced from the USDA Database or created as a custom entry by a user.
- **id**: Primary Key (`Integer`)
- **name**: `String(200)`
- **category**: `String(100)`
- **Macros per 100g**:
  - `calories_per_100g`, `protein_per_100g`, `carbs_per_100g`, `fats_per_100g` (`Float`)
  - `fiber_per_100g`, `sugar_per_100g`, `sodium_mg_per_100g` (`Float`, defaults to 0)
- **Metadata**: 
  - `source` (`String`, default="USDA")
  - `fdc_id` (USDA FoodData Central ID)
  - `serving_description`
  - `user_id`: Foreign Key to `users.id` (if it's a user's custom food)
- **Relationships**: One-to-Many with `MealIngredient`.

### 5. MealIngredient (Join Table)
Associates an `Ingredient` with a `Meal` and tracks the specific serving size consumed.
- **id**: Primary Key (`Integer`)
- **meal_id**: Foreign Key to `meals.id`
- **ingredient_id**: Foreign Key to `ingredients.id`
- **serving_size_g**: The actual amount logged (`Float`, default 100.0)

---

## Seed Strategy
The `backend/seed.py` file resets the schema entirely and provisions default users with predefined metrics, a historical dataset spanning 30+ days of `DailyLog`s to populate charts, and a selection of default `Ingredient` entries for testing without hitting the USDA API.
