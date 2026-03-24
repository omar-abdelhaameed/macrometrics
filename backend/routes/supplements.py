from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import date, datetime
from database import get_db
from models import User, SupplementCatalog, UserSupplementStack, DailySupplementLog
from auth import require_auth
from services.supplements import get_supplement_recommendations, get_supplement_by_category

router = APIRouter(prefix="/supplements", tags=["Supplements"])


# ==================== SCHEMAS ====================

class AddToStackRequest(BaseModel):
    supplement_id: int = Field(..., gt=0)
    custom_dosage_amount: float = Field(..., gt=0)
    time_of_day: Literal["morning", "afternoon", "evening", "pre_workout", "post_workout", "night", "with_meal", "before_sleep"] = "morning"
    notes: Optional[str] = None


class SupplementLogRequest(BaseModel):
    user_supplement_id: int = Field(..., gt=0)
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")


class SupplementCatalogOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    standard_dosage: float
    unit: str
    category: str
    target_goal: str
    benefits: Optional[str]

    class Config:
        from_attributes = True


class UserSupplementStackOut(BaseModel):
    id: int
    supplement: SupplementCatalogOut
    custom_dosage_amount: float
    time_of_day: str
    is_active: bool
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class DailyLogOut(BaseModel):
    id: int
    user_supplement_id: int
    date: date
    is_taken: bool
    taken_at: Optional[datetime]

    class Config:
        from_attributes = True


class SupplementWithStatus(BaseModel):
    """User supplement with today's taken status"""
    id: int
    supplement: SupplementCatalogOut
    custom_dosage_amount: float
    time_of_day: str
    is_active: bool
    notes: Optional[str]
    taken_today: bool


# ==================== ROUTES ====================

@router.get("/catalog")
def list_catalog(
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """Get all supplements in the catalog, optionally filtered by category."""
    return get_supplement_by_category(db, category)


@router.get("/recommendations")
def get_recommendations(
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """Get personalized supplement recommendations based on user profile."""
    return get_supplement_recommendations(db, user)


@router.get("/categories")
def list_categories(
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """List all supplement categories."""
    categories = db.query(SupplementCatalog.category).distinct().all()
    return {"categories": [c[0] for c in categories]}


# ==================== USER STACK ====================

@router.get("/my-stack", response_model=List[SupplementWithStatus])
def get_my_stack(
    date_param: Optional[str] = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """Get user's current supplement stack with today's status."""
    target_date = date.fromisoformat(date_param) if date_param else date.today()
    
    stack_items = db.query(UserSupplementStack).filter(
        UserSupplementStack.user_id == user.id,
        UserSupplementStack.is_active == True
    ).all()
    
    result = []
    for item in stack_items:
        # Check if taken today
        log = db.query(DailySupplementLog).filter(
            DailySupplementLog.user_supplement_id == item.id,
            DailySupplementLog.date == target_date
        ).first()
        
        result.append(SupplementWithStatus(
            id=item.id,
            supplement=item.supplement,
            custom_dosage_amount=item.custom_dosage_amount,
            time_of_day=item.time_of_day,
            is_active=item.is_active,
            notes=item.notes,
            taken_today=log.is_taken if log else False
        ))
    
    return result


@router.post("/my-stack", response_model=UserSupplementStackOut)
def add_to_stack(
    payload: AddToStackRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """Add a supplement to user's personal stack."""
    # Verify supplement exists
    supplement = db.query(SupplementCatalog).filter(
        SupplementCatalog.id == payload.supplement_id
    ).first()
    
    if not supplement:
        raise HTTPException(status_code=404, detail="Supplement not found in catalog")
    
    # Check if already in stack
    existing = db.query(UserSupplementStack).filter(
        UserSupplementStack.user_id == user.id,
        UserSupplementStack.supplement_id == payload.supplement_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=409, detail="Supplement already in your stack")
    
    stack_item = UserSupplementStack(
        user_id=user.id,
        supplement_id=payload.supplement_id,
        custom_dosage_amount=payload.custom_dosage_amount,
        time_of_day=payload.time_of_day,
        notes=payload.notes,
        is_active=True
    )
    
    db.add(stack_item)
    db.commit()
    db.refresh(stack_item)
    
    return stack_item


@router.delete("/my-stack/{stack_item_id}")
def remove_from_stack(
    stack_item_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """Remove a supplement from user's stack (soft delete)."""
    stack_item = db.query(UserSupplementStack).filter(
        UserSupplementStack.id == stack_item_id,
        UserSupplementStack.user_id == user.id
    ).first()
    
    if not stack_item:
        raise HTTPException(status_code=404, detail="Supplement not found in your stack")
    
    stack_item.is_active = False
    db.commit()
    
    return {"message": "Supplement removed from stack"}


# ==================== DAILY LOGGING ====================

@router.post("/log")
def log_supplement(
    payload: SupplementLogRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """Check off a supplement as taken for a specific date."""
    # Verify stack item exists and belongs to user
    stack_item = db.query(UserSupplementStack).filter(
        UserSupplementStack.id == payload.user_supplement_id,
        UserSupplementStack.user_id == user.id
    ).first()
    
    if not stack_item:
        raise HTTPException(status_code=404, detail="Supplement not in your stack")
    
    target_date = date.fromisoformat(payload.date)
    
    # Check if log exists for this date
    existing_log = db.query(DailySupplementLog).filter(
        DailySupplementLog.user_supplement_id == payload.user_supplement_id,
        DailySupplementLog.date == target_date
    ).first()
    
    if existing_log:
        # Toggle the status
        existing_log.is_taken = not existing_log.is_taken
        existing_log.taken_at = datetime.utcnow() if existing_log.is_taken else None
        db.commit()
        return {
            "message": "Supplement status updated",
            "is_taken": existing_log.is_taken
        }
    
    # Create new log
    new_log = DailySupplementLog(
        user_id=user.id,
        user_supplement_id=payload.user_supplement_id,
        date=target_date,
        is_taken=True,
        taken_at=datetime.utcnow()
    )
    
    db.add(new_log)
    db.commit()
    
    return {
        "message": "Supplement marked as taken",
        "is_taken": True
    }


@router.get("/log/history")
def get_log_history(
    days: int = 7,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """Get supplement log history for the last N days."""
    from datetime import timedelta
    start_date = date.today() - timedelta(days=days)
    
    logs = db.query(DailySupplementLog).filter(
        DailySupplementLog.user_id == user.id,
        DailySupplementLog.date >= start_date
    ).order_by(DailySupplementLog.date.desc()).all()
    
    # Group by date
    history_by_date = {}
    for log in logs:
        date_str = log.date.isoformat()
        if date_str not in history_by_date:
            history_by_date[date_str] = []
        history_by_date[date_str].append({
            "id": log.id,
            "supplement_id": log.user_supplement_id,
            "is_taken": log.is_taken,
            "taken_at": log.taken_at.isoformat() if log.taken_at else None
        })
    
    return history_by_date
