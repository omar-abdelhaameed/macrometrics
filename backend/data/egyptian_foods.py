"""
Egyptian/Middle Eastern Food Database with Full Macros
=======================================================
Common Egyptian foods with accurate nutritional data (per 100g).
Macros sourced from USDA and Egyptian food composition tables.
"""

EGYPTIAN_FOODS = [
    # ==================== PROTEINS ====================
    {"ar": "دجاج", "en": "Chicken Breast", "category": "Protein", "calories": 165, "protein": 31.0, "carbs": 0.0, "fats": 3.6, "fiber": 0.0},
    {"ar": "دجاج كامل", "en": "Whole Chicken", "category": "Protein", "calories": 239, "protein": 27.0, "carbs": 0.0, "fats": 14.0, "fiber": 0.0},
    {"ar": "لحم beef", "en": "Beef", "category": "Protein", "calories": 250, "protein": 26.0, "carbs": 0.0, "fats": 15.0, "fiber": 0.0},
    {"ar": "لحم ضاني", "en": "Lamb", "category": "Protein", "calories": 294, "protein": 25.0, "carbs": 0.0, "fats": 21.0, "fiber": 0.0},
    {"ar": "سمك", "en": "Fish", "category": "Protein", "calories": 136, "protein": 20.0, "carbs": 0.0, "fats": 5.0, "fiber": 0.0},
    {"ar": "سمك بلطي", "en": "Tilapia", "category": "Protein", "calories": 128, "protein": 26.0, "carbs": 0.0, "fats": 2.7, "fiber": 0.0},
    {"ar": "سمك سلمون", "en": "Salmon", "category": "Protein", "calories": 208, "protein": 20.0, "carbs": 0.0, "fats": 13.0, "fiber": 0.0},
    {"ar": "جمبري", "en": "Shrimp", "category": "Protein", "calories": 99, "protein": 24.0, "carbs": 0.2, "fats": 0.3, "fiber": 0.0},
    {"ar": "بيض", "en": "Eggs", "category": "Protein", "calories": 155, "protein": 13.0, "carbs": 1.1, "fats": 11.0, "fiber": 0.0},
    {"ar": "بيض مسلوق", "en": "Boiled Eggs", "category": "Protein", "calories": 155, "protein": 12.6, "carbs": 1.1, "fats": 10.6, "fiber": 0.0},
    {"ar": "بيض مقلي", "en": "Fried Eggs", "category": "Protein", "calories": 196, "protein": 13.6, "carbs": 0.8, "fats": 14.8, "fiber": 0.0},
    {"ar": "Turkey", "en": "Turkey", "category": "Protein", "calories": 189, "protein": 29.0, "carbs": 0.0, "fats": 7.4, "fiber": 0.0},
    {"ar": "كبده", "en": "Liver", "category": "Protein", "calories": 167, "protein": 26.0, "carbs": 4.0, "fats": 5.0, "fiber": 0.0},
    
    # ==================== GRAINS ====================
    {"ar": "شوفان", "en": "Oats", "category": "Grains", "calories": 389, "protein": 16.9, "carbs": 66.3, "fats": 6.9, "fiber": 10.6},
    {"ar": "شوفان مطبوخ", "en": "Cooked Oats", "category": "Grains", "calories": 71, "protein": 2.5, "carbs": 12.0, "fats": 1.5, "fiber": 1.7},
    {"ar": "أرز", "en": "Rice", "category": "Grains", "calories": 130, "protein": 2.7, "carbs": 28.0, "fats": 0.3, "fiber": 0.4},
    {"ar": "أرز أبيض", "en": "White Rice", "category": "Grains", "calories": 130, "protein": 2.7, "carbs": 28.0, "fats": 0.3, "fiber": 0.4},
    {"ar": "أرز بني", "en": "Brown Rice", "category": "Grains", "calories": 111, "protein": 2.6, "carbs": 23.0, "fats": 0.9, "fiber": 1.8},
    {"ar": "خبز", "en": "Bread", "category": "Grains", "calories": 265, "protein": 9.0, "carbs": 49.0, "fats": 3.2, "fiber": 2.7},
    {"ar": "خبز بلدي", "en": "Egyptian Bread", "category": "Grains", "calories": 280, "protein": 9.5, "carbs": 52.0, "fats": 4.0, "fiber": 3.0},
    {"ar": "توست", "en": "Toast Bread", "category": "Grains", "calories": 265, "protein": 9.0, "carbs": 49.0, "fats": 3.2, "fiber": 2.7},
    {"ar": "شيبس", "en": "Pita Bread", "category": "Grains", "calories": 275, "protein": 9.0, "carbs": 55.0, "fats": 1.2, "fiber": 2.0},
    {"ar": "معكرونه", "en": "Pasta", "category": "Grains", "calories": 131, "protein": 5.0, "carbs": 25.0, "fats": 1.1, "fiber": 1.8},
    {"ar": "سباغتي", "en": "Spaghetti", "category": "Grains", "calories": 131, "protein": 5.0, "carbs": 25.0, "fats": 1.1, "fiber": 1.8},
    {"ar": "مكرونه", "en": "Macaroni", "category": "Grains", "calories": 131, "protein": 5.0, "carbs": 25.0, "fats": 1.1, "fiber": 1.8},
    {"ar": "دقيق", "en": "Flour", "category": "Grains", "calories": 364, "protein": 10.0, "carbs": 76.0, "fats": 1.0, "fiber": 2.7},
    {"ar": "سميد", "en": "Semolina", "category": "Grains", "calories": 360, "protein": 13.0, "carbs": 73.0, "fats": 1.5, "fiber": 3.0},
    {"ar": "بر", "en": "Barley", "category": "Grains", "calories": 354, "protein": 12.0, "carbs": 77.0, "fats": 2.0, "fiber": 6.0},
    
    # ==================== DAIRY ====================
    {"ar": "حليب", "en": "Milk", "category": "Dairy", "calories": 61, "protein": 3.2, "carbs": 4.8, "fats": 3.3, "fiber": 0.0},
    {"ar": "حليب كامل الدسم", "en": "Whole Milk", "category": "Dairy", "calories": 61, "protein": 3.2, "carbs": 4.8, "fats": 3.3, "fiber": 0.0},
    {"ar": "حليب قليل الدسم", "en": "Skim Milk", "category": "Dairy", "calories": 34, "protein": 3.4, "carbs": 5.0, "fats": 0.1, "fiber": 0.0},
    {"ar": "زبادي", "en": "Yogurt", "category": "Dairy", "calories": 59, "protein": 10.0, "carbs": 3.6, "fats": 0.7, "fiber": 0.0},
    {"ar": "زبادي يوناني", "en": "Greek Yogurt", "category": "Dairy", "calories": 97, "protein": 9.0, "carbs": 3.6, "fats": 5.0, "fiber": 0.0},
    {"ar": "لبنه", "en": "Labneh", "category": "Dairy", "calories": 243, "protein": 14.0, "carbs": 3.0, "fats": 20.0, "fiber": 0.0},
    {"ar": "جبنه", "en": "Cheese", "category": "Dairy", "calories": 402, "protein": 25.0, "carbs": 1.3, "fats": 33.0, "fiber": 0.0},
    {"ar": "جبنه موزارلا", "en": "Mozzarella", "category": "Dairy", "calories": 280, "protein": 28.0, "carbs": 3.1, "fats": 17.0, "fiber": 0.0},
    {"ar": "جبنه شيدر", "en": "Cheddar Cheese", "category": "Dairy", "calories": 403, "protein": 25.0, "carbs": 1.3, "fats": 33.0, "fiber": 0.0},
    {"ar": "جبنه فيتا", "en": "Feta Cheese", "category": "Dairy", "calories": 264, "protein": 14.0, "carbs": 4.1, "fats": 21.0, "fiber": 0.0},
    {"ar": "جبنه قريش", "en": "Ricotta Cheese", "category": "Dairy", "calories": 174, "protein": 11.0, "carbs": 3.0, "fats": 13.0, "fiber": 0.0},
    {"ar": "قشطه", "en": "Cream", "category": "Dairy", "calories": 340, "protein": 2.0, "carbs": 2.8, "fats": 36.0, "fiber": 0.0},
    {"ar": "كريمه", "en": "Heavy Cream", "category": "Dairy", "calories": 340, "protein": 2.0, "carbs": 2.8, "fats": 36.0, "fiber": 0.0},
    {"ar": "كيري", "en": "Cream Cheese", "category": "Dairy", "calories": 342, "protein": 6.0, "carbs": 4.0, "fats": 34.0, "fiber": 0.0},
    {"ar": "زبه", "en": "Butter", "category": "Dairy", "calories": 717, "protein": 0.9, "carbs": 0.1, "fats": 81.0, "fiber": 0.0},
    
    # ==================== LEGUMES ====================
    {"ar": "فول", "en": "Fava Beans", "category": "Legumes", "calories": 110, "protein": 7.6, "carbs": 19.0, "fats": 0.4, "fiber": 5.0},
    {"ar": "فول مطبوخ", "en": "Cooked Fava Beans", "category": "Legumes", "calories": 110, "protein": 7.6, "carbs": 19.0, "fats": 0.4, "fiber": 5.0},
    {"ar": "عدس", "en": "Lentils", "category": "Legumes", "calories": 116, "protein": 9.0, "carbs": 20.0, "fats": 0.4, "fiber": 7.9},
    {"ar": "عدس أحمر", "en": "Red Lentils", "category": "Legumes", "calories": 116, "protein": 9.0, "carbs": 20.0, "fats": 0.4, "fiber": 6.0},
    {"ar": "عدس أخضر", "en": "Green Lentils", "category": "Legumes", "calories": 116, "protein": 9.0, "carbs": 20.0, "fats": 0.4, "fiber": 7.9},
    {"ar": "حمص", "en": "Chickpeas", "category": "Legumes", "calories": 164, "protein": 8.9, "carbs": 27.0, "fats": 2.6, "fiber": 7.6},
    {"ar": "حمص طحيني", "en": "Hummus", "category": "Legumes", "calories": 166, "protein": 7.9, "carbs": 14.0, "fats": 9.6, "fiber": 6.0},
    {"ar": "لوبياء", "en": "Green Beans", "category": "Legumes", "calories": 31, "protein": 1.8, "carbs": 7.0, "fats": 0.1, "fiber": 3.4},
    {"ar": "فاصوليا", "en": "Kidney Beans", "category": "Legumes", "calories": 127, "protein": 8.7, "carbs": 23.0, "fats": 0.5, "fiber": 6.4},
    {"ar": "فاصوليا بيضاء", "en": "White Beans", "category": "Legumes", "calories": 139, "protein": 9.7, "carbs": 25.0, "fats": 0.5, "fiber": 6.3},
    
    # ==================== VEGETABLES ====================
    {"ar": "بطاطس", "en": "Potato", "category": "Vegetables", "calories": 77, "protein": 2.0, "carbs": 17.0, "fats": 0.1, "fiber": 2.2},
    {"ar": "بطاطس مسلوقه", "en": "Boiled Potato", "category": "Vegetables", "calories": 87, "protein": 1.9, "carbs": 20.0, "fats": 0.1, "fiber": 1.8},
    {"ar": "بطاطس مقلية", "en": "French Fries", "category": "Vegetables", "calories": 312, "protein": 3.4, "carbs": 41.0, "fats": 15.0, "fiber": 3.8},
    {"ar": "طماطم", "en": "Tomato", "category": "Vegetables", "calories": 18, "protein": 0.9, "carbs": 3.9, "fats": 0.2, "fiber": 1.2},
    {"ar": "طماطم كرز", "en": "Cherry Tomatoes", "category": "Vegetables", "calories": 18, "protein": 0.9, "carbs": 3.9, "fats": 0.2, "fiber": 1.2},
    {"ar": "خيار", "en": "Cucumber", "category": "Vegetables", "calories": 16, "protein": 0.7, "carbs": 3.6, "fats": 0.1, "fiber": 0.5},
    {"ar": "جزر", "en": "Carrot", "category": "Vegetables", "calories": 41, "protein": 0.9, "carbs": 10.0, "fats": 0.2, "fiber": 2.8},
    {"ar": "بصل", "en": "Onion", "category": "Vegetables", "calories": 40, "protein": 1.1, "carbs": 9.3, "fats": 0.1, "fiber": 1.7},
    {"ar": "ثوم", "en": "Garlic", "category": "Vegetables", "calories": 149, "protein": 6.4, "carbs": 33.0, "fats": 0.5, "fiber": 2.1},
    {"ar": "فلفل", "en": "Pepper", "category": "Vegetables", "calories": 31, "protein": 1.0, "carbs": 6.0, "fats": 0.3, "fiber": 2.1},
    {"ar": "فليفلة", "en": "Bell Pepper", "category": "Vegetables", "calories": 31, "protein": 1.0, "carbs": 6.0, "fats": 0.3, "fiber": 2.1},
    {"ar": "خس", "en": "Lettuce", "category": "Vegetables", "calories": 15, "protein": 1.4, "carbs": 2.9, "fats": 0.2, "fiber": 1.3},
    {"ar": "جرجير", "en": "Arugula", "category": "Vegetables", "calories": 25, "protein": 2.6, "carbs": 3.7, "fats": 0.7, "fiber": 1.6},
    {"ar": "بقدونس", "en": "Parsley", "category": "Vegetables", "calories": 36, "protein": 3.0, "carbs": 6.3, "fats": 0.8, "fiber": 3.3},
    {"ar": "كزبرة", "en": "Coriander", "category": "Vegetables", "calories": 23, "protein": 2.1, "carbs": 3.7, "fats": 0.5, "fiber": 2.8},
    {"ar": "باذنجان", "en": "Eggplant", "category": "Vegetables", "calories": 25, "protein": 1.0, "carbs": 6.0, "fats": 0.2, "fiber": 3.0},
    {"ar": "كوسه", "en": "Zucchini", "category": "Vegetables", "calories": 17, "protein": 1.2, "carbs": 3.1, "fats": 0.3, "fiber": 1.0},
    {"ar": "بروكلي", "en": "Broccoli", "category": "Vegetables", "calories": 35, "protein": 2.4, "carbs": 7.2, "fats": 0.4, "fiber": 2.6},
    {"ar": "قرنبيط", "en": "Cauliflower", "category": "Vegetables", "calories": 25, "protein": 1.9, "carbs": 5.0, "fats": 0.3, "fiber": 2.0},
    
    # ==================== FRUITS ====================
    {"ar": "تفاح", "en": "Apple", "category": "Fruits", "calories": 52, "protein": 0.3, "carbs": 14.0, "fats": 0.2, "fiber": 2.4},
    {"ar": "موز", "en": "Banana", "category": "Fruits", "calories": 89, "protein": 1.1, "carbs": 23.0, "fats": 0.3, "fiber": 2.6},
    {"ar": "عنب", "en": "Grapes", "category": "Fruits", "calories": 69, "protein": 0.7, "carbs": 18.0, "fats": 0.2, "fiber": 0.9},
    {"ar": "برتقال", "en": "Orange", "category": "Fruits", "calories": 47, "protein": 0.9, "carbs": 12.0, "fats": 0.1, "fiber": 2.4},
    {"ar": "ليمون", "en": "Lemon", "category": "Fruits", "calories": 29, "protein": 1.1, "carbs": 9.3, "fats": 0.3, "fiber": 2.8},
    {"ar": "مانجو", "en": "Mango", "category": "Fruits", "calories": 60, "protein": 0.8, "carbs": 15.0, "fats": 0.4, "fiber": 1.6},
    {"ar": "بطيخ", "en": "Watermelon", "category": "Fruits", "calories": 30, "protein": 0.6, "carbs": 7.5, "fats": 0.2, "fiber": 0.4},
    {"ar": "فراوله", "en": "Strawberry", "category": "Fruits", "calories": 32, "protein": 0.7, "carbs": 7.7, "fats": 0.3, "fiber": 2.0},
    {"ar": "عنب اسود", "en": "Black Grapes", "category": "Fruits", "calories": 72, "protein": 0.7, "carbs": 18.0, "fats": 0.2, "fiber": 1.0},
    {"ar": "تين", "en": "Fig", "category": "Fruits", "calories": 74, "protein": 0.8, "carbs": 19.0, "fats": 0.3, "fiber": 2.9},
    {"ar": "تمر", "en": "Dates", "category": "Fruits", "calories": 277, "protein": 1.8, "carbs": 75.0, "fats": 0.2, "fiber": 6.7},
    {"ar": "جميز", "en": "Sycamore Fig", "category": "Fruits", "calories": 58, "protein": 0.8, "carbs": 14.0, "fats": 0.1, "fiber": 2.0},
    
    # ==================== FATS & OILS ====================
    {"ar": "زيت زيتون", "en": "Olive Oil", "category": "Fats", "calories": 884, "protein": 0.0, "carbs": 0.0, "fats": 100.0, "fiber": 0.0},
    {"ar": "زيت ذرة", "en": "Corn Oil", "category": "Fats", "calories": 884, "protein": 0.0, "carbs": 0.0, "fats": 100.0, "fiber": 0.0},
    {"ar": "زيت عباد الشمس", "en": "Sunflower Oil", "category": "Fats", "calories": 884, "protein": 0.0, "carbs": 0.0, "fats": 100.0, "fiber": 0.0},
    {"ar": "زبت", "en": "Ghee", "category": "Fats", "calories": 900, "protein": 0.0, "carbs": 0.0, "fats": 100.0, "fiber": 0.0},
    {"ar": "زيت", "en": "Vegetable Oil", "category": "Fats", "calories": 884, "protein": 0.0, "carbs": 0.0, "fats": 100.0, "fiber": 0.0},
    {"ar": "زبت مكواه", "en": "Clarified Butter", "category": "Fats", "calories": 900, "protein": 0.0, "carbs": 0.0, "fats": 100.0, "fiber": 0.0},
    
    # ==================== NUTS & SEEDS ====================
    {"ar": "لوز", "en": "Almonds", "category": "Nuts", "calories": 579, "protein": 21.0, "carbs": 22.0, "fats": 50.0, "fiber": 12.0},
    {"ar": "فستق", "en": "Pistachio", "category": "Nuts", "calories": 560, "protein": 20.0, "carbs": 28.0, "fats": 45.0, "fiber": 10.0},
    {"ar": "كاجو", "en": "Cashews", "category": "Nuts", "calories": 553, "protein": 18.0, "carbs": 30.0, "fats": 44.0, "fiber": 3.0},
    {"ar": "جوز", "en": "Walnuts", "category": "Nuts", "calories": 654, "protein": 15.0, "carbs": 14.0, "fats": 65.0, "fiber": 7.0},
    {"ar": "سمسم", "en": "Sesame", "category": "Seeds", "calories": 573, "protein": 18.0, "carbs": 23.0, "fats": 50.0, "fiber": 12.0},
    {"ar": "طحينة", "en": "Tahini", "category": "Seeds", "calories": 595, "protein": 17.0, "carbs": 21.0, "fats": 54.0, "fiber": 9.0},
    {"ar": "صنوبر", "en": "Pine Nuts", "category": "Nuts", "calories": 673, "protein": 14.0, "carbs": 13.0, "fats": 68.0, "fiber": 3.7},
    
    # ==================== OTHER COMMON ====================
    {"ar": "عسل", "en": "Honey", "category": "Sweeteners", "calories": 304, "protein": 0.3, "carbs": 82.0, "fats": 0.0, "fiber": 0.2},
    {"ar": "سكر", "en": "Sugar", "category": "Sweeteners", "calories": 387, "protein": 0.0, "carbs": 100.0, "fats": 0.0, "fiber": 0.0},
]


def normalize_arabic(text: str) -> str:
    """Normalize Arabic text for search: أ/إ/ا -> ا, ة -> ه"""
    if not text:
        return text
    # Normalize alef variants
    text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
    # Normalize taa marbuta
    text = text.replace('ة', 'ه')
    return text


def get_food_by_arabic_name(arabic_name: str) -> dict | None:
    """Get food by Arabic name with normalization."""
    normalized = normalize_arabic(arabic_name)
    for food in EGYPTIAN_FOODS:
        if normalize_arabic(food["ar"]) == normalized:
            return food
    return None


def get_all_egyptian_foods() -> list[dict]:
    """Return all Egyptian foods with macros."""
    return EGYPTIAN_FOODS


# Alias for compatibility with older code/imports
EGYPTIAN_PRIORITY_FOODS = EGYPTIAN_FOODS

def search_foods(query: str, language: str = "auto") -> list[dict]:
    """Search priority foods by Arabic or English name."""
    query = normalize_arabic(query.lower().strip())
    results = []
    for food in EGYPTIAN_FOODS:
        if query in normalize_arabic(food["ar"].lower()) or query in food["en"].lower():
            results.append(food)
    return results

def translate_to_english(arabic_query: str) -> str:
    """Try to find an English equivalent for an Arabic food name."""
    food = get_food_by_arabic_name(arabic_query)
    return food["en"] if food else arabic_query

def get_foods_by_category(category: str) -> list[dict]:
    """Filter priority foods by category."""
    return [f for f in EGYPTIAN_FOODS if f["category"].lower() == category.lower()]

def get_all_priority_foods() -> list[dict]:
    """Return all priority foods."""
    return EGYPTIAN_FOODS
