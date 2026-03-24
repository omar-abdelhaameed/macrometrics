from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserOut, UserUpdate
from auth import require_auth
from services.nutrition import calculate_macros

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserOut)
def get_current_profile(user: User = Depends(require_auth)):
    """Get the authenticated user's profile."""
    return user


@router.put("/me", response_model=UserOut)
def update_current_profile(
    payload: UserUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """Update the authenticated user's profile and targets."""
    update_data = payload.model_dump(exclude_unset=True)
    
    # Track if a recalculation metric was changed
    needs_recalc = any(
        k in update_data for k in 
        ["current_weight_lbs", "height_cm", "age", "gender", "activity_level", "primary_goal"]
    )
    
    for field, value in update_data.items():
        setattr(user, field, value)

    # Recalculate targets if necessary
    if needs_recalc:
        macros = calculate_macros(
            weight_kg=(user.current_weight_lbs / 2.20462) if user.current_weight_lbs else 75.0,
            height_cm=user.height_cm or 170.0,
            age=user.age or 30,
            gender=user.gender or 'male',
            activity_level=user.activity_level,
            primary_goal=user.primary_goal
        )
        user.daily_calorie_target = macros["daily_calorie_target"]
        user.protein_target_g = macros["protein_target_g"]
        user.carbs_target_g = macros["carbs_target_g"]
        user.fats_target_g = macros["fats_target_g"]

    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user profile by ID (public)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
