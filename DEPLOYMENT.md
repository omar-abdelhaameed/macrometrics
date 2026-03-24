# MacroMetrics V2.0 Deployment Guide

This guide covers deploying MacroMetrics to production with **Render** (Backend + PostgreSQL) and **Vercel** (Frontend).

---

## Prerequisites

- GitHub/GitLab account
- Render.com account
- Vercel.com account
- `git` installed locally

---

## Part 1: Database Setup (Render PostgreSQL)

### Step 1: Create PostgreSQL Database

1. Log in to [Render Dashboard](https://dashboard.render.com)
2. Click **New** → **PostgreSQL**
3. Configure:
   - **Name**: `macrometrics-db`
   - **Plan**: Free (or Starter $7/mo for production)
   - **Region**: Oregon (or closest to your users)
   - **PostgreSQL Version**: 16
4. Click **Create Database**

### Step 2: Get Connection String

Once provisioned (2-3 minutes):
1. Click your database name
2. Copy the **Internal Connection String** (format: `postgres://user:pass@host:5432/db`)
3. You'll use this as `DATABASE_URL` in the backend

---

## Part 2: Backend Deployment (Render)

### Option A: Deploy via Render Blueprint (Recommended)

1. Push your code to a GitHub repository
2. Go to [Render Blueprint](https://dashboard.render.com/blueprints)
3. Click **New Blueprint Instance**
4. Connect your GitHub repository
5. Select the `render.yaml` file
6. Configure environment variables:
   - `FRONTEND_URL`: Your Vercel frontend URL (e.g., `https://macrometrics.vercel.app`)
   - `JWT_SECRET`: Generate a secure secret (use a random 32+ char string)
7. Click **Apply**

### Option B: Manual Deploy

1. Create a new **Web Service** on Render:
   - **Name**: `macrometrics-backend`
   - **Repository**: Your GitHub repo
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt && alembic upgrade head`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
2. Add Environment Variables:
   ```
   DATABASE_URL=postgres://... (from Step 1)
   JWT_SECRET=your-secure-secret-min-32-chars
   FRONTEND_URL=https://your-vercel-app.vercel.app
   ```
3. Click **Deploy**

### Verify Backend Health

After deployment, visit:
```
https://macrometrics-backend.onrender.com/
```

Should return:
```json
{"app":"MacroMetrics API","version":"2.0.0","status":"operational"}
```

---

## Part 3: Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

Ensure `frontend/vite.config.js` uses environment variable:
```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
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
   VITE_API_URL=https://macrometrics-backend.onrender.com
   ```
6. Click **Deploy**

### Step 3: Configure Custom Domain (Optional)

1. Go to your Vercel project settings
2. Click **Domains**
3. Add your custom domain
4. Update DNS records as instructed

---

## Part 4: Environment Variables Summary

### Backend (Render)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgres://user:pass@host:5432/db` |
| `JWT_SECRET` | Secret for JWT tokens | Generate with `openssl rand -hex 32` |
| `FRONTEND_URL` | Vercel frontend URL | `https://macrometrics.vercel.app` |

### Frontend (Vercel)

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `https://macrometrics-backend.onrender.com` |

---

## Part 5: Update CORS for Production

After deploying, update `backend/main.py` to include your production domains:

```python
CORS_ORIGINS = [
    "https://your-app.vercel.app",
    "https://your-custom-domain.com",
    # ... other origins
]
```

Or set `FRONTEND_URL` environment variable on Render.

---

## Part 6: Local Development with Docker

For local testing, use Docker Compose:

```bash
# Clone and navigate to project
cd macrometrics

# Start all services
docker-compose up --build

# Services will be available at:
# - Frontend: http://localhost:5173
# - Backend:  http://localhost:8000
# - Database: localhost:5432
```

---

## Part 7: Troubleshooting

### Backend Issues

- **Migration failures**: Run `alembic upgrade head` manually in Render shell
- **CORS errors**: Verify `FRONTEND_URL` matches your Vercel domain exactly
- **Database connection**: Ensure `DATABASE_URL` is correct (use internal URL on Render)

### Frontend Issues

- **API not connecting**: Verify `VITE_API_URL` points to your Render backend
- **Build errors**: Ensure all dependencies in `package.json` are compatible with Node 20

### Common Fixes

```bash
# Rebuild backend Docker image
docker build -t backend ./backend

# Check backend logs on Render
render logs macrometrics-backend

# Run migrations manually
alembic upgrade head
```

---

## Quick Reference Commands

```bash
# Local development
docker-compose up

# Build for production (backend)
cd backend && docker build -t macrometrics .

# Generate JWT secret
openssl rand -hex 32
```

---

## Support

- Backend API: `https://macrometrics-backend.onrender.com`
- Frontend: `https://your-app.vercel.app`
- Health Check: `https://macrometrics-backend.onrender.com/`

---

**Deploy Date**: March 2026  
**Version**: V2.0.0