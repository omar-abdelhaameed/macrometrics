from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel, Field
from typing import List, Optional
from database import get_db
from models import User, Ingredient, Meal, DailyLog, MealIngredient, ChatHistory
from auth import require_auth
from datetime import date, datetime, timedelta
from rate_limiter import limiter
import os
import httpx

router = APIRouter(prefix="/chat", tags=["Chat"])


# ==================== SCHEMAS ====================

class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_history: Optional[List[dict]] = Field(default_factory=list, max_length=20)


class ChatResponse(BaseModel):
    response: str
    meal_suggestions: Optional[List[dict]] = None
    user_context: Optional[dict] = None


# ==================== AI CONFIG ====================
# Strategy:
#   Primary  → Gemini 2.5 Flash (250 req/day free) — always, no routing
#   Fallback → Groq Llama-3 (1000 req/day free)    — auto when Gemini hits 429

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GROQ_API_KEY   = os.environ.get("GROQ_API_KEY", "")

_GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
FLASH_URL    = f"{_GEMINI_BASE}/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

_GROQ_URL   = "https://api.groq.com/openai/v1/chat/completions"
_GROQ_MODEL = "llama-3.3-70b-versatile"   # 1000 req/day free


# ==================== CONTEXT BUILDERS ====================

def get_user_macro_context(user: User, db: Session) -> dict:
    from routes.analytics import check_weight_plateau  # Direct import to reuse logic
    
    today     = date.today()
    daily_log = db.query(DailyLog).filter(
        DailyLog.user_id == user.id, DailyLog.date == today
    ).first()

    c = {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fats": 0.0}
    if daily_log:
        for meal in daily_log.meals:
            for mi in meal.meal_ingredients:
                f = mi.serving_size_g / 100.0
                c["calories"] += mi.ingredient.calories_per_100g * f
                c["protein"]  += mi.ingredient.protein_per_100g  * f
                c["carbs"]    += mi.ingredient.carbs_per_100g    * f
                c["fats"]     += mi.ingredient.fats_per_100g     * f

    def _b(key, target):
        consumed = round(c[key]); t = target or 0
        return {"target": t, "consumed": consumed, "remaining": round(t - consumed)}

    plateau_data = check_weight_plateau(7, db, user)

    return {
        "calories":       _b("calories", user.daily_calorie_target),
        "protein":        _b("protein",  user.protein_target_g),
        "carbs":          _b("carbs",    user.carbs_target_g),
        "fats":           _b("fats",     user.fats_target_g),
        "goal":           user.primary_goal,
        "activity_level": user.activity_level,
        "plateau_status": plateau_data
    }


def get_7day_summary(user: User, db: Session) -> str:
    today = date.today()
    rows  = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        log = db.query(DailyLog).filter(
            DailyLog.user_id == user.id, DailyLog.date == day
        ).first()
        if not log:
            rows.append(f"  {day}: no data"); continue
        cal = pro = 0.0
        for meal in log.meals:
            for mi in meal.meal_ingredients:
                f    = mi.serving_size_g / 100.0
                cal += mi.ingredient.calories_per_100g * f
                pro += mi.ingredient.protein_per_100g  * f
        w      = f"{log.weight_lbs} lbs" if log.weight_lbs else "—"
        flags  = (" [REFEED]" if log.is_refeed_day else "") + (" [REST]" if log.is_rest_day else "")
        rows.append(f"  {day}: {round(cal)} kcal | {round(pro)}g protein | weight {w}{flags}")
    return "\n".join(rows)


def get_db_history(user_id: int, db: Session, limit: int = 10) -> List[dict]:
    rows = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(desc(ChatHistory.created_at))
        .limit(limit).all()
    )
    return [{"role": r.role, "content": r.content} for r in reversed(rows)]


def save_turn(user_id: int, role: str, content: str, db: Session):
    db.add(ChatHistory(user_id=user_id, role=role, content=content))
    db.commit()
    total = db.query(ChatHistory).filter(ChatHistory.user_id == user_id).count()
    if total > 50:
        oldest = (
            db.query(ChatHistory).filter(ChatHistory.user_id == user_id)
            .order_by(ChatHistory.created_at).limit(total - 50).all()
        )
        for row in oldest: db.delete(row)
        db.commit()


# ==================== MEAL HELPERS ====================

def find_meal_alternatives_from_db(db: Session, user_id: int, original_calories: float = 300) -> List[dict]:
    cal_min = original_calories * 0.9
    cal_max = original_calories * 1.1
    ingredients = db.query(Ingredient).filter(
        Ingredient.calories_per_100g >= cal_min * 10,
        Ingredient.calories_per_100g <= cal_max * 10,
    ).limit(10).all()
    suggestions = []
    for alt in ingredients:
        serving = 100
        for i in range(50, 200, 10):
            cal = alt.calories_per_100g * (i / 100.0)
            if cal_min <= cal <= cal_max:
                serving = i; break
        suggestions.append({
            "id": alt.id, "name": alt.name, "category": alt.category,
            "serving_size_g": serving,
            "calories": round(alt.calories_per_100g * (serving / 100.0), 1),
            "protein":  round(alt.protein_per_100g  * (serving / 100.0), 1),
            "carbs":    round(alt.carbs_per_100g    * (serving / 100.0), 1),
            "fats":     round(alt.fats_per_100g     * (serving / 100.0), 1),
        })
    return suggestions


def find_meal_alternatives(original_meal_id: int, db: Session) -> List[dict]:
    meal = db.query(Meal).filter(Meal.id == original_meal_id).first()
    if not meal: return []
    def _total(attr):
        return sum(getattr(mi.ingredient, attr) * (mi.serving_size_g / 100.0) for mi in meal.meal_ingredients)
    orig_cal  = _total("calories_per_100g")
    orig_prot = _total("protein_per_100g")
    alts = db.query(Ingredient).filter(
        Ingredient.calories_per_100g.between(orig_cal * 0.9, orig_cal * 1.1),
        Ingredient.protein_per_100g.between(orig_prot * 0.9, orig_prot * 1.1),
    ).limit(5).all()
    return [{"id": a.id, "name": a.name, "calories": round(a.calories_per_100g),
             "protein": round(a.protein_per_100g), "carbs": round(a.carbs_per_100g),
             "fats": round(a.fats_per_100g)} for a in alts]


# ==================== MAIN AI FUNCTION ====================

async def generate_ai_response(
    user: User, user_message: str, context: dict, history: List[dict], db: Session
) -> tuple[str, Optional[List[dict]]]:

    if not GEMINI_API_KEY:
        return _rule_based(user_message, context, db)

    cal_t = context["calories"]["target"];   cal_c = context["calories"]["consumed"]
    cal_r = context["calories"]["remaining"]; p_t  = context["protein"]["target"]
    p_c   = context["protein"]["consumed"];   p_r  = context["protein"]["remaining"]
    c_t   = context["carbs"]["target"];       c_c  = context["carbs"]["consumed"]
    f_t   = context["fats"]["target"];        f_c  = context["fats"]["consumed"]
    goal  = context["goal"];                  act  = context["activity_level"]
    plateau = context["plateau_status"]
    week  = get_7day_summary(user, db)
    name  = user.name.split()[0] if user.name else "champ"

    is_pro = getattr(user, "is_pro_user", False)
    tier_label = "PRO TIER (UNLIMITED)" if is_pro else "FREE TIER (GATED)"

    plateau_text = ""
    if is_pro:
        plateau_text = f"\n[!] PRO-TIER ALERT: {plateau['suggestion']}" if plateau.get("is_plateau") else "\n[✓] Weight trend is normal. No plateau detected."
    else:
        plateau_text = "\n[!] FREE TIER: Plateau analysis is restricted. Keep feedback basic."

    system = f"""You are Coach AI — an elite bilingual (Arabic & English) nutrition and
bodybuilding coach inside MacroMetrics, a premium SaaS fitness app.

=== CLIENT SUBSCRIPTION ===
Tier    : {tier_label}
Name    : {name}
Goal    : {goal.upper()}
Activity: {act}

=== TODAY'S MACROS ===
Calories : {cal_c} / {cal_t} kcal  ({cal_r} remaining)
Protein  : {p_c} / {p_t} g         ({p_r} g remaining)
Carbs    : {c_c} / {c_t} g
Fats     : {f_c} / {f_t} g

=== LAST 7 DAYS ===
{week}

=== LIFETIME DIAGNOSTICS ==={plateau_text}

=== SAAS RULES ===
1. Reply in the SAME language as the user (Arabic → Arabic, English → English).
2. Use the client's first name ({name}) for a premium feel.
3. {f"PRO-TIER NEGOTIATION: Highly proactive. Negotiate macros for refeed days/plateaus using science." if is_pro else "FREE-TIER LIMITS: Keep it very basic. If the user asks for deep analysis or plans, kindly suggest upgrading to the Pro plan for elite coaching features."}
4. Be motivating and concise.
5. Max 250 words."""

    contents = []
    for turn in history[-8:]:
        role = "user" if turn["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": turn["content"]}]})
    contents.append({"role": "user", "parts": [{"text": user_message}]})

    swap_kw = ["swap","replace","alternative","بديل","تغيير","بدل"]

    # ── 1. Try Gemini 2.5 Flash ──────────────────────────────────────────
    if GEMINI_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(FLASH_URL, json={
                    "system_instruction": {"parts": [{"text": system}]},
                    "contents": contents,
                    "generationConfig": {"temperature": 0.75, "maxOutputTokens": 500},
                })

            if resp.status_code == 200:
                data    = resp.json()
                ai_text = (
                    data.get("candidates", [{}])[0]
                    .get("content", {}).get("parts", [{}])[0]
                    .get("text", "").strip()
                )
                if ai_text:
                    suggestions = None
                    if any(kw in user_message.lower() for kw in swap_kw):
                        suggestions = find_meal_alternatives_from_db(db, user.id, cal_c or 300)
                    return ai_text, suggestions

            elif resp.status_code == 429:
                print("Gemini quota hit (429) — switching to Groq fallback.")
            else:
                print(f"Gemini error {resp.status_code}: {resp.text[:200]}")

        except Exception as exc:
            print(f"Gemini call failed: {exc}")

    # ── 2. Fallback → Groq Llama-3 (1000 req/day free) ───────────────────
    if GROQ_API_KEY:
        try:
            groq_messages = [{"role": "system", "content": system}]
            for turn in history[-8:]:
                groq_messages.append({"role": turn["role"], "content": turn["content"]})
            groq_messages.append({"role": "user", "content": user_message})

            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    _GROQ_URL,
                    headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                    json={"model": _GROQ_MODEL, "messages": groq_messages, "max_tokens": 500, "temperature": 0.75},
                )

            if resp.status_code == 200:
                ai_text = resp.json()["choices"][0]["message"]["content"].strip()
                if ai_text:
                    suggestions = None
                    if any(kw in user_message.lower() for kw in swap_kw):
                        suggestions = find_meal_alternatives_from_db(db, user.id, cal_c or 300)
                    return ai_text, suggestions
            else:
                print(f"Groq error {resp.status_code}: {resp.text[:200]}")

        except Exception as exc:
            print(f"Groq call failed: {exc}")

    # ── 3. Final fallback → rule-based ────────────────────────────────────
    return _rule_based(user_message, context, db)


# ==================== RULE-BASED FALLBACK ====================

def _rule_based(user_message: str, context: dict, db: Session) -> tuple[str, Optional[List[dict]]]:
    msg   = user_message.lower()
    ar    = any('\u0600' <= c <= '\u06FF' for c in user_message)
    cal_t = context["calories"]["target"];    cal_c = context["calories"]["consumed"]
    cal_r = context["calories"]["remaining"]; p_t   = context["protein"]["target"]
    p_c   = context["protein"]["consumed"];   p_r   = context["protein"]["remaining"]

    if any(kw in msg for kw in ["swap","replace","بديل","تغيير","بدل","alternative"]):
        alts = find_meal_alternatives_from_db(db, 0, cal_c or 300)
        if alts:
            txt = ("🔥 **بدالات مناسبة:**\n" + "\n".join(
                f"• {a['name']} ({a['serving_size_g']}g): {a['calories']} سعرة | {a['protein']}g بروتين"
                for a in alts[:5]
            ) if ar else "🔥 **Smart alternatives:**\n" + "\n".join(
                f"• {a['name']} ({a['serving_size_g']}g): {a['calories']} cal | {a['protein']}g protein"
                for a in alts[:5]
            ))
            return txt, alts[:5]

    if "بروتين" in msg or "protein" in msg:
        return ((f"💪 بروتين: {p_c}/{p_t}g | متبقي {p_r}g" if ar
                 else f"💪 Protein: {p_c}/{p_t}g | {p_r}g remaining"), None)

    if any(kw in msg for kw in ["hello","hi","hey","مرحبا","اهلا","هاي"]):
        return ((f"👋 مرحباً! سعراتك: {cal_c}/{cal_t} | بروتين: {p_c}/{p_t}g 💪" if ar
                 else f"👋 Hey! Calories: {cal_c}/{cal_t} | Protein: {p_c}/{p_t}g 💪"), None)

    return ((f"🔥 اليوم: {cal_c}/{cal_t} سعرة | متبقي {cal_r} 💪" if ar
             else f"🔥 Today: {cal_c}/{cal_t} cal | {cal_r} remaining 💪"), None)


# ==================== ROUTES ====================

@router.post("", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat(
    request: Request,
    payload: ChatMessage,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    context = get_user_macro_context(user, db)
    context["user_id"] = user.id

    history = get_db_history(user.id, db, limit=10)
    save_turn(user.id, "user", payload.message, db)

    response_text, suggestions = await generate_ai_response(
        user, payload.message, context, history, db
    )

    save_turn(user.id, "assistant", response_text, db)

    return ChatResponse(
        response=response_text,
        meal_suggestions=suggestions,
        user_context={
            "calories_remaining": context["calories"]["remaining"],
            "protein_remaining":  context["protein"]["remaining"],
            "goal":               context["goal"],
        },
    )


@router.get("/context")
def get_chat_context(
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    context = get_user_macro_context(user, db)
    recent_meals = (
        db.query(Meal).join(DailyLog)
        .filter(DailyLog.user_id == user.id)
        .order_by(Meal.time_logged.desc()).limit(5).all()
    )
    context["recent_meals"] = [
        {
            "id": m.id, "meal_type": m.meal_type,
            "time_logged": m.time_logged.isoformat() if m.time_logged else None,
            "total_calories": round(sum(
                mi.ingredient.calories_per_100g * (mi.serving_size_g / 100.0)
                for mi in m.meal_ingredients
            )),
        }
        for m in recent_meals
    ]
    return context


@router.delete("/history")
def clear_chat_history(
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    """Wipe the user's chat memory."""
    db.query(ChatHistory).filter(ChatHistory.user_id == user.id).delete()
    db.commit()
    return {"message": "Chat history cleared"}


@router.post("/swap/{meal_id}")
def swap_meal(
    meal_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_auth),
):
    alts = find_meal_alternatives(meal_id, db)
    if not alts:
        raise HTTPException(status_code=404, detail="No alternatives found")
    return {"alternatives": alts}