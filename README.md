# MacroMetrics V2.0
**Pioneering Precision in Personal Nutrition**

MacroMetrics is a premium, full-stack web application meticulously engineered to provide users with a truly personalized, highly-accurate fitness and macronutrient tracking experience. Built on a modern React + FastAPI + PostgreSQL stack, it dynamically adapts to your body composition and evolving fitness goals.

## 🚀 Key Features

### 1. The Automated Nutrition Engine
Gone are the days of guessing your targets. MacroMetrics implements a robust, math-first backend engine:
- **Mifflin-St Jeor Formula**: Calculates your Basal Metabolic Rate (BMR) with clinical precision using your exact physiological inputs.
- **Activity Multipliers**: Computes your Total Daily Energy Expenditure (TDEE).
- **Bodybuilder Macro Distribution**: Automatically structures your diet: 
  - Sets **Protein** to an optimal 2.2g per kg of body weight for lean mass retention/growth.
  - Dedicates **25% of calories** to healthy **Fats**.
  - Dynamically assigns the remaining caloric payload to energizing **Carbohydrates**.
- **Real-Time Recalculation**: Change your primary goal (Cut, Maintain, Bulk) or update your weight, and the system instantly recalculates your optimal targets across the entire app.

### 2. Premium User Experience (UI/UX)
- **Tailwind CSS 4** with custom dark mode design system
- **Framer Motion** for elegant page transitions and micro-interactions
- **Responsive Layout** - Mobile-first design
- **Smart Onboarding**: A fluid, multi-step registration flow

### 3. AI-Powered Elite Coach
- **Ollama Integration** - Local AI for intelligent chat responses
- **Bilingual Support** - Arabic & English
- **Smart Meal Swaps** - Suggests alternatives within ±10% of macros
- **Context Awareness** - Knows your daily targets, consumed macros, goals

### 4. Supplement Tracking
- **Supplement Cabinet** - Save & track daily supplements
- **Custom Supplements** - Add your own with dosage
- **Daily Checkbox** - Auto-resets at midnight
- **Progress Tracker** - Visual completion bar

### 5. Analytics & Insights
- **Weight Trends** - 30-day chart with calorie correlation
- **Macro Composition** - Pie chart breakdown
- **Streak Tracking** - Logging consistency
- **Refeed Engine** - Detects plateaus & suggests refeed days

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18, Vite, Tailwind CSS 4, Framer Motion |
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Database | PostgreSQL |
| AI | Ollama (Llama3/Phi3) |
| Charts | Recharts |

## 📁 Project Structure

```
MacroMetrics/
├── frontend/           # React + Vite + Tailwind
│   ├── src/
│   │   ├── pages/     # Dashboard, MealLogger, Profile, etc.
│   │   ├── components/# Sidebar, AIChat, ToastProvider
│   │   └── api.js     # API calls
│
├── backend/           # FastAPI
│   ├── routes/        # API endpoints (users, meals, chat, etc.)
│   ├── models.py      # SQLAlchemy models
│   ├── schemas.py     # Pydantic schemas
│   └── main.py        # App entry
│
└── docs/              # Full documentation
```

## 🚦 Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### AI Chat (Optional)
```bash
ollama run llama3
ollama serve
```

## 📚 Full Documentation

- **[Backend API Documentation](docs/api.md)**
- **[Database Schema](docs/database.md)**
- **[Setup Guide](docs/setup.md)**

---

*MacroMetrics V2.0 - Built with ❤️ for fitness enthusiasts*