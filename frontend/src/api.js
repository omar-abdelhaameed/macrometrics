const API_BASE = 'http://localhost:8000';

function getHeaders() {
  const headers = { 'Content-Type': 'application/json' };
  const token = localStorage.getItem('mm_token');
  if (token) headers['Authorization'] = `Bearer ${token}`;
  return headers;
}

async function api(url, options = {}) {
  const res = await fetch(`${API_BASE}${url}`, {
    ...options,
    headers: { ...getHeaders(), ...options.headers },
  });
  if (res.status === 401) {
    localStorage.removeItem('mm_token');
    localStorage.removeItem('mm_user');
    window.location.href = '/login';
    throw new Error('Session expired');
  }
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || `Request failed (${res.status})`);
  }
  return res.json();
}

// ── Auth ─────────────────────────────────────────────
export const loginUser = (email, password) =>
  api('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) });

export const registerUser = (data) =>
  api('/auth/register', { method: 'POST', body: JSON.stringify(data) });

// ── User ─────────────────────────────────────────────
export const fetchUser = () => api('/users/me');
export const updateUser = (data) =>
  api('/users/me', { method: 'PUT', body: JSON.stringify(data) });

// ── Daily Summary ────────────────────────────────────
export const fetchDailySummary = (date) => api(`/daily-summary?date=${date}`);

// ── Ingredients ──────────────────────────────────────
export const fetchIngredients = (query = '') => {
  const url = query
    ? `/ingredients?search=${encodeURIComponent(query)}`
    : '/ingredients';
  return api(url);
};

export const searchUSDA = (query, lang = 'en') =>
  api(`/ingredients/search?query=${encodeURIComponent(query)}&lang=${lang}`);

export const searchUSDAOld = (query) =>
  api(`/ingredients/search-usda?query=${encodeURIComponent(query)}`);

export const saveFromUSDA = (data) =>
  api('/ingredients/save-from-usda', { method: 'POST', body: JSON.stringify(data) });

// ── Meals ────────────────────────────────────────────
export const logMeal = (mealData) =>
  api('/meals', { method: 'POST', body: JSON.stringify(mealData) });

export const fetchMeals = (date) => api(`/meals?date=${date}`);

// ── Daily Log ────────────────────────────────────────
export const toggleRefeedDay = (logId) =>
  api(`/daily-log/${logId}/toggle-refeed`, { method: 'PATCH' });

// ── Analytics ────────────────────────────────────────
export const fetchAnalyticsSummary = (days = 30) => api(`/analytics/summary?days=${days}`);
export const fetchWeightTrend = (days = 30) => api(`/analytics/weight-trend?days=${days}`);
export const fetchMacroComposition = (days = 30) => api(`/analytics/macro-composition?days=${days}`);
export const fetchWeightPlateau = (days = 7) => api(`/analytics/weight-plateau?days=${days}`);

// ── Chat ──────────────────────────────────────────────
export const sendChatMessage = (message, history = []) =>
  api('/chat', { method: 'POST', body: JSON.stringify({ message, conversation_history: history }) });

export const fetchChatContext = () => api('/chat/context');

// ── Supplements ───────────────────────────────────────
export const fetchSupplements = () => api('/supplements/catalog');
export const fetchSupplementCategories = () => api('/supplements/categories');
export const fetchRecommendations = () => api('/supplements/recommendations');
export const fetchMyStack = () => api('/supplements/my-stack');

export const addToStack = (data) =>
  api('/supplements/my-stack', { method: 'POST', body: JSON.stringify(data) });

export const removeFromStack = (stackItemId) =>
  api(`/supplements/my-stack/${stackItemId}`, { method: 'DELETE' });

export const logSupplement = (userSupplementId, date) =>
  api('/supplements/log', { 
    method: 'POST', 
    body: JSON.stringify({ 
      user_supplement_id: userSupplementId,
      date: date || new Date().toISOString().split('T')[0]
    }) 
  });

export const fetchSupplementHistory = (days = 7) =>
  api(`/supplements/log/history?days=${days}`);
