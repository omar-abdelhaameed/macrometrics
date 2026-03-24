# API Documentation

MacroMetrics features a robust, RESTful FastAPI backend. All endpoints returning personalized data require a valid JWT token passed in the `Authorization: Bearer <token>` header.

The base URL typically runs on `http://localhost:8000`.

---

## 1. Authentication (`/auth`)

### `POST /auth/register`
Creates a new user and automatically calculates their basal metabolic rate (BMR), total daily energy expenditure (TDEE), and optimal macro split based on their inputs.
- **Body**: 
  - Required: `name`, `email`, `password`.
  - Recommended for accurate macros: `age`, `gender`, `current_weight_lbs`, `height_cm`, `activity_level`, `primary_goal`.
- **Returns**: `access_token` and `user` object.

### `POST /auth/login`
Authenticates an existing user.
- **Body**: `email`, `password`.
- **Returns**: `access_token` and `user` object.

---

## 2. Users (`/users`)

### `GET /users/me` (Auth Required)
Fetches the currently authenticated user's profile and macro targets.

### `PUT /users/me` (Auth Required)
Updates the authenticated user's profile.
- **Note**: If physical metrics or goals are changed (`current_weight_lbs`, `activity_level`, `primary_goal`, etc.), the backend **automatically recalculates** and updates their macro targets.

---

## 3. Meals (`/meals`)

### `POST /meals` (Auth Required)
Logs a new meal, associating it with the current date's `DailyLog`.
- **Body**: 
  - `date` (YYYY-MM-DD): The day to log the meal on.
  - `meal_type` (e.g., "lunch").
  - `ingredients`: Array of objects containing `ingredient_id` and `serving_size_g`.

### `GET /meals?date=YYYY-MM-DD` (Auth Required)
Fetches all meals logged by the user for a specific date, including nested ingredient details and calculated totals for the serving sizes.

---

## 4. Daily Summaries (`/daily`)

### `GET /daily/daily-summary?date=YYYY-MM-DD` (Auth Required)
The core dashboard endpoint. Retrieves a comprehensive aggregation of the day's nutrition.
- **Returns**: 
  - Total consumed macro values (calories, protein, carbs, fats).
  - Target macro values.
  - Remaining macro values.
  - Nested array of all `meals` and their `ingredients`.

### `PATCH /daily/daily-log/{log_id}/toggle-refeed` (Auth Required)
Toggles the `is_refeed_day` flag on a specific log.

---

## 5. Ingredients (`/ingredients`)

### `GET /ingredients/search-usda?query={search}`
Searches the external USDA FoodData Central API for a food item.
- Note: This endpoint catches USDA timeouts/errors and returns clean 502 responses to the frontend.

### `POST /ingredients/save-from-usda` (Auth Required)
Saves a food item retrieved from the USDA API into the local database for faster future querying.

### `GET /ingredients?search={query}`
Searches locally cached and user-created ingredients.

---

## 6. Analytics (`/analytics`)
*All Analytics endpoints require Authentication and accept an optional `?days={int}` query parameter (default: 30).*

### `GET /analytics/summary`
Returns high-level statistics: `avg_daily_calories`, `total_weight_change`, `streak`, and `logged_days`.

### `GET /analytics/weight-trend`
Returns an array of specific dates with the logged `weight` and total `calories` for charting timelines.

### `GET /analytics/macro-composition`
Returns the percentage breakdown of macro consumption (Protein, Carbs, Fats) over the period, formatted perfectly for Recharts Donut charts.
