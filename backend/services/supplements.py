"""
Supplement Recommendation Engine
=================================
Analyzes user profile to recommend optimal supplements.
"""
from sqlalchemy.orm import Session
from models import SupplementCatalog, User


def get_supplement_recommendations(
    db: Session,
    user: User
) -> list[dict]:
    """
    Generate personalized supplement recommendations based on user's profile.
    
    Factors considered:
    - primary_goal (cut, bulk, maintain)
    - activity_level (sedentary, light, moderate, active, very_active)
    """
    goal = (user.primary_goal or "maintain").lower()
    activity = (user.activity_level or "moderate").lower()
    
    recommendations = []
    added_names = set()
    
    # ==================== UNIVERSAL (Everyone) ====================
    universal_supplements = [
        "Vitamin D3",
        "Multivitamin",
        "Omega-3 Fish Oil",
    ]
    
    for name in universal_supplements:
        supp = db.query(SupplementCatalog).filter(SupplementCatalog.name == name).first()
        if supp and name not in added_names:
            recommendations.append({
                "id": supp.id,
                "name": supp.name,
                "description": supp.description,
                "standard_dosage": supp.standard_dosage,
                "unit": supp.unit,
                "category": supp.category,
                "target_goal": supp.target_goal,
                "benefits": supp.benefits,
                "reason": "Essential for overall health",
                "priority": 1
            })
            added_names.add(name)
    
    # ==================== GOAL-SPECIFIC ====================
    if "bulk" in goal or "gain" in goal:
        bulk_supplements = [
            ("Whey Protein Isolate", "Essential for muscle protein synthesis"),
            ("Creatine Monohydrate", "Enhances strength and muscle volume"),
            ("Beta-Ecdysterone", "Natural anabolic support"),
            ("Zinc", "Supports testosterone and recovery"),
        ]
        for name, reason in bulk_supplements:
            supp = db.query(SupplementCatalog).filter(SupplementCatalog.name == name).first()
            if supp and name not in added_names:
                recommendations.append({
                    "id": supp.id,
                    "name": supp.name,
                    "description": supp.description,
                    "standard_dosage": supp.standard_dosage,
                    "unit": supp.unit,
                    "category": supp.category,
                    "target_goal": supp.target_goal,
                    "benefits": supp.benefits,
                    "reason": reason,
                    "priority": 2
                })
                added_names.add(name)
    
    elif "cut" in goal or "lose" in goal:
        cut_supplements = [
            ("Omega-3 (EPA 1000mg)", "Anti-inflammatory and fat loss support"),
            ("L-Carnitine", "Supports fat metabolism"),
            ("Caffeine", "Enhances fat oxidation and energy"),
            ("Magnesium Glycinate", "Supports sleep and recovery"),
        ]
        for name, reason in cut_supplements:
            supp = db.query(SupplementCatalog).filter(SupplementCatalog.name == name).first()
            if supp and name not in added_names:
                recommendations.append({
                    "id": supp.id,
                    "name": supp.name,
                    "description": supp.description,
                    "standard_dosage": supp.standard_dosage,
                    "unit": supp.unit,
                    "category": supp.category,
                    "target_goal": supp.target_goal,
                    "benefits": supp.benefits,
                    "reason": reason,
                    "priority": 2
                })
                added_names.add(name)
    
    else:  # maintain
        maintain_supplements = [
            ("Casein Protein", "Sustained protein release"),
            ("Vitamin C", "Antioxidant protection"),
        ]
        for name, reason in maintain_supplements:
            supp = db.query(SupplementCatalog).filter(SupplementCatalog.name == name).first()
            if supp and name not in added_names:
                recommendations.append({
                    "id": supp.id,
                    "name": supp.name,
                    "description": supp.description,
                    "standard_dosage": supp.standard_dosage,
                    "unit": supp.unit,
                    "category": supp.category,
                    "target_goal": supp.target_goal,
                    "benefits": supp.benefits,
                    "reason": reason,
                    "priority": 2
                })
                added_names.add(name)
    
    # ==================== ACTIVITY-BASED ====================
    if "very_active" in activity or "active" in activity:
        activity_supplements = [
            ("BCAA (Branched-Chain Amino Acids)", "Reduces muscle soreness"),
            ("Magnesium Glycinate", "Improves sleep and recovery"),
            ("L-Glutamine", "Supports immune system"),
            ("Beta-Alanine", "Delays fatigue"),
        ]
        for name, reason in activity_supplements:
            supp = db.query(SupplementCatalog).filter(SupplementCatalog.name == name).first()
            if supp and name not in added_names:
                recommendations.append({
                    "id": supp.id,
                    "name": supp.name,
                    "description": supp.description,
                    "standard_dosage": supp.standard_dosage,
                    "unit": supp.unit,
                    "category": supp.category,
                    "target_goal": supp.target_goal,
                    "benefits": supp.benefits,
                    "reason": reason,
                    "priority": 3
                })
                added_names.add(name)
    
    # ==================== STRESS & SLEEP ====================
    stress_supplements = [
        ("Ashwagandha", "Adaptogen for stress management"),
    ]
    for name, reason in stress_supplements:
        supp = db.query(SupplementCatalog).filter(SupplementCatalog.name == name).first()
        if supp and name not in added_names:
            recommendations.append({
                "id": supp.id,
                "name": supp.name,
                "description": supp.description,
                "standard_dosage": supp.standard_dosage,
                "unit": supp.unit,
                "category": supp.category,
                "target_goal": supp.target_goal,
                "benefits": supp.benefits,
                "reason": reason,
                "priority": 4
            })
            added_names.add(name)
    
    # Sort by priority
    recommendations.sort(key=lambda x: x["priority"])
    
    return recommendations


def get_supplement_by_category(
    db: Session,
    category: str = None
) -> list[dict]:
    """Get all supplements, optionally filtered by category."""
    query = db.query(SupplementCatalog)
    
    if category:
        query = query.filter(SupplementCatalog.category == category)
    
    supplements = query.order_by(SupplementCatalog.name).all()
    
    return [{
        "id": s.id,
        "name": s.name,
        "description": s.description,
        "standard_dosage": s.standard_dosage,
        "unit": s.unit,
        "category": s.category,
        "target_goal": s.target_goal,
        "benefits": s.benefits,
    } for s in supplements]
