from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Ingredient

GOLDEN_FOODS = [
    {
        "name": "Oats, Rolled, Raw",
        "name_ar": "شوفان (نيء)",
        "category": "Grains",
        "calories_per_100g": 389.0,
        "protein_per_100g": 16.9,
        "carbs_per_100g": 66.3,
        "fats_per_100g": 6.9,
        "fiber_per_100g": 10.6,
        "fdc_id": "PR_OATS_RAW",
        "is_golden": True,
        "popularity_score": 100.0,
    },
    {
        "name": "Oatmeal, Cooked",
        "name_ar": "شوفان مطبوخ",
        "category": "Grains",
        "calories_per_100g": 71.0,
        "protein_per_100g": 2.5,
        "carbs_per_100g": 12.0,
        "fats_per_100g": 1.5,
        "fiber_per_100g": 1.7,
        "fdc_id": "PR_OATS_CKD",
        "is_golden": True,
        "popularity_score": 90.0,
    },
    {
        "name": "Chicken Breast, Raw",
        "name_ar": "صدر دجاج (نيء)",
        "category": "Protein",
        "calories_per_100g": 120.0,
        "protein_per_100g": 22.5,
        "carbs_per_100g": 0.0,
        "fats_per_100g": 2.6,
        "fiber_per_100g": 0.0,
        "fdc_id": "PR_CHK_RAW",
        "is_golden": True,
        "popularity_score": 100.0,
    },
    {
        "name": "Chicken Breast, Grilled",
        "name_ar": "صدر دجاج مشوي",
        "category": "Protein",
        "calories_per_100g": 165.0,
        "protein_per_100g": 31.0,
        "carbs_per_100g": 0.0,
        "fats_per_100g": 3.6,
        "fiber_per_100g": 0.0,
        "fdc_id": "PR_CHK_GRL",
        "is_golden": True,
        "popularity_score": 95.0,
    },
    {
        "name": "White Rice, Raw",
        "name_ar": "أرز أبيض (نيء)",
        "category": "Grains",
        "calories_per_100g": 365.0,
        "protein_per_100g": 7.1,
        "carbs_per_100g": 80.0,
        "fats_per_100g": 0.7,
        "fiber_per_100g": 1.3,
        "fdc_id": "PR_RICE_RAW",
        "is_golden": True,
        "popularity_score": 90.0,
    },
    {
        "name": "White Rice, Cooked",
        "name_ar": "أرز أبيض مطبوخ",
        "category": "Grains",
        "calories_per_100g": 130.0,
        "protein_per_100g": 2.7,
        "carbs_per_100g": 28.0,
        "fats_per_100g": 0.3,
        "fiber_per_100g": 0.4,
        "fdc_id": "PR_RICE_CKD",
        "is_golden": True,
        "popularity_score": 95.0,
    },
    {
        "name": "Eggs, Whole, Raw",
        "name_ar": "بيض كامل (نيء)",
        "category": "Protein",
        "calories_per_100g": 143.0,
        "protein_per_100g": 12.6,
        "carbs_per_100g": 0.7,
        "fats_per_100g": 9.5,
        "fiber_per_100g": 0.0,
        "fdc_id": "PR_EGG_RAW",
        "is_golden": True,
        "popularity_score": 80.0,
    },
    {
        "name": "Eggs, Hard Boiled",
        "name_ar": "بيض مسلوق",
        "category": "Protein",
        "calories_per_100g": 155.0,
        "protein_per_100g": 12.6,
        "carbs_per_100g": 1.1,
        "fats_per_100g": 10.6,
        "fiber_per_100g": 0.0,
        "fdc_id": "PR_EGG_BOIL",
        "is_golden": True,
        "popularity_score": 100.0,
    },
    {
        "name": "Sweet Potato, Raw",
        "name_ar": "بطاطا حلوة (نيء)",
        "category": "Vegetables",
        "calories_per_100g": 86.0,
        "protein_per_100g": 1.6,
        "carbs_per_100g": 20.1,
        "fats_per_100g": 0.1,
        "fiber_per_100g": 3.0,
        "fdc_id": "PR_SWT_PTT_RAW",
        "is_golden": True,
        "popularity_score": 80.0,
    },
    {
        "name": "Sweet Potato, Baked",
        "name_ar": "بطاطا حلوة مشوية",
        "category": "Vegetables",
        "calories_per_100g": 90.0,
        "protein_per_100g": 2.0,
        "carbs_per_100g": 20.7,
        "fats_per_100g": 0.2,
        "fiber_per_100g": 3.3,
        "fdc_id": "PR_SWT_PTT_BKD",
        "is_golden": True,
        "popularity_score": 90.0,
    }
]

def seed_golden_foods():
    db = SessionLocal()
    try:
        for f in GOLDEN_FOODS:
            # Check if exists
            existing = db.query(Ingredient).filter(Ingredient.fdc_id == f["fdc_id"]).first()
            if not existing:
                food_record = Ingredient(
                    name=f["name"],
                    name_ar=f["name_ar"],
                    category=f["category"],
                    calories_per_100g=f["calories_per_100g"],
                    protein_per_100g=f["protein_per_100g"],
                    carbs_per_100g=f["carbs_per_100g"],
                    fats_per_100g=f["fats_per_100g"],
                    fiber_per_100g=f.get("fiber_per_100g", 0.0),
                    fdc_id=f["fdc_id"],
                    source="MacroMetrics Core",
                    is_golden=True,
                    popularity_score=f["popularity_score"],
                )
                db.add(food_record)
        db.commit()
        print("Golden Foods seeded perfectly.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding golden foods: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_golden_foods()
