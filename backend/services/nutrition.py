def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """Calculate BMR using the Mifflin-St Jeor equation."""
    # Base calculation
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)
    
    # Gender adjustment
    if gender and gender.lower() == 'female':
        bmr -= 161
    else:  # Default to male math
        bmr += 5
        
    return bmr

def calculate_tdee(bmr: float, activity_level: str) -> float:
    """Calculate TDEE based on BMR and activity multipliers."""
    multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725
    }
    # Map input text (which might be human readable) to our keys safely
    al = activity_level.lower()
    if 'sedentary' in al:
        mult = multipliers['sedentary']
    elif 'light' in al:
        mult = multipliers['light']
    elif 'active' in al and 'very' not in al:
        mult = multipliers['active']
    elif 'moderate' in al:
        mult = multipliers['moderate']
    else:
        mult = multipliers['moderate'] # Fallback
        
    return bmr * mult

def calculate_macros(weight_kg: float, height_cm: float, age: int, gender: str, activity_level: str, primary_goal: str) -> dict:
    """
    Complete engine to calculate optimal daily macro targets.
    Expected primary_goal: 'cut', 'maintain', 'bulk'
    """
    bmr = calculate_bmr(weight_kg, height_cm, age, gender)
    tdee = calculate_tdee(bmr, activity_level)
    
    # Goal Adjustments
    goal = primary_goal.lower()
    if 'cut' in goal or 'lose' in goal:
        target_calories = tdee - 500
    elif 'bulk' in goal or 'gain' in goal:
        target_calories = tdee + 300
    else:
        target_calories = tdee
        
    # Ensure calories don't drop dangerously low
    target_calories = max(1200, round(target_calories))
    
    # Bodybuilder standard macro distribution
    # Protein: 2.2g per kg of body weight
    protein_g = round(weight_kg * 2.2)
    protein_cals = protein_g * 4
    
    # Fats: 25% of total adjusted calories (9 kcal/g)
    fat_cals = target_calories * 0.25
    fat_g = round(fat_cals / 9)
    
    # Carbs: The remaining calories (4 kcal/g)
    remaining_cals = target_calories - protein_cals - fat_cals
    carb_g = round(max(0, remaining_cals) / 4)
    
    return {
        "daily_calorie_target": target_calories,
        "protein_target_g": float(protein_g),
        "carbs_target_g": float(carb_g),
        "fats_target_g": float(fat_g)
    }
