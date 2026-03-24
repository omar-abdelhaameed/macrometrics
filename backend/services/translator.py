"""
Translator Service for Smart Food Search
=========================================
Handles Arabic to English translation and priority food matching.
"""

from typing import List, Dict, Optional
from data.egyptian_foods import (
    EGYPTIAN_PRIORITY_FOODS,
    search_foods as search_priority_foods,
    translate_to_english,
    get_foods_by_category,
    get_all_priority_foods,
)

# Arabic to English translation map for common search terms
TRANSLATION_MAP = {
    # Proteins
    "دجاج": "chicken",
    "فراخ": "chicken",
    "لحم": "beef",
    "لحم beef": "beef",
    "لحم ضاني": "lamb",
    "lamb": "lamb",
    "سمك": "fish",
    "بيض": "egg",
    "بيض": "eggs",
    "Turkey": "turkey",
    "كبده": "liver",
    
    # Grains
    "شوفان": "oats",
    "أرز": "rice",
    "خبز": "bread",
    "توست": "toast",
    "شيبس": "pita",
    "معكرونه": "pasta",
    "سباغتي": "spaghetti",
    "مكرونه": "macaroni",
    "دقيق": "flour",
    "سميد": "semolina",
    "بر": "barley",
    
    # Dairy
    "حليب": "milk",
    "زبادي": "yogurt",
    "لبنه": "labneh",
    "جبنه": "cheese",
    "جبن": "cheese",
    "قشطه": "cream",
    "كريمه": "cream",
    "كيري": "cream cheese",
    "زبه": "butter",
    
    # Legumes
    "فول": "fava beans",
    "عدس": "lentils",
    "حمص": "chickpeas",
    "لوبياء": "green beans",
    "فاصوليا": "kidney beans",
    
    # Vegetables
    "بطاطس": "potato",
    "طماطم": "tomato",
    "خيار": "cucumber",
    "جزر": "carrot",
    "بصل": "onion",
    "ثوم": "garlic",
    "فلفل": "pepper",
    "خس": "lettuce",
    "جرجير": "arugula",
    "بقدونس": "parsley",
    "كزبرة": "coriander",
    "باذنجان": "eggplant",
    "كوسه": "zucchini",
    "بروكلي": "broccoli",
    "قرنبيط": "cauliflower",
    
    # Fruits
    "تفاح": "apple",
    "موز": "banana",
    "عنب": "grapes",
    "برتقال": "orange",
    "ليمون": "lemon",
    "مانجو": "mango",
    "بطيخ": "watermelon",
    "فراوله": "strawberry",
    "تين": "fig",
    
    # Fats & Oils
    "زيت زيتون": "olive oil",
    "زيت": "oil",
    "زبت": "ghee",
    
    # Nuts
    "لوز": "almonds",
    "فستق": "pistachio",
    "كاجو": "cashews",
    "جوز": "walnuts",
    "سمسم": "sesame",
    "طحينة": "tahini",
    
    # Other
    "عسل": "honey",
    "سكر": "sugar",
    "ملح": "salt",
    "بهارات": "spices",
    "كمون": "cumin",
}


def is_arabic(text: str) -> bool:
    """Check if text contains Arabic characters."""
    return any('\u0600' <= c <= '\u06FF' for c in text)


def translate_search_query(query: str) -> str:
    """
    Translate Arabic search query to English for USDA search.
    Returns translated query if Arabic, otherwise returns original.
    """
    query_clean = query.strip().lower()
    
    # Check direct translation
    if query_clean in TRANSLATION_MAP:
        return TRANSLATION_MAP[query_clean]
    
    # Check if it's Arabic and try to find partial match
    if is_arabic(query):
        for arabic, english in TRANSLATION_MAP.items():
            if arabic in query_clean or query_clean in arabic:
                return english
    
    return query


def smart_search(query: str, language: str = "en") -> Dict[str, List[Dict]]:
    """
    Perform smart food search with priority results.
    
    Returns:
        {
            "priority_foods": [...],  # Egyptian foods matching query
            "translated_query": "...",  # English version for USDA
            "is_arabic": bool
        }
    """
    is_arabic_query = is_arabic(query)
    
    # Get priority foods that match the query
    priority_results = search_priority_foods(query, language)
    
    # Translate if Arabic
    translated_query = translate_search_query(query) if is_arabic_query else query
    
    return {
        "priority_foods": priority_results,
        "translated_query": translated_query,
        "is_arabic": is_arabic_query,
        "language": language
    }


def merge_search_results(priority_foods: List[Dict], usda_foods: List[Dict], max_results: int = 15) -> List[Dict]:
    """
    Merge priority foods with USDA results.
    Priority foods come first, then USDA results. Priority foods will inherit macros from the top USDA match.
    """
    results = []
    
    # Grab macros from the top USDA result so Arabic priorities have nutritional info
    base_macros = None
    if usda_foods:
        top = usda_foods[0]
        base_macros = {
            "fdc_id": str(top.get("fdc_id")) if top.get("fdc_id") else "",
            "calories_per_100g": float(top.get("calories_per_100g") or 0.0),
            "protein_per_100g": float(top.get("protein_per_100g") or 0.0),
            "carbs_per_100g": float(top.get("carbs_per_100g") or 0.0),
            "fats_per_100g": float(top.get("fats_per_100g") or 0.0),
        }
    
    # Add priority foods first (with "priority" source)
    for food in priority_foods[:5]:  # Max 5 priority results
        # Give priority foods a unique fake FDC ID based on their name so they don't incorrectly merge
        fake_fdc_id = "PR_" + food["en"].replace(" ", "").upper()
        
        item = {
            "name": food["ar"] + " - " + food["en"],
            "name_ar": food["ar"],
            "category": food["category"],
            "source": "USDA FDC",
            "is_priority": True
        }
        
        if base_macros:
            item.update(base_macros)
            item["fdc_id"] = fake_fdc_id  # Ensure uniqueness
        else:
            item.update({
                "fdc_id": fake_fdc_id,
                "calories_per_100g": 0.0, "protein_per_100g": 0.0, "carbs_per_100g": 0.0, "fats_per_100g": 0.0
            })
        results.append(item)
    
    # Add USDA results (skip duplicates by name)
    priority_names = {f["en"].lower() for f in priority_foods}
    usda_count = 0
    for food in usda_foods:
        if usda_count >= max_results - len(results):
            break
        if food.get("name", "").lower() not in priority_names:
            results.append({
                "name": food.get("name", ""),
                "name_ar": None,
                "category": food.get("category", ""),
                "source": "USDA FDC",
                "is_priority": False,
                "fdc_id": food.get("fdc_id"),
                "calories_per_100g": food.get("calories_per_100g"),
                "protein_per_100g": food.get("protein_per_100g"),
                "carbs_per_100g": food.get("carbs_per_100g"),
                "fats_per_100g": food.get("fats_per_100g"),
            })
            usda_count += 1
    
    return results


def get_categories() -> List[str]:
    """Get all available food categories."""
    categories = set()
    for food in EGYPTIAN_PRIORITY_FOODS:
        categories.add(food["category"])
    return sorted(list(categories))