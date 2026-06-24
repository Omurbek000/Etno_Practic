import axios from 'axios';

function getBaseURL() {
  return `/${localStorage.getItem('etno_lang') || 'ru'}`;
}

const api = axios.create({ baseURL: '/ru', headers: { 'Content-Type': 'application/json' } });

api.interceptors.request.use((config) => {
  config.baseURL = getBaseURL();
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      if (!window.location.pathname.includes('/login')) window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Force re-render helper for language changes
let _langVersion = 0;
export function getLangVersion() { return _langVersion; }
export function bumpLangVersion() { _langVersion++; }

export default api;
