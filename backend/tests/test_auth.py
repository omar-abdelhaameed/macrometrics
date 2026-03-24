import pytest
from pydantic import BaseModel, EmailStr, Field, ValidationError
from typing import Literal, Optional


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


class TestRegisterRequest:
    def test_valid_registration(self):
        req = RegisterRequest(
            name="John Doe",
            email="john@example.com",
            password="securepass123",
            activity_level="moderate",
            preferred_unit="metric",
            primary_goal="maintain"
        )
        assert req.name == "John Doe"
        assert req.email == "john@example.com"

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            RegisterRequest(
                name="John",
                email="invalid-email",
                password="password123",
                activity_level="moderate",
                preferred_unit="metric",
                primary_goal="maintain"
            )

    def test_password_too_short(self):
        with pytest.raises(ValidationError):
            RegisterRequest(
                name="John",
                email="john@example.com",
                password="short",
                activity_level="moderate",
                preferred_unit="metric",
                primary_goal="maintain"
            )

    def test_invalid_age_range(self):
        with pytest.raises(ValidationError):
            RegisterRequest(
                name="John",
                email="john@example.com",
                password="password123",
                age=5,
                activity_level="moderate",
                preferred_unit="metric",
                primary_goal="maintain"
            )


class TestLoginRequest:
    def test_valid_login(self):
        req = LoginRequest(
            email="user@example.com",
            password="password123"
        )
        assert req.email == "user@example.com"

    def test_invalid_login_email(self):
        with pytest.raises(ValidationError):
            LoginRequest(
                email="not-an-email",
                password="password"
            )
