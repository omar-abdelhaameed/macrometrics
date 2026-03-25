# MacroMetrics V2.0 Deployment Guide

**Stack:** Vercel (Frontend) + Render (Backend + PostgreSQL)

---

## Prerequisites

- GitHub account
- Vercel account
- Render account

---

## Part 1: Database Setup (Render PostgreSQL)

### Step 1: Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New** → **PostgreSQL**
3. Configure:
   - **Name**: `macrometrics-db`
   - **Plan**: Free (or Starter $7/mo for production)
   - **Region**: Oregon (US West)
   - **PostgreSQL Version**: 16
4. Click **Create Database**

### Step 2: Get Connection String

Once provisioned (2-3 minutes):
1. Click on your database name (**macrometrics-db**)
2. Go to **Connections** section
3. Copy the **Internal Connection String** (format: `postgres://user:pass@host:5432/db`)

---

## Part 2: Backend Deployment (Render)

### Deploy via GitHub (Recommended)

1. Push your code to GitHub (if not already done)
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click **New** → **Web Service**
4. Connect your GitHub repository
5. Configure:
   - **Name**: `macrometrics-backend`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt && alembic upgrade head`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add Environment Variables:
   ```
   DATABASE_URL=postgres://... (from Step 1)
   JWT_SECRET=macrometrics-v1-prod-secret-983fn29d
   FRONTEND_URL=https://your-vercel-app.vercel.app
   ```
7. Click **Deploy**

### Get Backend URL

After deployment, Render will give you a URL like:
```
https://macrometrics-backend-xxxx.onrender.com
```

---

## Part 3: Frontend Deployment (Vercel)

### Step 1: Prepare Environment

Create `frontend/.env`:
```
VITE_API_URL=https://macrometrics-backend-xxxx.onrender.com
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
   VITE_API_URL=https://macrometrics-backend-xxxx.onrender.com
   ```
6. Click **Deploy**

---

## Part 4: Connect Everything

### Update Render Backend Environment

1. Go to your Backend Web Service on Render
2. Click **Environment**
3. Update `FRONTEND_URL` to your actual Vercel URL:
   ```
   FRONTEND_URL=https://your-app-name.vercel.app
   ```
4. Click **Save Changes** - service will auto-redeploy

---

## Environment Variables Summary

### Render Backend

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgres://user:pass@host:5432/db` |
| `JWT_SECRET` | Secret for JWT tokens | Generate with `openssl rand -hex 32` |
| `FRONTEND_URL` | Vercel frontend URL | `https://your-app.vercel.app` |

### Vercel Frontend

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Render backend URL | `https://backend.onrender.com` |

---

## Quick Commands

```bash
# Generate JWT secret
openssl rand -hex 32

# Run migrations
alembic upgrade head
```

---

## Troubleshooting

### Backend Issues
- **Migration failures**: Run `alembic upgrade head` in Render Console
- **CORS errors**: Ensure `FRONTEND_URL` in Render matches your Vercel domain exactly
- **Database connection**: Verify `DATABASE_URL` is correct (use Internal URL)

### Frontend Issues
- **API not found**: Verify `VITE_API_URL` points to correct Render domain
- **Build errors**: Check package.json dependencies

---

## Production URLs (Example)

- **Database**: Render PostgreSQL
- **Backend**: `https://macrometrics-backend.onrender.com`
- **Frontend**: `https://macrometrics.vercel.app`

---

**Deploy Date:** March 2026  
**Version:** V2.0