"""
Seed script for MacroMetrics V1.1
Creates test user "Omar" (with password) and populates USDA ingredients.
Run:  py -3 seed.py
"""
from dotenv import load_dotenv
load_dotenv()

from database import engine, SessionLocal, Base
from models import User, Ingredient
from services.nutrition import calculate_macros
from auth import hash_password

# Re-create all tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

macros = calculate_macros(
    weight_kg=80.0,
    height_cm=180.0,
    age=20,
    gender="male",
    activity_level="moderate",
    primary_goal="bulk"
)

# ── 1. Create user "Omar" ────────────────────────────────
omar = User(
    name="Omar",
    email="omar@macrometrics.app",
    password_hash=hash_password("omar123"),
    age=20,
    gender="male",
    daily_calorie_target=macros["daily_calorie_target"],
    protein_target_g=macros["protein_target_g"],
    carbs_target_g=macros["carbs_target_g"],
    fats_target_g=macros["fats_target_g"],
    current_weight_lbs=80.0 * 2.20462,  # 80kg approx 176.37 lbs
    height_cm=180.0,
    body_fat_pct=14.0,
    activity_level="moderate",
    primary_goal="bulk",
    preferred_unit="metric",
    theme_mode="dark",
    theme_accent="green",
)
db.add(omar)

# ── 2. Seed Ingredients (USDA values per 100g) ──────────
ingredients_data = [
    {"name": "Grilled Chicken Breast", "category": "Poultry", "calories_per_100g": 165, "protein_per_100g": 31.0, "carbs_per_100g": 0.0, "fats_per_100g": 3.6, "fiber_per_100g": 0.0, "source": "USDA"},
    {"name": "Large Brown Egg", "category": "Dairy/Protein", "calories_per_100g": 155, "protein_per_100g": 12.6, "carbs_per_100g": 1.1, "fats_per_100g": 10.6, "fiber_per_100g": 0.0, "source": "USDA"},
    {"name": "Whey Protein Isolate", "category": "Supplement", "calories_per_100g": 370, "protein_per_100g": 90.0, "carbs_per_100g": 2.0, "fats_per_100g": 1.0, "fiber_per_100g": 0.0, "source": "USDA"},
    {"name": "Atlantic Salmon (baked)", "category": "Seafood", "calories_per_100g": 208, "protein_per_100g": 20.4, "carbs_per_100g": 0.0, "fats_per_100g": 13.4, "fiber_per_100g": 0.0, "source": "USDA"},
    {"name": "White Basmati Rice (cooked)", "category": "Grain", "calories_per_100g": 150, "protein_per_100g": 3.5, "carbs_per_100g": 32.0, "fats_per_100g": 0.3, "fiber_per_100g": 0.4, "source": "USDA"},
    {"name": "Sweet Potato (baked)", "category": "Vegetable", "calories_per_100g": 90, "protein_per_100g": 2.0, "carbs_per_100g": 20.7, "fats_per_100g": 0.1, "fiber_per_100g": 3.3, "source": "USDA"},
    {"name": "Greek Yogurt (2%)", "category": "Dairy", "calories_per_100g": 73, "protein_per_100g": 9.9, "carbs_per_100g": 3.9, "fats_per_100g": 1.7, "fiber_per_100g": 0.0, "source": "USDA"},
    {"name": "Rolled Oats", "category": "Grain", "calories_per_100g": 379, "protein_per_100g": 13.2, "carbs_per_100g": 67.7, "fats_per_100g": 6.5, "fiber_per_100g": 10.1, "source": "USDA"},
    {"name": "Extra-Lean Ground Beef (95/5)", "category": "Red Meat", "calories_per_100g": 137, "protein_per_100g": 21.4, "carbs_per_100g": 0.0, "fats_per_100g": 5.0, "fiber_per_100g": 0.0, "source": "USDA"},
    {"name": "Avocado", "category": "Fruit", "calories_per_100g": 160, "protein_per_100g": 2.0, "carbs_per_100g": 8.5, "fats_per_100g": 14.7, "fiber_per_100g": 6.7, "source": "USDA"},
    {"name": "Cottage Cheese (1%)", "category": "Dairy", "calories_per_100g": 72, "protein_per_100g": 12.4, "carbs_per_100g": 2.7, "fats_per_100g": 1.0, "fiber_per_100g": 0.0, "source": "USDA"},
    {"name": "Broccoli (steamed)", "category": "Vegetable", "calories_per_100g": 35, "protein_per_100g": 2.4, "carbs_per_100g": 7.2, "fats_per_100g": 0.4, "fiber_per_100g": 3.3, "source": "USDA"},
]

for data in ingredients_data:
    db.add(Ingredient(**data))

db.commit()
db.close()

print(f"✅ Seeded 1 user (Omar/omar123, age:26, imperial) + {len(ingredients_data)} ingredients.")
