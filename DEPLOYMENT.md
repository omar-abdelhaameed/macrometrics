# MacroMetrics V2.0 Deployment Guide

**Stack:** Vercel (Frontend) + Koyeb (Backend) + Neon.tech (PostgreSQL)

---

## Prerequisites

- GitHub account
- Vercel account
- Koyeb account  
- Neon.tech account

---

## Part 1: Database Setup (Neon.tech)

### Step 1: Create Free PostgreSQL Database

1. Go to [Neon.tech](https://neon.tech) and sign up
2. Click **Create a project**
3. Configure:
   - **Name**: `macrometrics`
   - **Region**: Choose closest to your users
4. Click **Create Project**

### Step 2: Get Connection String

1. Click **Dashboard** → your project
2. Go to **Connection Details**
3. Copy the **Connection String** (format: `postgres://user:pass@host.neon.tech/db?sslmode=require`)

**Note:** The app automatically converts `postgres://` to `postgresql://` for SQLAlchemy 2.0 compatibility.

---

## Part 2: Backend Deployment (Koyeb)

### Step 1: Prepare GitHub Repository

Push your code to GitHub (if not already done).

### Step 2: Deploy to Koyeb

1. Log in to [Koyeb Dashboard](https://koyeb.com)
2. Click **Create App**
3. Choose **GitHub** as the source
4. Select your repository
5. Configure:
   - **Name**: `macrometrics-backend`
   - **Region**: Choose closest to your users
   - **Builder**: Dockerfile (since we have `backend/Dockerfile`)
   - **Dockerfile Path**: `backend/Dockerfile`
6. Add Environment Variables:
   ```
   DATABASE_URL=postgres://... (from Neon)
   JWT_SECRET=<generate-a-secure-secret>
   FRONTEND_URL=https://your-vercel-app.vercel.app
   ```
7. Click **Deploy**

### Step 3: Get Backend URL

After deployment, Koyeb will give you a URL like:
```
https://macrometrics-backend-username.koyeb.app
```

---

## Part 3: Frontend Deployment (Vercel)

### Step 1: Prepare Environment

Ensure your frontend has the API URL set. Create or update `frontend/.env`:
```
VITE_API_URL=https://macrometrics-backend-username.koyeb.app
```

### Step 2: Deploy to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **Add New** → **Project**
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
5. Add Environment Variable:
   ```
   VITE_API_URL=https://macrometrics-backend-username.koyeb.app
   ```
6. Click **Deploy**

---

## Part 4: Connect Everything

### Update Koyeb Environment

1. Go to your Koyeb app settings
2. Update `FRONTEND_URL` to your actual Vercel URL:
   ```
   FRONTEND_URL=https://macrometrics-username.vercel.app
   ```

### Update CORS (Auto-handled)

The backend already reads `FRONTEND_URL` from environment and allows it automatically.

---

## Part 5: Run Migrations (Critical!)

Before the app goes live, you MUST run migrations on the Neon database:

### Option A: From Local Terminal

```bash
# Set your Neon connection string
export DATABASE_URL="postgres://user:pass@host.neon.tech/db?sslmode=require"

# Navigate to backend
cd backend

# Run migrations
alembic upgrade head
```

### Option B: Using Koyeb Shell

1. Go to your Koyeb app in dashboard
2. Click **Console**
3. Run:
   ```bash
   alembic upgrade head
   ```

---

## Environment Variables Summary

### Koyeb Backend

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Neon connection string | `postgres://...neon.tech/db` |
| `JWT_SECRET` | Secure token secret | Generate with `openssl rand -hex 32` |
| `FRONTEND_URL` | Vercel frontend URL | `https://macrometrics.vercel.app` |

### Vercel Frontend

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Koyeb backend URL | `https://backend.koyeb.app` |

---

## Quick Commands

```bash
# Generate JWT secret
openssl rand -hex 32

# Test database connection locally
cd backend
export DATABASE_URL="postgres://..."
python -c "from database import engine; print(engine.connect())"

# Run migrations
alembic upgrade head
```

---

## Troubleshooting

### Neon Issues
- **Connection timeout**: Ensure you're using `?sslmode=require` in the URL
- **Database paused**: Neon free tier pauses after 30 days - simply resume from dashboard

### Koyeb Issues
- **Build fails**: Check Dockerfile path is `backend/Dockerfile`
- **Runtime errors**: Verify DATABASE_URL is correct

### Vercel Issues
- **API not found**: Verify VITE_API_URL points to correct Koyeb domain
- **CORS errors**: Ensure FRONTEND_URL in Koyeb matches exactly

---

## Production URLs (Example)

- **Database**: Neon.tech (managed PostgreSQL)
- **Backend**: `https://macrometrics-backend.koyeb.app`
- **Frontend**: `https://macrometrics.vercel.app`

---

**Deploy Date:** March 2026  
**Version:** V2.0