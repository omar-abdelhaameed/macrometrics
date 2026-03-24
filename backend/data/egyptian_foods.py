"""
Egyptian Food Priority List
===========================
List of common Egyptian/Middle Eastern foods that should appear first in search results.
This list is used to prioritize local foods over USDA generic results.
"""

EGYPTIAN_PRIORITY_FOODS = [
    # ==================== PROTEINS ====================
    {"ar": "دجاج", "en": "Chicken Breast", "category": "Protein"},
    {"ar": "دجاج كامل", "en": "Whole Chicken", "category": "Protein"},
    {"ar": "لحم beef", "en": "Beef", "category": "Protein"},
    {"ar": "لحم ضاني", "en": "Lamb", "category": "Protein"},
    {"ar": "سمك", "en": "Fish", "category": "Protein"},
    {"ar": "سمك بلطي", "en": "Tilapia", "category": "Protein"},
    {"ar": "سمك سلمون", "en": "Salmon", "category": "Protein"},
    {"ar": "جمبري", "en": "Shrimp", "category": "Protein"},
    {"ar": "بيض", "en": "Eggs", "category": "Protein"},
    {"ar": "بيض مسلوق", "en": "Boiled Eggs", "category": "Protein"},
    {"ar": "بيض مقلي", "en": "Fried Eggs", "category": "Protein"},
    {"ar": "Turkey", "en": "Turkey", "category": "Protein"},
    {"ar": "كبده", "en": "Liver", "category": "Protein"},
    
    # ==================== GRAINS ====================
    {"ar": "شوفان", "en": "Oats", "category": "Grains"},
    {"ar": "شوفان rolled", "en": "Rolled Oats", "category": "Grains"},
    {"ar": "أرز", "en": "Rice", "category": "Grains"},
    {"ar": "أرز أبيض", "en": "White Rice", "category": "Grains"},
    {"ar": "أرز بني", "en": "Brown Rice", "category": "Grains"},
    {"ar": "خبز", "en": "Bread", "category": "Grains"},
    {"ar": "خبز بلدي", "en": "Egyptian Bread", "category": "Grains"},
    {"ar": "توست", "en": "Toast Bread", "category": "Grains"},
    {"ar": "شيبس", "en": "Pita Bread", "category": "Grains"},
    {"ar": "معكرونه", "en": "Pasta", "category": "Grains"},
    {"ar": "سباغتي", "en": "Spaghetti", "category": "Grains"},
    {"ar": "مكرونه", "en": "Macaroni", "category": "Grains"},
    {"ar": "دقيق", "en": "Flour", "category": "Grains"},
    {"ar": "سميد", "en": "Semolina", "category": "Grains"},
    {"ar": "بر", "en": "Barley", "category": "Grains"},
    
    # ==================== DAIRY ====================
    {"ar": "حليب", "en": "Milk", "category": "Dairy"},
    {"ar": "حليب كامل الدسم", "en": "Whole Milk", "category": "Dairy"},
    {"ar": "حليب قليل الدسم", "en": "Skim Milk", "category": "Dairy"},
    {"ar": "زبادي", "en": "Yogurt", "category": "Dairy"},
    {"ar": "زبادي يوناني", "en": "Greek Yogurt", "category": "Dairy"},
    {"ar": "لبنه", "en": "Labneh", "category": "Dairy"},
    {"ar": "جبنه", "en": "Cheese", "category": "Dairy"},
    {"ar": "جبنه موزارلا", "en": "Mozzarella", "category": "Dairy"},
    {"ar": "جبنه شيدر", "en": "Cheddar Cheese", "category": "Dairy"},
    {"ar": "جبنه فيتا", "en": "Feta Cheese", "category": "Dairy"},
    {"ar": "جبنه قريش", "en": "Ricotta Cheese", "category": "Dairy"},
    {"ar": "قشطه", "en": "Cream", "category": "Dairy"},
    {"ar": "كريمه", "en": "Heavy Cream", "category": "Dairy"},
    {"ar": "كيري", "en": "Cream Cheese", "category": "Dairy"},
    {"ar": "زبه", "en": "Butter", "category": "Dairy"},
    
    # ==================== LEGUMES ====================
    {"ar": "فول", "en": "Fava Beans", "category": "Legumes"},
    {"ar": "فول مطبوخ", "en": "Cooked Fava Beans", "category": "Legumes"},
    {"ar": "عدس", "en": "Lentils", "category": "Legumes"},
    {"ar": "عدس أحمر", "en": "Red Lentils", "category": "Legumes"},
    {"ar": "عدس أخضر", "en": "Green Lentils", "category": "Legumes"},
    {"ar": "حمص", "en": "Chickpeas", "category": "Legumes"},
    {"ar": "حمص طحيني", "en": "Hummus", "category": "Legumes"},
    {"ar": "لوبياء", "en": "Green Beans", "category": "Legumes"},
    {"ar": "فاصوليا", "en": "Kidney Beans", "category": "Legumes"},
    {"ar": "فاصوليا بيضاء", "en": "White Beans", "category": "Legumes"},
    
    # ==================== VEGETABLES ====================
    {"ar": "بطاطس", "en": "Potato", "category": "Vegetables"},
    {"ar": "بطاطس مسلوقه", "en": "Boiled Potato", "category": "Vegetables"},
    {"ar": "بطاطس مقلية", "en": "French Fries", "category": "Vegetables"},
    {"ar": "طماطم", "en": "Tomato", "category": "Vegetables"},
    {"ar": "طماطم كرز", "en": "Cherry Tomatoes", "category": "Vegetables"},
    {"ar": "خيار", "en": "Cucumber", "category": "Vegetables"},
    {"ar": "جزر", "en": "Carrot", "category": "Vegetables"},
    {"ar": "بصل", "en": "Onion", "category": "Vegetables"},
    {"ar": "ثوم", "en": "Garlic", "category": "Vegetables"},
    {"ar": "فلفل", "en": "Pepper", "category": "Vegetables"},
    {"ar": "فليفلة", "en": "Bell Pepper", "category": "Vegetables"},
    {"ar": "خس", "en": "Lettuce", "category": "Vegetables"},
    {"ar": "جرجير", "en": "Arugula", "category": "Vegetables"},
    {"ar": "بقدونس", "en": "Parsley", "category": "Vegetables"},
    {"ar": "كزبرة", "en": "Coriander", "category": "Vegetables"},
    {"ar": "باذنجان", "en": "Eggplant", "category": "Vegetables"},
    {"ar": "كوسه", "en": "Zucchini", "category": "Vegetables"},
    {"ar": "فاصوليا خضراء", "en": "Green Beans", "category": "Vegetables"},
    {"ar": "بروكلي", "en": "Broccoli", "category": "Vegetables"},
    {"ar": "قرنبيط", "en": "Cauliflower", "category": "Vegetables"},
    
    # ==================== FRUITS ====================
    {"ar": "تفاح", "en": "Apple", "category": "Fruits"},
    {"ar": "موز", "en": "Banana", "category": "Fruits"},
    {"ar": "عنب", "en": "Grapes", "category": "Fruits"},
    {"ar": "برتقال", "en": "Orange", "category": "Fruits"},
    {"ar": "ليمون", "en": "Lemon", "category": "Fruits"},
    {"ar": "مانجو", "en": "Mango", "category": "Fruits"},
    {"ar": "بطيخ", "en": "Watermelon", "category": "Fruits"},
    {"ar": "فراوله", "en": "Strawberry", "category": "Fruits"},
    {"ar": "عنب اسود", "en": "Black Grapes", "category": "Fruits"},
    {"ar": "تين", "en": "Fig", "category": "Fruits"},
    {"ar": "موز مجفف", "en": "Dried Dates", "category": "Fruits"},
    {"ar": "جميز", "en": "Sycamore Fig", "category": "Fruits"},
    
    # ==================== FATS & OILS ====================
    {"ar": "زيت زيتون", "en": "Olive Oil", "category": "Fats"},
    {"ar": "زيت ذرة", "en": "Corn Oil", "category": "Fats"},
    {"ar": "زيت عباد الشمس", "en": "Sunflower Oil", "category": "Fats"},
    {"ar": "زبت", "en": "Ghee", "category": "Fats"},
    {"ar": "زيت", "en": "Vegetable Oil", "category": "Fats"},
    {"ar": "زبت مكواه", "en": "Clarified Butter", "category": "Fats"},
    
    # ==================== NUTS & SEEDS ====================
    {"ar": "لوز", "en": "Almonds", "category": "Nuts"},
    {"ar": "فستق", "en": "Pistachio", "category": "Nuts"},
    {"ar": "كاجو", "en": "Cashews", "category": "Nuts"},
    {"ar": "جوز", "en": "Walnuts", "category": "Nuts"},
    {"ar": "سمسم", "en": "Sesame", "category": "Seeds"},
    {"ar": "طحينة", "en": "Tahini", "category": "Seeds"},
    {"ar": "صنوبر", "en": "Pine Nuts", "category": "Nuts"},
    
    # ==================== OTHER COMMON ====================
    {"ar": "عسل", "en": "Honey", "category": "Sweeteners"},
    {"ar": "سكر", "en": "Sugar", "category": "Sweeteners"},
    {"ar": "ملح", "en": "Salt", "category": "Seasonings"},
    {"ar": "بهارات", "en": "Spices", "category": "Seasonings"},
    {"ar": "كمون", "en": "Cumin", "category": "Seasonings"},
    {"ar": "كركم", "en": "Turmeric", "category": "Seasonings"},
    {"ar": "فلفل أسود", "en": "Black Pepper", "category": "Seasonings"},
]

# Create a lookup dictionary for quick search
FOOD_LOOKUP = {food["en"].lower(): food for food in EGYPTIAN_PRIORITY_FOODS}
FOOD_LOOKUP_AR = {food["ar"]: food for food in EGYPTIAN_PRIORITY_FOODS}

def get_food_by_name(name: str, language: str = "en") -> dict | None:
    """Get food by name in specified language."""
    name_lower = name.lower().strip()
    if language == "ar":
        return FOOD_LOOKUP_AR.get(name)
    return FOOD_LOOKUP.get(name_lower)

def search_foods(query: str, language: str = "en") -> list[dict]:
    """Search foods in the priority list."""
    query_lower = query.lower().strip()
    results = []
    
    if language == "ar":
        for food in EGYPTIAN_PRIORITY_FOODS:
            if query_lower in food["ar"].lower() or query_lower in food["en"].lower():
                results.append(food)
    else:
        for food in EGYPTIAN_PRIORITY_FOODS:
            if query_lower in food["en"].lower() or query_lower in food["ar"]:
                results.append(food)
    
    return results

def get_all_priority_foods() -> list[dict]:
    """Return all priority foods."""
    return EGYPTIAN_PRIORITY_FOODS

def get_foods_by_category(category: str) -> list[dict]:
    """Get all foods in a specific category."""
    return [f for f in EGYPTIAN_PRIORITY_FOODS if f["category"] == category]

def translate_to_english(arabic_name: str) -> str | None:
    """Translate Arabic food name to English."""
    food = FOOD_LOOKUP_AR.get(arabic_name)
    return food["en"] if food else None