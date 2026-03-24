# Frontend Architecture

The MacroMetrics frontend is an SPA (Single Page Application) built with React 18 and Vite. It emphasizes a clean, premium user experience governed by dynamic themes, Framer Motion animations, and a strict separation of concerns.

## Global Contexts

The application relies on a series of nested React Context providers enveloping the `BrowserRouter` to supply global state.

1. **`AuthProvider`**: Manages the JWT `mm_token` and the currently authenticated `mm_user` object in `localStorage`. Exposes `isAuthenticated`, `login()`, `register()`, and `logout()` methods.
2. **`ThemeProvider`**: Listens to the authenticated user's `theme_mode` (light/dark) and `theme_accent` (green, blue, etc.), physically applying corresponding CSS variable classes to the document body. 
3. **`ToastProvider`**: A custom, globally accessible notification system exposing `showToast(msg, type)`.

### Routing Strategy
React Router handles navigation.
- **`AuthRoute`**: HOC (Higher-Order Component) wrapping `/login` and `/register`. If a user is already authenticated, they are redirected to `/`.
- **`ProtectedRoute`**: HOC wrapping the main app interface. If a user is missing a valid token, they are immediately redirected to `/login`.
- **`AppLayout`**: The main persistent shell comprising `Sidebar` and the nested `<main>` content container.

---

## Page Architecture

1. **`Login` / `Register`**
   - Public-facing auth routes. `Register` includes a stepped onboarding flow gathering physiological data necessary for the backend to compute their initial BMR/TDEE and macro targets.
   
2. **`Dashboard`** (`/`)
   - The primary view for the `DailySummary`. Renders the macro progress rings and the `MealLog` list for the current day. 

3. **`MealLogger`** (`/log`)
   - Features a togglable search interface:
     - **My Foods**: Queries the user's cached/custom `Ingredient` database (`GET /ingredients?search=...`).
     - **USDA Database**: Queries the external USDA API (`GET /ingredients/search-usda`).
   - Adding a USDA food automatically saves it locally via `POST /ingredients/save-from-usda` before logging it to the `Meal`.

4. **`Analytics`** (`/analytics`)
   - Connects to the `/analytics` endpoints to pull historical aggregates. Uses Recharts to render weight timeline graphs and macro composition donut charts.

5. **`Profile`** (`/profile`)
   - A form mapped to `PUT /users/me`. Modifying attributes like `goal_weight_lbs` or `activity_level` here triggers backend macro recalculation seamlessly.

6. **`Settings`** (`/settings`)
   - UI toggles mapping to the `ThemeProvider` context. Select dark/light mode and application accent colors, persisting changes back to the database.

---

## API & Networking (`api.js`)
A centralized custom fetch wrapper connecting to the FastAPI backend backend.
- **JWT Injection**: Automatically appends `Authorization: Bearer <token>` to requests from `localStorage`.
- **Interceptor-like behavior**: Globally catches `401 Unauthorized` responses to nuke local cache and kick the user back to `/login` if their token expires.
- **Error mapping**: Forwards FastAPI `HttpException` dictionary details to be easily caught by components and displayed in `showToast` UI alerts.
