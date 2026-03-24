# Automatic Nutrition Calculation Engine & UI Refinements

## Goal
Implement a backend engine to calculate auto-assigned daily macro targets (Calories, Protein, Carbs, Fats) based on demographic inputs, activity level, and a primary goal (Cut, Maintain, Bulk). We will also refine the Registration UI (remove "Other" gender option, fix header layouts), introduce the "Primary Goal" field, and restructure the Meal Logger to prioritize USDA search as the primary "Food Search".

## User Review Required
None right now. The mathematical approach directly reflects the instructions (Mifflin-St Jeor + strict multiplier rules + bodybuilder macro parsing).

## Proposed Changes

### Database Layer
#### [MODIFY] [backend/models.py](file:///C:/Users/afsao/Desktop/new%20project/backend/models.py)
- Add `primary_goal` column (`String(50)`, default="maintain") to [User](file:///C:/Users/afsao/Desktop/new%20project/backend/models.py#19-48) model.

#### [MODIFY] [backend/schemas.py](file:///C:/Users/afsao/Desktop/new%20project/backend/schemas.py)
- Add `primary_goal` to [UserOut](file:///C:/Users/afsao/Desktop/new%20project/backend/schemas.py#88-109) and [UserUpdate](file:///C:/Users/afsao/Desktop/new%20project/backend/schemas.py#111-128).

---

### Backend Logic
#### [NEW] `backend/services/nutrition.py`
Create a new service with the following functions:
- `calculate_bmr(weight_kg, height_cm, age, gender)`: Implements Mifflin-St Jeor equation.
- `calculate_tdee(bmr, activity_level)`: Multiplies BMR by activity coefficient.
- `calculate_macros(weight_kg, height_cm, age, gender, activity_level, primary_goal)`: Returns a dictionary with `daily_calorie_target`, `protein_target_g`, `carbs_target_g`, and `fats_target_g`.

#### [MODIFY] [backend/routes/auth.py](file:///C:/Users/afsao/Desktop/new%20project/backend/routes/auth.py)
- Update [RegisterRequest](file:///C:/Users/afsao/Desktop/new%20project/backend/routes/auth.py#12-29) to include `primary_goal`.
- Call `calculate_macros` during registration and populate the `_target_g` fields automatically.

#### [MODIFY] [backend/routes/users.py](file:///C:/Users/afsao/Desktop/new%20project/backend/routes/users.py)
- Update `PUT /users/me` so that if any core stat changes (`current_weight_lbs`, `height_cm`, `age`, `gender`, `activity_level`, or `primary_goal`), the server automatically recalculates and updates the macro targets on the user profile.

#### [MODIFY] [backend/seed.py](file:///C:/Users/afsao/Desktop/new%20project/backend/seed.py)
- Update the default seeded user (20yo male, 80kg, 180cm, moderately active, Bulking) and explicitly run the stats through `services/nutrition.py` to seed realistic macros.

---

### Frontend UI
#### [MODIFY] [frontend/src/pages/Register.jsx](file:///C:/Users/afsao/Desktop/new%20project/frontend/src/pages/Register.jsx)
- Replace 3-option Gender pill with 2-option (Male/Female).
- Fix header alignments for "Body Stats" and "Targets".
- Auto-calculate macros on the frontend for step 3 to give them a preview (or just let the backend handle it and remove the manual target inputs from registration Step 3).
- **Design decision**: Step 3 will just ask for `primary_goal` instead of manual targets.

#### [MODIFY] [frontend/src/pages/Profile.jsx](file:///C:/Users/afsao/Desktop/new%20project/frontend/src/pages/Profile.jsx)
- Add UI to display and change `primary_goal`.

#### [MODIFY] [frontend/src/pages/MealLogger.jsx](file:///C:/Users/afsao/Desktop/new%20project/frontend/src/pages/MealLogger.jsx)
- Default `searchMode` to [usda](file:///C:/Users/afsao/Desktop/new%20project/backend/routes/ingredients.py#17-35).
- Rename USDA toggle button to "Food Search".
- Rename Local toggle button to "Saved Foods" or "Frequent Foods".
