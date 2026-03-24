"""
Seed Supplement Catalog
======================
Populates the supplement catalog with real-world vitamins and supplements.
Run: cd backend && python -m data.seed_supplements
"""
from dotenv import load_dotenv
load_dotenv()

from database import SessionLocal
from models import SupplementCatalog


SUPPLEMENT_CATALOG = [
    # ==================== PROTEIN & AMINO ACIDS ====================
    {
        "name": "Whey Protein Isolate",
        "description": "Fast-absorbing protein for muscle recovery and growth. Contains 24g protein per scoop.",
        "standard_dosage": 30.0,
        "unit": "g",
        "category": "Protein",
        "target_goal": "bulk",
        "benefits": "High bioavailability, complete amino acid profile, supports muscle protein synthesis",
        "recommended_for_activity": "active"
    },
    {
        "name": "Casein Protein",
        "description": "Slow-digesting protein ideal for nighttime use. Provides sustained amino acid release.",
        "standard_dosage": 30.0,
        "unit": "g",
        "category": "Protein",
        "target_goal": "maintain",
        "benefits": "Slow absorption, prevents muscle breakdown during sleep",
        "recommended_for_activity": "moderate"
    },
    {
        "name": "Creatine Monohydrate",
        "description": "The most researched sports supplement. Enhances strength, power, and muscle volume.",
        "standard_dosage": 5.0,
        "unit": "g",
        "category": "Amino Acid",
        "target_goal": "bulk",
        "benefits": "Increases ATP production, improves workout performance, supports cognitive function",
        "recommended_for_activity": "active"
    },
    {
        "name": "BCAA (Branched-Chain Amino Acids)",
        "description": "Essential amino acids (Leucine, Isoleucine, Valine) that directly stimulate muscle protein synthesis.",
        "standard_dosage": 10.0,
        "unit": "g",
        "category": "Amino Acid",
        "target_goal": "all",
        "benefits": "Reduces muscle soreness, promotes recovery, preserves lean muscle",
        "recommended_for_activity": "active"
    },
    {
        "name": "L-Glutamine",
        "description": "Supports gut health and immune function. Important for recovery after intense training.",
        "standard_dosage": 5.0,
        "unit": "g",
        "category": "Amino Acid",
        "target_goal": "all",
        "benefits": "Supports immune system, aids recovery, improves gut health",
        "recommended_for_activity": "very_active"
    },
    {
        "name": "Beta-Alanine",
        "description": "Increases muscle carnosine levels, buffering acid during high-intensity exercise.",
        "standard_dosage": 3.2,
        "unit": "g",
        "category": "Amino Acid",
        "target_goal": "bulk",
        "benefits": "Delays fatigue, improves endurance, enhances exercise capacity",
        "recommended_for_activity": "active"
    },

    # ==================== OMEGAS & FATS ====================
    {
        "name": "Omega-3 Fish Oil",
        "description": "Essential fatty acids (EPA/DHA) for heart health, brain function, and inflammation reduction.",
        "standard_dosage": 2000.0,
        "unit": "mg",
        "category": "Fatty Acid",
        "target_goal": "all",
        "benefits": "Reduces inflammation, supports heart health, improves brain function",
        "recommended_for_activity": "all"
    },
    {
        "name": "Omega-3 (EPA 1000mg)",
        "description": "High-dose EPA for anti-inflammatory benefits and cardiovascular support.",
        "standard_dosage": 1000.0,
        "unit": "mg",
        "category": "Fatty Acid",
        "target_goal": "cut",
        "benefits": "Powerful anti-inflammatory, supports fat loss, heart health",
        "recommended_for_activity": "all"
    },
    {
        "name": "MCT Oil",
        "description": "Medium-chain triglycerides for quick energy and ketone production.",
        "standard_dosage": 15.0,
        "unit": "ml",
        "category": "Fatty Acid",
        "target_goal": "cut",
        "benefits": "Sustained energy, supports ketosis, enhances focus",
        "recommended_for_activity": "moderate"
    },

    # ==================== VITAMINS ====================
    {
        "name": "Vitamin D3",
        "description": "Essential for bone health, immune function, and mood regulation. Many are deficient.",
        "standard_dosage": 5000.0,
        "unit": "IU",
        "category": "Vitamin",
        "target_goal": "all",
        "benefits": "Supports bone health, immune function, mood, testosterone levels",
        "recommended_for_activity": "all"
    },
    {
        "name": "Vitamin C",
        "description": "Powerful antioxidant that supports immune function and collagen production.",
        "standard_dosage": 1000.0,
        "unit": "mg",
        "category": "Vitamin",
        "target_goal": "all",
        "benefits": "Antioxidant protection, immune support, collagen synthesis",
        "recommended_for_activity": "all"
    },
    {
        "name": "Vitamin B-Complex",
        "description": "Complete B vitamin formula for energy metabolism and nervous system support.",
        "standard_dosage": 1.0,
        "unit": "capsule",
        "category": "Vitamin",
        "target_goal": "all",
        "benefits": "Energy production, brain function, stress management",
        "recommended_for_activity": "all"
    },
    {
        "name": "Multivitamin",
        "description": "Comprehensive daily vitamin/mineral formula for overall health insurance.",
        "standard_dosage": 1.0,
        "unit": "capsule",
        "category": "Vitamin",
        "target_goal": "all",
        "benefits": "Fills nutritional gaps, supports overall health, energy metabolism",
        "recommended_for_activity": "all"
    },

    # ==================== MINERALS ====================
    {
        "name": "Magnesium Glycinate",
        "description": "Highly bioavailable form of magnesium. Supports sleep, muscle function, and recovery.",
        "standard_dosage": 400.0,
        "unit": "mg",
        "category": "Mineral",
        "target_goal": "all",
        "benefits": "Improves sleep quality, reduces muscle cramps, supports recovery",
        "recommended_for_activity": "active"
    },
    {
        "name": "Zinc",
        "description": "Essential mineral for immune function, testosterone production, and protein synthesis.",
        "standard_dosage": 30.0,
        "unit": "mg",
        "category": "Mineral",
        "target_goal": "bulk",
        "benefits": "Supports testosterone, immune function, muscle protein synthesis",
        "recommended_for_activity": "all"
    },
    {
        "name": "Iron",
        "description": "Essential mineral for oxygen transport in blood. Important for energy levels.",
        "standard_dosage": 18.0,
        "unit": "mg",
        "category": "Mineral",
        "target_goal": "all",
        "benefits": "Prevents anemia, supports energy, oxygen transport",
        "recommended_for_activity": "all"
    },
    {
        "name": "Calcium",
        "description": "Essential mineral for bone health and muscle function.",
        "standard_dosage": 1000.0,
        "unit": "mg",
        "category": "Mineral",
        "target_goal": "all",
        "benefits": "Strong bones, muscle contraction, nerve function",
        "recommended_for_activity": "all"
    },
    {
        "name": "Potassium",
        "description": "Key electrolyte for muscle function and hydration balance.",
        "standard_dosage": 99.0,
        "unit": "mg",
        "category": "Mineral",
        "target_goal": "all",
        "benefits": "Muscle function, hydration, blood pressure regulation",
        "recommended_for_activity": "very_active"
    },

    # ==================== PERFORMANCE ====================
    {
        "name": "Caffeine",
        "description": "Stimulant for enhanced focus, energy, and fat oxidation during workouts.",
        "standard_dosage": 200.0,
        "unit": "mg",
        "category": "Stimulant",
        "target_goal": "cut",
        "benefits": "Increased alertness, enhanced fat burning, improved workout performance",
        "recommended_for_activity": "active"
    },
    {
        "name": "L-Carnitine",
        "description": "Amino acid derivative that helps transport fatty acids for energy.",
        "standard_dosage": 500.0,
        "unit": "mg",
        "category": "Amino Acid",
        "target_goal": "cut",
        "benefits": "Supports fat metabolism, improves endurance, heart health",
        "recommended_for_activity": "moderate"
    },
    {
        "name": "Ashwagandha",
        "description": "Adaptogenic herb that helps manage stress and cortisol levels.",
        "standard_dosage": 600.0,
        "unit": "mg",
        "category": "Herb",
        "target_goal": "all",
        "benefits": "Reduces stress, improves sleep, supports testosterone",
        "recommended_for_activity": "all"
    },
    {
        "name": "Beta-Ecdysterone",
        "description": "Natural anabolic compound from plants. May support muscle protein synthesis.",
        "standard_dosage": 500.0,
        "unit": "mg",
        "category": "Herb",
        "target_goal": "bulk",
        "benefits": "Muscle building support, recovery, strength enhancement",
        "recommended_for_activity": "active"
    },
]


def seed_supplements():
    db = SessionLocal()
    try:
        seeded_count = 0
        skipped_count = 0
        
        for supp_data in SUPPLEMENT_CATALOG:
            existing = db.query(SupplementCatalog).filter(
                SupplementCatalog.name == supp_data["name"]
            ).first()
            
            if existing:
                skipped_count += 1
                continue
            
            supplement = SupplementCatalog(**supp_data)
            db.add(supplement)
            seeded_count += 1
        
        db.commit()
        print(f"[OK] Seeded {seeded_count} supplements. Skipped {skipped_count} existing.")
        
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error seeding supplements: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_supplements()
