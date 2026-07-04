import api from "./client";

/* ---------- Auth ---------- */
export const registerUser = (data) => api.post("/register/", data).then((r) => r.data);
export const loginUser = (data) => api.post("/login/", data).then((r) => r.data);
export const logoutUser = (refresh) => api.post("/logout/", { refresh }).then((r) => r.data);
export const fetchMe = () => api.get("/users/").then((r) => r.data);
export const updateMe = (id, data) => api.patch(`/users/${id}/`, data).then((r) => r.data);

/* ---------- Catalog ---------- */
export const fetchFilms = (params) => api.get("/film/", { params }).then((r) => r.data);
export const fetchFilm = (id) => api.get(`/film/${id}/`).then((r) => r.data);

export const fetchSeries = (params) => api.get("/series/", { params }).then((r) => r.data);
export const fetchSeriesDetail = (id) => api.get(`/series/${id}/`).then((r) => r.data);

export const fetchCartoons = (params) => api.get("/cartoon/", { params }).then((r) => r.data);
export const fetchCartoon = (id) => api.get(`/cartoon/${id}/`).then((r) => r.data);

export const fetchGenres = () => api.get("/genre/").then((r) => r.data);
export const fetchCountries = () => api.get("/country/").then((r) => r.data);

/* ---------- Favorites ---------- */
export const fetchFavorites = () => api.get("/favorite/").then((r) => r.data);
export const addFavorite = (payload) => api.post("/favoriteitem/", payload).then((r) => r.data);
export const removeFavorite = (id) => api.delete(`/favoriteitem/${id}/`);

/* ---------- Reviews ---------- */
export const fetchReviews = (params) => api.get("/review/", { params }).then((r) => r.data);
export const createReview = (payload) => api.post("/review/", payload).then((r) => r.data);
export const deleteReview = (id) => api.delete(`/review/${id}/`);
