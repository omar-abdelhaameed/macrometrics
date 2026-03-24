# MacroMetrics V2.0

**Precision Nutrition Engineering for Elite Fitness**

MacroMetrics is a production-ready, commercial-grade fitness SaaS platform that delivers clinical-grade macronutrient tracking with AI-powered coaching. Built for athletes who demand mathematical precision in their nutrition.

---

## Key Features

### 1. Automated Nutrition Engine
- **Mifflin-St Jeor BMR Calculation** - Clinical precision using weight, height, age, gender
- **TDEE Activity Multipliers** - Sedentary to Very Active (1.2x–1.9x)
- **Bodybuilder Macro Distribution** - 2.2g protein/kg, 25% fats, remainder carbs
- **Dynamic Recalculation** - Real-time target updates on goal/weight changes

### 2. AI Elite Coach (Gemini)
- **Context-Aware Conversations** - Knows your daily macros, goals, trends
- **Bilingual Support** - Arabic & English
- **Smart Meal Alternatives** - ±10% macro matching
- **Pro-Tier Plateau Detection** - Refeed suggestions for stuck users

### 3. Bilingual Hybrid Food Search
- **Golden Foods Database** - Curated priority foods with fast lookup
- **USDA API Fallback** - 900,000+ foods for long-tail items
- **Arabic Text Normalization** - Handles أ/إ/ا and ه/ة variations
- **Real-Time Results** - Sorted by popularity and relevance

### 4. Personalized Supplement Stack
- **AI Recommendations** - Based on user's goal (Cut/Bulk/Maintain) and activity level
- **Custom Dosages** - Personalize every supplement
- **Time-of-Day Scheduling** - Morning, Pre-workout, Night, etc.
- **Daily Logging** - Track compliance with visual progress
- **22+ Scientific Supplements** - Creatine, Whey, Omega-3, Vitamin D3, Zinc, Magnesium, and more

### 5. Analytics Dashboard
- **30-Day Weight Trends** - With calorie correlation
- **Macro Composition** - Pie chart breakdown
- **Streak Tracking** - Logging consistency
- **Refeed Engine** - Plateau detection & refeed day suggestions

### 6. Premium UX
- **Tailwind CSS 4** with custom dark mode design tokens
- **Framer Motion** animations
- **Mobile-First** responsive layout
- **JWT Authentication** with theme persistence

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 19, Vite 8, Tailwind CSS 4, Framer Motion, Recharts |
| Backend | FastAPI, SQLAlchemy 2.0, Pydantic 2.x |
| Database | PostgreSQL (Alembic migrations) |
| Auth | JWT (48hr), bcrypt (rounds=12), SlowAPI rate limiting |
| AI | Gemini 2.5 Flash (primary), Flash-Lite (fallback) |
| External APIs | USDA FoodData Central |

---

## Project Structure

```
MacroMetrics/
├── frontend/                    # React + Vite + Tailwind
│   ├── src/
│   │   ├── pages/              # Dashboard, MealLogger, Profile, Supplements
│   │   ├── components/         # Sidebar, AIChat, ToastProvider
│   │   ├── contexts/           # AuthContext, ThemeContext
│   │   └── api.js              # API client
│   └── package.json
│
├── backend/                     # FastAPI
│   ├── routes/                 # API endpoints
│   │   ├── auth.py            # Register, Login
│   │   ├── supplements.py      # Supplement CRUD + logging
│   │   ├── ingredients.py      # Food search
│   │   └── ...
│   ├── services/
│   │   ├── nutrition.py        # Mifflin-St Jeor engine
│   │   ├── supplements.py     # AI recommendations
│   │   └── usda.py            # USDA API client
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── main.py                # App entry
│   ├── alembic/               # Database migrations
│   └── data/                  # Seed scripts
│       ├── seed_golden_foods.py
│       ├── seed_egyptian_foods.py
│       └── seed_supplements.py
│
└── docs/                       # API documentation
```

---

## Local Development Setup

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 14+

### 1. Clone & Install

```bash
# Clone the repository
git clone <repo-url>
cd MacroMetrics

# Backend setup
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### 2. Environment Variables

Create `backend/.env`:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/macrometrics

# Security (generate with: python -c "import secrets; print(secrets.token_hex(32))")
JWT_SECRET=your-256-bit-secret-key

# USDA FoodData Central (free API key)
NUTRITION_API_KEY=your-usda-key

# Google Gemini AI (optional - for AI Coach)
GEMINI_API_KEY=your-gemini-key

# App Environment
APP_ENV=development
```

### 3. Database Migrations

```bash
cd backend

# Run Alembic migrations
python -m alembic upgrade head
```

### 4. Seed Database

```bash
# Seed golden foods (curated priority foods)
python -m data.seed_golden_foods

# Seed Egyptian foods (Arabic food database)
python -m data.seed_egyptian_foods

# Seed supplement catalog (22+ supplements)
python -m data.seed_supplements
```

### 5. Run Development Servers

```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 6. Access

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/register` | POST | User registration with auto macro calculation |
| `/auth/login` | POST | JWT token authentication |
| `/ingredients/search` | GET | Hybrid food search (Golden + USDA) |
| `/supplements/catalog` | GET | All available supplements |
| `/supplements/recommendations` | GET | AI recommendations based on user profile |
| `/supplements/my-stack` | GET/POST | User's personal supplement stack |
| `/supplements/log` | POST | Check off supplement for today |
| `/meals` | POST | Log a meal with ingredients |
| `/daily-summary/{date}` | GET | Daily macro progress |
| `/chat` | POST | AI Coach conversation |
| `/analytics/weight-trend` | GET | 30-day weight analytics |

---

## Security Features

- **Rate Limiting** - SlowAPI (Auth: 5/min, Search: 30/min, Chat: 10/min)
- **Input Validation** - Pydantic with EmailStr, Field constraints, Literal enums
- **JWT Authentication** - 48-hour expiry, bcrypt rounds=12
- **Environment Secrets** - Required DATABASE_URL, JWT_SECRET (no fallbacks)
- **CORS Protection** - Configurable origins

---

## Production Deployment

1. Set `APP_ENV=production` in environment
2. Configure PostgreSQL connection pooling
3. Set up reverse proxy (nginx) with SSL
4. Configure CORS in `main.py` for production domain
5. Run: `alembic upgrade head` (not create_all)

---

*MacroMetrics V2.0 - Science-Backed Nutrition for Elite Athletes*
