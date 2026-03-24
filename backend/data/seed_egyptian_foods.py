"""
Seed Egyptian Foods into the Database
======================================
Seeds Egyptian/Middle Eastern foods with full macro data.
Run: cd backend && python -m data.seed_egyptian_foods
"""
from dotenv import load_dotenv
load_dotenv()

from database import SessionLocal
from models import Ingredient
from data.egyptian_foods import EGYPTIAN_FOODS


def seed_egyptian_foods():
    db = SessionLocal()
    try:
        seeded_count = 0
        skipped_count = 0
        
        for food in EGYPTIAN_FOODS:
            # Check if food already exists (by English name)
            existing = db.query(Ingredient).filter(
                Ingredient.name.ilike(food["en"])
            ).first()
            
            if existing:
                skipped_count += 1
                continue
            
            # Create new ingredient
            ingredient = Ingredient(
                name=food["en"],
                name_ar=food["ar"],
                category=food["category"],
                calories_per_100g=food["calories"],
                protein_per_100g=food["protein"],
                carbs_per_100g=food["carbs"],
                fats_per_100g=food["fats"],
                fiber_per_100g=food.get("fiber", 0.0),
                fdc_id=f"EGYPT_{food['en'].upper().replace(' ', '_')}",
                source="Egyptian Database",
                is_golden=True,  # Mark as golden for priority search
                popularity_score=50.0,  # Medium priority (below curated golden foods)
            )
            db.add(ingredient)
            seeded_count += 1
        
        db.commit()
        print(f"[OK] Seeded {seeded_count} Egyptian foods. Skipped {skipped_count} existing foods.")
        
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error seeding Egyptian foods: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_egyptian_foods()
