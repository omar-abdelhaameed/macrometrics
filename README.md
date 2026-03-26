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

### 6. Premium Subscription (Coming Soon)
- **$10/month** - Unlock elite features
- Everything in Free + AI Coach, USDA database, advanced analytics, supplement AI, priority support

### 7. Premium UX
- **Tailwind CSS 4** with custom dark/light mode design tokens
- **Framer Motion** animations
- **Mobile-First** responsive layout
- **JWT Authentication** with theme persistence
- **Expandable Sidebar** with hover animations

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 19, Vite 8, Tailwind CSS 4, Framer Motion, Recharts |
| Backend | FastAPI, SQLAlchemy 2.0, Pydantic 2.x |
| Database | PostgreSQL (Alembic migrations) |
| Auth | JWT (48hr), pbkdf2_sha256, SlowAPI rate limiting |
| AI | Gemini 2.5 Flash (primary), Flash-Lite (fallback) |
| External APIs | USDA FoodData Central |
| Deployment | Vercel (Frontend), Render (Backend + PostgreSQL) |

---

## Project Structure

```
MacroMetrics/
├── frontend/                    # React + Vite + Tailwind
│   ├── src/
│   │   ├── pages/              # Dashboard, MealLogger, Profile, Supplements, Analytics, Premium
│   │   ├── components/         # Sidebar, AIChat, WaterTracker, NumberInput, ToastProvider
│   │   ├── contexts/           # AuthContext, ThemeContext
│   │   └── api.js             # API client with timeout handling
│   └── package.json
│
├── backend/                     # FastAPI
│   ├── routes/                 # API endpoints
│   │   ├── auth.py            # Register, Login
│   │   ├── supplements.py     # Supplement CRUD + logging
│   │   ├── ingredients.py     # Food search
│   │   ├── analytics.py      # Weight trends, macro composition
│   │   ├── chat.py           # AI Coach
│   │   └── ...
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py            # Pydantic schemas
│   ├── main.py               # App entry + seed functions
│   ├── database.py           # SQLAlchemy engine with Neon URL fix
│   ├── auth.py               # JWT utilities with dev fallback
│   ├── alembic/              # Database migrations
│   └── data/                 # Seed scripts
│       ├── seed_golden_foods.py
│       ├── seed_egyptian_foods.py
│       └── seed_supplements.py
│
├── docker-compose.yml          # Local development
├── DEPLOYMENT.md              # Production deployment guide
└── README.md
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
# Database (fallback to SQLite for local dev if not set)
DATABASE_URL=postgresql://username:password@localhost:5432/macrometrics

# Security (generate with: openssl rand -hex 32)
JWT_SECRET=your-256-bit-secret-key

# USDA FoodData Central (free API key)
NUTRITION_API_KEY=your-usda-key

# Google Gemini AI (optional - for AI Coach)
GEMINI_API_KEY=your-gemini-key

# Frontend URL for CORS (local dev)
FRONTEND_URL=http://localhost:5173
```

Create `frontend/.env` (optional for local):

```env
VITE_API_URL=http://localhost:8000
```

### 3. Database Migrations

```bash
cd backend
python -m alembic upgrade head
```

### 4. Run Development Servers

```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 5. Access

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/register` | POST | User registration with auto macro calculation |
| `/auth/login` | POST | JWT token authentication |
| `/users/me` | GET/PUT | Get or update user profile |
| `/ingredients` | GET | List golden foods database |
| `/ingredients/search` | GET | Hybrid food search (Golden + USDA) |
| `/ingredients/save-from-usda` | POST | Save USDA food to user library |
| `/meals` | GET/POST | Log meals |
| `/daily-summary` | GET | Daily macro progress |
| `/daily-log/{id}/toggle-refeed` | PATCH | Toggle refeed day |
| `/supplements/catalog` | GET | All available supplements |
| `/supplements/recommendations` | GET | AI recommendations based on profile |
| `/supplements/my-stack` | GET/POST/DELETE | User's personal supplement stack |
| `/supplements/log` | POST | Log supplement taken |
| `/analytics/summary` | GET | Analytics overview |
| `/analytics/weight-trend` | GET | 30-day weight trends |
| `/analytics/macro-composition` | GET | Macro breakdown pie chart |
| `/analytics/weight-plateau` | GET | Plateau detection |
| `/chat` | POST | AI Coach conversation |
| `/chat/context` | GET | User context for AI |

---

## Security Features

- **Rate Limiting** - SlowAPI (Auth: 5/min, Search: 30/min, Chat: 10/min)
- **Input Validation** - Pydantic with EmailStr, Field constraints, Literal enums
- **JWT Authentication** - 48-hour expiry, pbkdf2_sha256
- **Dynamic CORS** - Configurable origins via FRONTEND_URL env variable
- **SQL Injection Protection** - SQLAlchemy ORM with parameterized queries

---

## Production Deployment

### Stack
- **Frontend**: Vercel
- **Backend**: Render (Web Service)
- **Database**: Render (PostgreSQL)

### Environment Variables

**Render Backend:**
| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string from Render |
| `JWT_SECRET` | Secure token secret (generate with `openssl rand -hex 32`) |
| `FRONTEND_URL` | Your Vercel frontend URL |
| `NUTRITION_API_KEY` | USDA API key |
| `GEMINI_API_KEY` | Google Gemini API key |

**Vercel Frontend:**
| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | Your Render backend URL |

### Quick Deploy

1. Create PostgreSQL on Render → copy connection string
2. Deploy Backend to Render (GitHub) with env vars
3. Deploy Frontend to Vercel with VITE_API_URL
4. Update FRONTEND_URL on Render to match your Vercel domain

See `DEPLOYMENT.md` for detailed step-by-step guide.

---

## Premium Subscription

Coming soon at **$10/month**:

| Feature | Free | Premium |
|---------|------|---------|
| Basic macro tracking | ✅ | ✅ |
| Manual food logging | ✅ | ✅ |
| Daily summary dashboard | ✅ | ✅ |
| Golden Foods database | ✅ | ✅ |
| AI Coach (Gemini) | ❌ | ✅ |
| USDA database (900k+ foods) | ❌ | ✅ |
| Advanced analytics (30-day+) | ❌ | ✅ |
| Supplement tracking | ❌ | ✅ |
| AI supplement recommendations | ❌ | ✅ |
| Priority support | ❌ | ✅ |

---

*MacroMetrics V2.0 - Science-Backed Nutrition for Elite Athletes*
*Build with ❤️ for performance athletes worldwide*