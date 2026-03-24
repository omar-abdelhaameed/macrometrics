from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from database import get_db
from models import User
from auth import hash_password, verify_password, create_access_token
from services.nutrition import calculate_macros
from rate_limiter import limiter

router = APIRouter(prefix="/auth", tags=["Authentication"])


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    age: Optional[int] = Field(None, ge=10, le=120)
    gender: Optional[Literal["male", "female", "other"]] = None
    current_weight_lbs: Optional[float] = Field(None, ge=30, le=700)
    height_cm: Optional[float] = Field(None, ge=50, le=300)
    activity_level: Literal["sedentary", "light", "moderate", "active", "very_active"] = "moderate"
    preferred_unit: Literal["metric", "imperial"] = "metric"
    primary_goal: Literal["cut", "maintain", "bulk"] = "maintain"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


@router.post("/register", response_model=AuthResponse, status_code=201)
@limiter.limit("5/minute")
def register(request: Request, payload: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user with full onboarding data."""
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    # Calculate optimal macros
    macros = calculate_macros(
        weight_kg=payload.current_weight_lbs / 2.20462 if payload.current_weight_lbs else 75,
        height_cm=payload.height_cm or 170,
        age=payload.age or 30,
        gender=payload.gender or 'male',
        activity_level=payload.activity_level,
        primary_goal=payload.primary_goal
    )

    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        age=payload.age,
        gender=payload.gender,
        current_weight_lbs=payload.current_weight_lbs,
        height_cm=payload.height_cm,
        activity_level=payload.activity_level,
        primary_goal=payload.primary_goal,
        preferred_unit=payload.preferred_unit,
        daily_calorie_target=macros["daily_calorie_target"],
        protein_target_g=macros["protein_target_g"],
        carbs_target_g=macros["carbs_target_g"],
        fats_target_g=macros["fats_target_g"],
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(data={"sub": str(user.id)})
    return AuthResponse(
        access_token=token,
        user=_user_dict(user),
    )


@router.post("/login", response_model=AuthResponse)
@limiter.limit("5/minute")
def login(request: Request, payload: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate and return a JWT."""
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(data={"sub": str(user.id)})
    return AuthResponse(
        access_token=token,
        user=_user_dict(user),
    )


def _user_dict(user: User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "gender": user.gender,
        "daily_calorie_target": user.daily_calorie_target,
        "protein_target_g": user.protein_target_g,
        "carbs_target_g": user.carbs_target_g,
        "fats_target_g": user.fats_target_g,
        "theme_mode": user.theme_mode,
        "theme_accent": user.theme_accent,
        "current_weight_lbs": user.current_weight_lbs,
        "goal_weight_lbs": user.goal_weight_lbs,
        "height_cm": user.height_cm,
        "activity_level": user.activity_level,
        "primary_goal": user.primary_goal,
        "preferred_unit": user.preferred_unit,
        "is_pro_user": getattr(user, "is_pro_user", False),
    }
