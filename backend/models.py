from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Date, DateTime,
    ForeignKey, Text
)
from sqlalchemy.orm import relationship
from database import Base
import enum
from datetime import datetime


class MealType(str, enum.Enum):
    breakfast    = "breakfast"
    lunch        = "lunch"
    dinner       = "dinner"
    snack        = "snack"
    post_workout = "post_workout"
    pre_workout  = "pre_workout"


# ── Users ─────────────────────────────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id                    = Column(Integer, primary_key=True, index=True)
    name                  = Column(String(100), nullable=False)
    email                 = Column(String(255), unique=True, nullable=False)
    password_hash         = Column(String(255), nullable=False)
    age                   = Column(Integer, nullable=True)
    gender                = Column(String(20), nullable=True)
    daily_calorie_target  = Column(Integer, default=2800)
    protein_target_g      = Column(Float, default=220.0)
    carbs_target_g        = Column(Float, default=300.0)
    fats_target_g         = Column(Float, default=80.0)
    goal_weight_lbs       = Column(Float, nullable=True)
    current_weight_lbs    = Column(Float, nullable=True)
    height_cm             = Column(Float, nullable=True)
    body_fat_pct          = Column(Float, nullable=True)
    activity_level        = Column(String(50), default="moderate")
    primary_goal          = Column(String(50), default="maintain")
    preferred_unit        = Column(String(20), default="metric")
    theme_mode            = Column(String(20), default="dark")
    theme_accent          = Column(String(30), default="green")
    created_at            = Column(DateTime, default=datetime.utcnow)
    is_pro_user           = Column(Boolean, default=False)
    stripe_customer_id    = Column(String(100), nullable=True)
    subscription_end_date = Column(DateTime, nullable=True)

    daily_logs       = relationship("DailyLog",           back_populates="user", cascade="all, delete-orphan")
    chat_history     = relationship("ChatHistory",         back_populates="user", cascade="all, delete-orphan")
    supplement_stack = relationship("UserSupplementStack", back_populates="user", cascade="all, delete-orphan")
    supplement_logs  = relationship("DailySupplementLog",  back_populates="user", cascade="all, delete-orphan")


# ── Ingredients ───────────────────────────────────────────────────────────────
class Ingredient(Base):
    __tablename__ = "ingredients"

    id                  = Column(Integer, primary_key=True, index=True)
    name                = Column(String(200), nullable=False, index=True)
    name_ar             = Column(String(200), nullable=True,  index=True)
    category            = Column(String(100), nullable=False)
    calories_per_100g   = Column(Float, nullable=False)
    protein_per_100g    = Column(Float, nullable=False)
    carbs_per_100g      = Column(Float, nullable=False)
    fats_per_100g       = Column(Float, nullable=False)
    fiber_per_100g      = Column(Float, default=0.0)
    sugar_per_100g      = Column(Float, default=0.0)
    sodium_mg_per_100g  = Column(Float, default=0.0)
    is_golden           = Column(Boolean, default=False, index=True)
    popularity_score    = Column(Float,   default=1.0,   index=True)
    source              = Column(String(100), default="USDA")
    fdc_id              = Column(String(50),  nullable=True, index=True)
    serving_description = Column(String(200), nullable=True)
    user_id             = Column(Integer, ForeignKey("users.id"), nullable=True)

    meal_ingredients = relationship("MealIngredient", back_populates="ingredient")


# ── Daily Logs ────────────────────────────────────────────────────────────────
class DailyLog(Base):
    __tablename__ = "daily_logs"

    id                      = Column(Integer, primary_key=True, index=True)
    user_id                 = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    date                    = Column(Date,    nullable=False, index=True)
    weight_lbs              = Column(Float,   nullable=True)
    is_refeed_day           = Column(Boolean, default=False, index=True)
    is_rest_day             = Column(Boolean, default=False)
    notes                   = Column(Text,    nullable=True)
    calorie_target_override = Column(Integer, nullable=True)
    protein_target_override = Column(Float,   nullable=True)
    carbs_target_override   = Column(Float,   nullable=True)
    fats_target_override    = Column(Float,   nullable=True)

    user  = relationship("User", back_populates="daily_logs")
    meals = relationship("Meal", back_populates="daily_log", cascade="all, delete-orphan")


class Meal(Base):
    __tablename__ = "meals"

    id           = Column(Integer,   primary_key=True, index=True)
    daily_log_id = Column(Integer,   ForeignKey("daily_logs.id"), nullable=False, index=True)
    meal_type    = Column(String(50), nullable=False, default="lunch", index=True)
    time_logged  = Column(DateTime,  default=datetime.utcnow, index=True)
    notes        = Column(Text,      nullable=True)

    daily_log        = relationship("DailyLog",       back_populates="meals")
    meal_ingredients = relationship("MealIngredient", back_populates="meal", cascade="all, delete-orphan")


class MealIngredient(Base):
    __tablename__ = "meal_ingredients"

    id             = Column(Integer, primary_key=True, index=True)
    meal_id        = Column(Integer, ForeignKey("meals.id"),       nullable=False)
    ingredient_id  = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    serving_size_g = Column(Float,   nullable=False, default=100.0)

    meal       = relationship("Meal",       back_populates="meal_ingredients")
    ingredient = relationship("Ingredient", back_populates="meal_ingredients")


# ── Supplements (legacy) ──────────────────────────────────────────────────────
class Supplement(Base):
    __tablename__ = "supplements"

    id                 = Column(Integer, primary_key=True, index=True)
    name               = Column(String(100), nullable=False)
    default_daily_dose = Column(String(50),  nullable=False)
    category           = Column(String(50),  nullable=False)
    is_global          = Column(Boolean, default=True)


class UserSupplement(Base):
    __tablename__ = "user_supplements"

    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    supplement_name = Column(String(100), nullable=False)
    dosage          = Column(Float,       nullable=False)
    unit            = Column(String(20),  nullable=False)
    is_active       = Column(Boolean, default=True, index=True)
    created_at      = Column(DateTime, default=datetime.utcnow)


# ── NEW: Supplement Catalog + Stack + Daily Log ───────────────────────────────
class SupplementCatalog(Base):
    __tablename__ = "supplement_catalog"

    id                       = Column(Integer,    primary_key=True, index=True)
    name                     = Column(String(150), nullable=False, unique=True, index=True)
    description              = Column(Text,        nullable=True)
    standard_dosage          = Column(Float,       nullable=False)
    unit                     = Column(String(30),  nullable=False)
    category                 = Column(String(80),  nullable=False, index=True)
    target_goal              = Column(String(50),  nullable=False, default="all")
    benefits                 = Column(Text,        nullable=True)
    recommended_for_activity = Column(String(50),  nullable=True, default="all")

    user_stacks = relationship("UserSupplementStack", back_populates="supplement")


class UserSupplementStack(Base):
    __tablename__ = "user_supplement_stack"

    id                   = Column(Integer,   primary_key=True, index=True)
    user_id              = Column(Integer,   ForeignKey("users.id"),             nullable=False, index=True)
    supplement_id        = Column(Integer,   ForeignKey("supplement_catalog.id"), nullable=False)
    custom_dosage_amount = Column(Float,     nullable=False)
    time_of_day          = Column(String(30), nullable=False, default="morning")
    is_active            = Column(Boolean,   default=True, index=True)
    notes                = Column(Text,      nullable=True)
    created_at           = Column(DateTime,  default=datetime.utcnow)

    user       = relationship("User",              back_populates="supplement_stack")
    supplement = relationship("SupplementCatalog", back_populates="user_stacks")
    daily_logs = relationship("DailySupplementLog", back_populates="stack_item", cascade="all, delete-orphan")


class DailySupplementLog(Base):
    __tablename__ = "daily_supplement_log"

    id                 = Column(Integer,  primary_key=True, index=True)
    user_id            = Column(Integer,  ForeignKey("users.id"),                nullable=False, index=True)
    user_supplement_id = Column(Integer,  ForeignKey("user_supplement_stack.id"), nullable=False, index=True)
    date               = Column(Date,     nullable=False, index=True)
    is_taken           = Column(Boolean,  default=False)
    taken_at           = Column(DateTime, nullable=True)

    user       = relationship("User",                back_populates="supplement_logs")
    stack_item = relationship("UserSupplementStack", back_populates="daily_logs")


# ── Chat Memory ───────────────────────────────────────────────────────────────
class ChatHistory(Base):
    __tablename__ = "chat_history"

    id         = Column(Integer,    primary_key=True, index=True)
    user_id    = Column(Integer,    ForeignKey("users.id"), nullable=False, index=True)
    role       = Column(String(20), nullable=False)
    content    = Column(Text,       nullable=False)
    created_at = Column(DateTime,   default=datetime.utcnow)

    user = relationship("User", back_populates="chat_history")
