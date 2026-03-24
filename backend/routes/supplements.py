from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from database import get_db
from models import User
from auth import require_auth

router = APIRouter(prefix="/supplements", tags=["Supplements"])


class SupplementBase(BaseModel):
    name: str
    default_daily_dose: str
    category: str


class SupplementOut(SupplementBase):
    id: int

    class Config:
        from_attributes = True


class UserSupplementBase(BaseModel):
    supplement_id: int
    is_active: bool = True
    notes: Optional[str] = None


class UserSupplementOut(UserSupplementBase):
    id: int
    supplement: SupplementOut
    last_taken: Optional[date] = None
    taken_today: bool = False

    class Config:
        from_attributes = True


SUPPLEMENT_DB = [
    {"id": 1, "name": "Creatine Monohydrate", "default_daily_dose": "5g", "category": "Performance"},
    {"id": 2, "name": "Whey Protein", "default_daily_dose": "25-50g", "category": "Protein"},
    {"id": 3, "name": "Vitamin D3", "default_daily_dose": "2000-5000 IU", "category": "Vitamins"},
    {"id": 4, "name": "Omega-3 Fish Oil", "default_daily_dose": "2-3g", "category": "Healthy Fats"},
    {"id": 5, "name": "Magnesium", "default_daily_dose": "200-400mg", "category": "Minerals"},
    {"id": 6, "name": "Zinc", "default_daily_dose": "15-30mg", "category": "Minerals"},
    {"id": 7, "name": "Multivitamin", "default_daily_dose": "1 tablet", "category": "Vitamins"},
    {"id": 8, "name": "Casein Protein", "default_daily_dose": "25g", "category": "Protein"},
    {"id": 9, "name": "BCAAs", "default_daily_dose": "5-10g", "category": "Amino Acids"},
    {"id": 10, "name": "Pre-Workout", "default_daily_dose": "1 serving", "category": "Performance"},
]


_supplement_store = {s["id"]: s for s in SUPPLEMENT_DB}


@router.get("", response_model=List[SupplementOut])
def list_supplements(
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """List available supplements, optionally filtered by category."""
    supplements = list(_supplement_store.values())
    if category:
        supplements = [s for s in supplements if s["category"].lower() == category.lower()]
    return supplements


@router.get("/{supplement_id}", response_model=SupplementOut)
def get_supplement(
    supplement_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """Get a specific supplement by ID."""
    if supplement_id not in _supplement_store:
        raise HTTPException(status_code=404, detail="Supplement not found")
    return _supplement_store[supplement_id]


@router.get("/categories")
def list_categories(
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """List all supplement categories."""
    categories = list(set(s["category"] for s in _supplement_store.values()))
    return {"categories": categories}