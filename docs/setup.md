# Local Development Setup Guide

Getting MacroMetrics running locally requires setting up the PostgreSQL database, the Python/FastAPI backend, and the Vite/React frontend.

## 1. Prerequisites
- **Node.js** v18+ 
- **Python** 3.10+
- **PostgreSQL** 14+ installed and running locally.

## 2. Database Configuration
Ensure PostgreSQL is running on its default port (`5432`).
Create the development database by running the following command in your terminal / pgAdmin / psql:
```sql
CREATE DATABASE "fitnessApp";
```
*Note: Make sure your PostgreSQL user credentials match the connection string specified in the backend's `.env` file.*

---

## 3. Backend Setup

1. Open a terminal and navigate to the `backend/` directory:
   ```bash
   cd backend
   ```

2. Create a Python Virtual Environment:
   ```bash
   python -m venv venv
   ```

3. Activate the Virtual Environment:
   - **Windows**: `venv\Scripts\activate`
   - **Mac/Linux**: `source venv/bin/activate`

4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Environment Variables:
   Ensure the `backend/.env` file exists with the following values:
   ```env
   DATABASE_URL="postgresql://postgres:loader@localhost:5432/fitnessApp"
   SECRET_KEY="your_super_secret_dev_jwt_key_here"
   USDA_API_KEY="DEMO_KEY"
   ```
   *Note: Change `postgres:loader` to your actual postgres username and password.*

6. **Seed the Database (Important)**:
   This will create all the required PostgreSQL tables, seed a few dummy user accounts with historical data, and inject a starting `Ingredient` library.
   ```bash
   python seed.py
   ```

7. Start the Uvicorn Dev Server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

---

## 4. Frontend Setup

1. Open a *new* terminal window and navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```

2. Install NPM dependencies:
   ```bash
   npm install
   ```

3. Start the Vite server:
   ```bash
   npm run dev
   ```

4. The application should now be accessible at `http://localhost:5173`. 
   - You can log in using the demo credentials created by the seed script:
     - **Email**: `omar@macrometrics.app`
     - **Password**: `omar123`
