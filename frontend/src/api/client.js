import axios from "axios";

// Бэкенд оборачивает все роуты в i18n_patterns (movie/urls.py),
// поэтому каждый запрос должен идти с языковым префиксом, например /ru/film/.
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
const LANG = import.meta.env.VITE_API_LANG || "ru";

export const MEDIA_BASE_URL = BASE_URL;

const api = axios.create({
  baseURL: `${BASE_URL}/${LANG}`,
});

function getTokens() {
  return {
    access: localStorage.getItem("access"),
    refresh: localStorage.getItem("refresh"),
  };
}

export function setTokens({ access, refresh }) {
  if (access) localStorage.setItem("access", access);
  if (refresh) localStorage.setItem("refresh", refresh);
}

export function clearTokens() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
}

api.interceptors.request.use((config) => {
  const { access } = getTokens();
  if (access) {
    config.headers.Authorization = `Bearer ${access}`;
  }
  return config;
});

// Если access-токен истёк (401), пробуем обновить его через refresh и повторить запрос.
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const { refresh } = getTokens();
      if (refresh) {
        try {
          const { data } = await axios.post(`${BASE_URL}/${LANG}/token/refresh/`, { refresh });
          setTokens({ access: data.access });
          originalRequest.headers.Authorization = `Bearer ${data.access}`;
          return api(originalRequest);
        } catch {
          clearTokens();
        }
      } else {
        clearTokens();
      }
    }
    return Promise.reject(error);
  }
);

/** Превращает относительный путь от DRF (если он не абсолютный) в полный URL медиа-файла. */
export function mediaUrl(path) {
  if (!path) return null;
  if (path.startsWith("http://") || path.startsWith("https://")) return path;
  return `${MEDIA_BASE_URL}${path}`;
}

export default api;
