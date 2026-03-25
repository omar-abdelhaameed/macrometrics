from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import logging
import os

load_dotenv() 

from database import engine, Base, SessionLocal
from routes import ingredients, meals, daily, users, auth, analytics, chat, supplements
from rate_limiter import limiter

logger = logging.getLogger("macrometrics")


# ==================== SEED HELPERS ====================

def _seed_supplements(db):
    from models import SupplementCatalog
    CATALOG = [
        {"name": "Whey Protein Isolate",            "description": "Fast-absorbing protein for muscle recovery.",          "standard_dosage": 30.0,   "unit": "g",       "category": "Protein",      "target_goal": "bulk",     "benefits": "Complete amino acid profile, supports muscle protein synthesis", "recommended_for_activity": "active"},
        {"name": "Casein Protein",                  "description": "Slow-digesting protein ideal for nighttime use.",      "standard_dosage": 30.0,   "unit": "g",       "category": "Protein",      "target_goal": "maintain", "benefits": "Slow absorption, prevents muscle breakdown during sleep",       "recommended_for_activity": "moderate"},
        {"name": "Creatine Monohydrate",            "description": "Enhances strength, power, and muscle volume.",         "standard_dosage": 5.0,    "unit": "g",       "category": "Amino Acid",   "target_goal": "bulk",     "benefits": "Increases ATP production, improves workout performance",        "recommended_for_activity": "active"},
        {"name": "BCAA (Branched-Chain Amino Acids)","description": "Essential amino acids for muscle protein synthesis.", "standard_dosage": 10.0,   "unit": "g",       "category": "Amino Acid",   "target_goal": "all",      "benefits": "Reduces muscle soreness, promotes recovery",                    "recommended_for_activity": "active"},
        {"name": "L-Glutamine",                     "description": "Supports gut health and immune function.",             "standard_dosage": 5.0,    "unit": "g",       "category": "Amino Acid",   "target_goal": "all",      "benefits": "Supports immune system, aids recovery",                         "recommended_for_activity": "very_active"},
        {"name": "Beta-Alanine",                    "description": "Buffers acid during high-intensity exercise.",         "standard_dosage": 3.2,    "unit": "g",       "category": "Amino Acid",   "target_goal": "bulk",     "benefits": "Delays fatigue, improves endurance",                            "recommended_for_activity": "active"},
        {"name": "Omega-3 Fish Oil",                "description": "Essential fatty acids for heart and brain health.",    "standard_dosage": 2000.0, "unit": "mg",      "category": "Fatty Acid",   "target_goal": "all",      "benefits": "Reduces inflammation, supports heart and brain health",         "recommended_for_activity": "all"},
        {"name": "Omega-3 (EPA 1000mg)",            "description": "High-dose EPA for anti-inflammatory benefits.",        "standard_dosage": 1000.0, "unit": "mg",      "category": "Fatty Acid",   "target_goal": "cut",      "benefits": "Powerful anti-inflammatory, supports fat loss",                 "recommended_for_activity": "all"},
        {"name": "Vitamin D3",                      "description": "Essential for bone health and immune function.",       "standard_dosage": 5000.0, "unit": "IU",      "category": "Vitamin",      "target_goal": "all",      "benefits": "Supports bone health, immune function, mood, testosterone",     "recommended_for_activity": "all"},
        {"name": "Vitamin C",                       "description": "Antioxidant supporting immune function.",              "standard_dosage": 1000.0, "unit": "mg",      "category": "Vitamin",      "target_goal": "all",      "benefits": "Antioxidant protection, immune support, collagen synthesis",    "recommended_for_activity": "all"},
        {"name": "Vitamin B-Complex",               "description": "B vitamins for energy metabolism.",                    "standard_dosage": 1.0,    "unit": "capsule", "category": "Vitamin",      "target_goal": "all",      "benefits": "Energy production, brain function, stress management",          "recommended_for_activity": "all"},
        {"name": "Multivitamin",                    "description": "Comprehensive daily vitamin/mineral formula.",         "standard_dosage": 1.0,    "unit": "capsule", "category": "Vitamin",      "target_goal": "all",      "benefits": "Fills nutritional gaps, supports overall health",               "recommended_for_activity": "all"},
        {"name": "Magnesium Glycinate",             "description": "Highly bioavailable magnesium for sleep and recovery.","standard_dosage": 400.0,  "unit": "mg",      "category": "Mineral",      "target_goal": "all",      "benefits": "Improves sleep quality, reduces muscle cramps",                 "recommended_for_activity": "active"},
        {"name": "Zinc",                            "description": "Essential for immune function and testosterone.",      "standard_dosage": 30.0,   "unit": "mg",      "category": "Mineral",      "target_goal": "bulk",     "benefits": "Supports testosterone, immune function, protein synthesis",     "recommended_for_activity": "all"},
        {"name": "Iron",                            "description": "Essential for oxygen transport in blood.",             "standard_dosage": 18.0,   "unit": "mg",      "category": "Mineral",      "target_goal": "all",      "benefits": "Prevents anemia, supports energy",                              "recommended_for_activity": "all"},
        {"name": "Caffeine",                        "description": "Stimulant for focus, energy, and fat oxidation.",      "standard_dosage": 200.0,  "unit": "mg",      "category": "Stimulant",    "target_goal": "cut",      "benefits": "Increased alertness, enhanced fat burning",                     "recommended_for_activity": "active"},
        {"name": "L-Carnitine",                     "description": "Helps transport fatty acids for energy.",              "standard_dosage": 500.0,  "unit": "mg",      "category": "Amino Acid",   "target_goal": "cut",      "benefits": "Supports fat metabolism, improves endurance",                   "recommended_for_activity": "moderate"},
        {"name": "Ashwagandha",                     "description": "Adaptogenic herb for stress and cortisol management.","standard_dosage": 600.0,  "unit": "mg",      "category": "Herb",         "target_goal": "all",      "benefits": "Reduces stress, improves sleep, supports testosterone",         "recommended_for_activity": "all"},
        {"name": "Beta-Ecdysterone",                "description": "Natural anabolic compound from plants.",               "standard_dosage": 500.0,  "unit": "mg",      "category": "Herb",         "target_goal": "bulk",     "benefits": "Muscle building support, recovery, strength enhancement",       "recommended_for_activity": "active"},
    ]
    added = 0
    for item in CATALOG:
        if not db.query(SupplementCatalog).filter(SupplementCatalog.name == item["name"]).first():
            db.add(SupplementCatalog(**item))
            added += 1
    db.commit()
    if added:
        logger.info(f"✅ Seeded {added} supplements.")


def _seed_golden_foods(db):
    from models import Ingredient
    FOODS = [
        {"name": "Chicken Breast, Raw",      "name_ar": "صدر دجاج نيء",      "category": "Protein",    "calories_per_100g": 120.0, "protein_per_100g": 22.5, "carbs_per_100g": 0.0,  "fats_per_100g": 2.6,  "fiber_per_100g": 0.0,  "fdc_id": "PR_CHK_RAW",    "popularity_score": 100.0},
        {"name": "Chicken Breast, Grilled",  "name_ar": "صدر دجاج مشوي",     "category": "Protein",    "calories_per_100g": 165.0, "protein_per_100g": 31.0, "carbs_per_100g": 0.0,  "fats_per_100g": 3.6,  "fiber_per_100g": 0.0,  "fdc_id": "PR_CHK_GRL",    "popularity_score": 100.0},
        {"name": "Chicken Breast, Boiled",   "name_ar": "صدر دجاج مسلوق",    "category": "Protein",    "calories_per_100g": 150.0, "protein_per_100g": 28.0, "carbs_per_100g": 0.0,  "fats_per_100g": 3.2,  "fiber_per_100g": 0.0,  "fdc_id": "PR_CHK_BOIL",   "popularity_score": 95.0},
        {"name": "Beef, Lean, Raw",          "name_ar": "لحم بقري نيء",      "category": "Protein",    "calories_per_100g": 143.0, "protein_per_100g": 21.0, "carbs_per_100g": 0.0,  "fats_per_100g": 6.0,  "fiber_per_100g": 0.0,  "fdc_id": "PR_BEEF_RAW",   "popularity_score": 90.0},
        {"name": "Eggs, Hard Boiled",        "name_ar": "بيض مسلوق",         "category": "Protein",    "calories_per_100g": 155.0, "protein_per_100g": 12.6, "carbs_per_100g": 1.1,  "fats_per_100g": 10.6, "fiber_per_100g": 0.0,  "fdc_id": "PR_EGG_BOIL",   "popularity_score": 100.0},
        {"name": "Eggs, Whole, Raw",         "name_ar": "بيض كامل نيء",      "category": "Protein",    "calories_per_100g": 143.0, "protein_per_100g": 12.6, "carbs_per_100g": 0.7,  "fats_per_100g": 9.5,  "fiber_per_100g": 0.0,  "fdc_id": "PR_EGG_RAW",    "popularity_score": 90.0},
        {"name": "Egg Whites, Raw",          "name_ar": "بياض البيض",         "category": "Protein",    "calories_per_100g": 52.0,  "protein_per_100g": 10.9, "carbs_per_100g": 0.7,  "fats_per_100g": 0.2,  "fiber_per_100g": 0.0,  "fdc_id": "PR_EGG_WHITE",  "popularity_score": 95.0},
        {"name": "Tilapia, Raw",             "name_ar": "سمك بلطي نيء",      "category": "Protein",    "calories_per_100g": 96.0,  "protein_per_100g": 20.0, "carbs_per_100g": 0.0,  "fats_per_100g": 1.7,  "fiber_per_100g": 0.0,  "fdc_id": "PR_TILAPIA_RAW","popularity_score": 90.0},
        {"name": "Tuna, Canned in Water",    "name_ar": "تونة معلبة",         "category": "Protein",    "calories_per_100g": 116.0, "protein_per_100g": 25.5, "carbs_per_100g": 0.0,  "fats_per_100g": 0.8,  "fiber_per_100g": 0.0,  "fdc_id": "PR_TUNA_CAN",   "popularity_score": 95.0},
        {"name": "Whey Protein Powder",      "name_ar": "بروتين مسحوق",       "category": "Protein",    "calories_per_100g": 380.0, "protein_per_100g": 80.0, "carbs_per_100g": 5.0,  "fats_per_100g": 5.0,  "fiber_per_100g": 0.0,  "fdc_id": "PR_WHEY",       "popularity_score": 90.0},
        {"name": "Oats, Rolled, Raw",        "name_ar": "شوفان نيء",          "category": "Grains",     "calories_per_100g": 389.0, "protein_per_100g": 16.9, "carbs_per_100g": 66.3, "fats_per_100g": 6.9,  "fiber_per_100g": 10.6, "fdc_id": "PR_OATS_RAW",   "popularity_score": 100.0},
        {"name": "Oatmeal, Cooked",          "name_ar": "شوفان مطبوخ",        "category": "Grains",     "calories_per_100g": 71.0,  "protein_per_100g": 2.5,  "carbs_per_100g": 12.0, "fats_per_100g": 1.5,  "fiber_per_100g": 1.7,  "fdc_id": "PR_OATS_CKD",   "popularity_score": 95.0},
        {"name": "White Rice, Cooked",       "name_ar": "أرز أبيض مطبوخ",    "category": "Grains",     "calories_per_100g": 130.0, "protein_per_100g": 2.7,  "carbs_per_100g": 28.0, "fats_per_100g": 0.3,  "fiber_per_100g": 0.4,  "fdc_id": "PR_RICE_W_CKD", "popularity_score": 100.0},
        {"name": "White Rice, Raw",          "name_ar": "أرز أبيض نيء",      "category": "Grains",     "calories_per_100g": 365.0, "protein_per_100g": 7.1,  "carbs_per_100g": 80.0, "fats_per_100g": 0.7,  "fiber_per_100g": 1.3,  "fdc_id": "PR_RICE_W_RAW", "popularity_score": 95.0},
        {"name": "Brown Rice, Cooked",       "name_ar": "أرز بني مطبوخ",     "category": "Grains",     "calories_per_100g": 123.0, "protein_per_100g": 2.6,  "carbs_per_100g": 26.0, "fats_per_100g": 1.0,  "fiber_per_100g": 1.8,  "fdc_id": "PR_RICE_B_CKD", "popularity_score": 88.0},
        {"name": "Egyptian Bread (Baladi)",  "name_ar": "خبز بلدي",           "category": "Grains",     "calories_per_100g": 255.0, "protein_per_100g": 8.5,  "carbs_per_100g": 50.0, "fats_per_100g": 1.5,  "fiber_per_100g": 6.0,  "fdc_id": "PR_BREAD_EGY",  "popularity_score": 100.0},
        {"name": "Pasta, Cooked",            "name_ar": "معكرونة مطبوخة",     "category": "Grains",     "calories_per_100g": 158.0, "protein_per_100g": 5.8,  "carbs_per_100g": 31.0, "fats_per_100g": 0.9,  "fiber_per_100g": 1.8,  "fdc_id": "PR_PASTA_CKD",  "popularity_score": 95.0},
        {"name": "Sweet Potato, Baked",      "name_ar": "بطاطا حلوة مشوية",  "category": "Grains",     "calories_per_100g": 90.0,  "protein_per_100g": 2.0,  "carbs_per_100g": 20.7, "fats_per_100g": 0.2,  "fiber_per_100g": 3.3,  "fdc_id": "PR_SWT_BKD",    "popularity_score": 88.0},
        {"name": "Greek Yogurt, Full Fat",   "name_ar": "زبادي يوناني",       "category": "Dairy",      "calories_per_100g": 97.0,  "protein_per_100g": 9.0,  "carbs_per_100g": 3.6,  "fats_per_100g": 5.0,  "fiber_per_100g": 0.0,  "fdc_id": "PR_YOGURT_GRK", "popularity_score": 95.0},
        {"name": "Whole Milk",               "name_ar": "حليب كامل الدسم",   "category": "Dairy",      "calories_per_100g": 61.0,  "protein_per_100g": 3.2,  "carbs_per_100g": 4.8,  "fats_per_100g": 3.3,  "fiber_per_100g": 0.0,  "fdc_id": "PR_MILK_FULL",  "popularity_score": 90.0},
        {"name": "Labneh",                   "name_ar": "لبنة",               "category": "Dairy",      "calories_per_100g": 170.0, "protein_per_100g": 8.0,  "carbs_per_100g": 4.0,  "fats_per_100g": 14.0, "fiber_per_100g": 0.0,  "fdc_id": "PR_LABNEH",     "popularity_score": 95.0},
        {"name": "Cottage Cheese",           "name_ar": "جبنة قريش",          "category": "Dairy",      "calories_per_100g": 98.0,  "protein_per_100g": 11.1, "carbs_per_100g": 3.4,  "fats_per_100g": 4.3,  "fiber_per_100g": 0.0,  "fdc_id": "PR_CHEESE_CTG", "popularity_score": 88.0},
        {"name": "Fava Beans, Cooked",       "name_ar": "فول مطبوخ",          "category": "Legumes",    "calories_per_100g": 110.0, "protein_per_100g": 7.6,  "carbs_per_100g": 19.7, "fats_per_100g": 0.4,  "fiber_per_100g": 5.4,  "fdc_id": "PR_FAVA_CKD",   "popularity_score": 100.0},
        {"name": "Red Lentils, Cooked",      "name_ar": "عدس أحمر مطبوخ",    "category": "Legumes",    "calories_per_100g": 116.0, "protein_per_100g": 9.0,  "carbs_per_100g": 20.0, "fats_per_100g": 0.4,  "fiber_per_100g": 7.9,  "fdc_id": "PR_LENTIL_RCDK","popularity_score": 95.0},
        {"name": "Chickpeas, Cooked",        "name_ar": "حمص مطبوخ",          "category": "Legumes",    "calories_per_100g": 164.0, "protein_per_100g": 8.9,  "carbs_per_100g": 27.4, "fats_per_100g": 2.6,  "fiber_per_100g": 7.6,  "fdc_id": "PR_CHICKPEA",   "popularity_score": 90.0},
        {"name": "Hummus",                   "name_ar": "حمص طحيني",          "category": "Legumes",    "calories_per_100g": 177.0, "protein_per_100g": 7.9,  "carbs_per_100g": 14.3, "fats_per_100g": 9.6,  "fiber_per_100g": 6.0,  "fdc_id": "PR_HUMMUS",     "popularity_score": 88.0},
        {"name": "Potato, Boiled",           "name_ar": "بطاطس مسلوقة",       "category": "Vegetables", "calories_per_100g": 87.0,  "protein_per_100g": 1.9,  "carbs_per_100g": 20.0, "fats_per_100g": 0.1,  "fiber_per_100g": 1.8,  "fdc_id": "PR_POTATO_BOIL","popularity_score": 90.0},
        {"name": "Tomato, Raw",              "name_ar": "طماطم طازجة",        "category": "Vegetables", "calories_per_100g": 18.0,  "protein_per_100g": 0.9,  "carbs_per_100g": 3.9,  "fats_per_100g": 0.2,  "fiber_per_100g": 1.2,  "fdc_id": "PR_TOMATO",     "popularity_score": 90.0},
        {"name": "Cucumber, Raw",            "name_ar": "خيار طازج",           "category": "Vegetables", "calories_per_100g": 15.0,  "protein_per_100g": 0.7,  "carbs_per_100g": 3.6,  "fats_per_100g": 0.1,  "fiber_per_100g": 0.5,  "fdc_id": "PR_CUCUMBER",   "popularity_score": 88.0},
        {"name": "Banana",                   "name_ar": "موز",                 "category": "Fruits",     "calories_per_100g": 89.0,  "protein_per_100g": 1.1,  "carbs_per_100g": 23.0, "fats_per_100g": 0.3,  "fiber_per_100g": 2.6,  "fdc_id": "PR_BANANA",     "popularity_score": 100.0},
        {"name": "Apple",                    "name_ar": "تفاح",                "category": "Fruits",     "calories_per_100g": 52.0,  "protein_per_100g": 0.3,  "carbs_per_100g": 14.0, "fats_per_100g": 0.2,  "fiber_per_100g": 2.4,  "fdc_id": "PR_APPLE",      "popularity_score": 95.0},
        {"name": "Mango",                    "name_ar": "مانجو",               "category": "Fruits",     "calories_per_100g": 60.0,  "protein_per_100g": 0.8,  "carbs_per_100g": 15.0, "fats_per_100g": 0.4,  "fiber_per_100g": 1.6,  "fdc_id": "PR_MANGO",      "popularity_score": 90.0},
        {"name": "Dates, Dried",             "name_ar": "بلح جاف",             "category": "Fruits",     "calories_per_100g": 282.0, "protein_per_100g": 2.5,  "carbs_per_100g": 75.0, "fats_per_100g": 0.4,  "fiber_per_100g": 8.0,  "fdc_id": "PR_DATES",      "popularity_score": 88.0},
        {"name": "Olive Oil",                "name_ar": "زيت زيتون",           "category": "Fats",       "calories_per_100g": 884.0, "protein_per_100g": 0.0,  "carbs_per_100g": 0.0,  "fats_per_100g": 100.0,"fiber_per_100g": 0.0,  "fdc_id": "PR_OIL_OLIVE",  "popularity_score": 95.0},
        {"name": "Almonds, Raw",             "name_ar": "لوز نيء",             "category": "Nuts",       "calories_per_100g": 579.0, "protein_per_100g": 21.2, "carbs_per_100g": 21.6, "fats_per_100g": 49.9, "fiber_per_100g": 12.5, "fdc_id": "PR_ALMOND",     "popularity_score": 90.0},
        {"name": "Peanut Butter",            "name_ar": "زبدة الفول السوداني", "category": "Nuts",       "calories_per_100g": 588.0, "protein_per_100g": 25.1, "carbs_per_100g": 20.1, "fats_per_100g": 50.4, "fiber_per_100g": 6.0,  "fdc_id": "PR_PEANUTBTR",  "popularity_score": 90.0},
        {"name": "Tahini (Sesame Paste)",    "name_ar": "طحينة",               "category": "Nuts",       "calories_per_100g": 595.0, "protein_per_100g": 17.0, "carbs_per_100g": 21.2, "fats_per_100g": 53.8, "fiber_per_100g": 9.3,  "fdc_id": "PR_TAHINI",     "popularity_score": 88.0},
    ]
    added = 0
    for f in FOODS:
        if not db.query(Ingredient).filter(Ingredient.fdc_id == f["fdc_id"]).first():
            db.add(Ingredient(
                name=f["name"], name_ar=f["name_ar"], category=f["category"],
                calories_per_100g=f["calories_per_100g"], protein_per_100g=f["protein_per_100g"],
                carbs_per_100g=f["carbs_per_100g"], fats_per_100g=f["fats_per_100g"],
                fiber_per_100g=f.get("fiber_per_100g", 0.0), fdc_id=f["fdc_id"],
                source="MacroMetrics Core", is_golden=True, popularity_score=f["popularity_score"],
            ))
            added += 1
    db.commit()
    if added:
        logger.info(f"✅ Seeded {added} golden foods.")


# ==================== LIFESPAN ====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        import models  # noqa
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables verified / created.")
        db = SessionLocal()
        try:
            _seed_supplements(db)
            _seed_golden_foods(db)
        finally:
            db.close()
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
    yield


# ==================== APP ====================

app = FastAPI(
    title="MacroMetrics API",
    description="High-performance REST API for fitness & macro tracking",
    version="2.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Dynamic CORS - read FRONTEND_URL from environment
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://macrometrics.vercel.app")
CORS_ORIGINS = [
    FRONTEND_URL,
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_preflights(request: Request, call_next):
    if request.method == "OPTIONS":
        logger.info(f"PREFLIGHT: {request.url} | Origin: {request.headers.get('origin')}")
    return await call_next(request)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"error": "Validation Error", "detail": [{"loc": e["loc"], "msg": e["msg"]} for e in exc.errors()]})

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(status_code=500, content={"error": "Internal Server Error"})


app.include_router(auth.router)
app.include_router(ingredients.router)
app.include_router(meals.router)
app.include_router(daily.router)
app.include_router(users.router)
app.include_router(analytics.router)
app.include_router(chat.router)
app.include_router(supplements.router)


@app.get("/")
def root():
    return {"app": "MacroMetrics API", "version": "2.0.0", "status": "operational"}

@app.get("/health")
def health():
    return {"status": "ok", "database": str(engine.url.render_as_string(hide_password=True))}
