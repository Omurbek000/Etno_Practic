// @ts-check
import api from "./client";

/* ---------- Типы данных (соответствуют сериализаторам movie/etno/serializers.py) ---------- */

/**
 * @typedef {Object} Country
 * @property {number} id
 * @property {string} country
 */

/**
 * @typedef {Object} Genre
 * @property {number} id
 * @property {string} name
 */

/**
 * @typedef {Object} Person
 * @property {number} id
 * @property {string} last_name
 * @property {string} person_image
 * @property {string} role
 */

/**
 * @typedef {Object} UserProfile
 * @property {number} id
 * @property {string} username
 * @property {string} first_name
 * @property {string} last_name
 * @property {string} email
 * @property {string|null} avatar
 * @property {string|null} phone_number
 * @property {string} subscription_status
 * @property {string} date_register
 */

/**
 * @typedef {Object} FilmList
 * @property {number} id
 * @property {string} title
 * @property {string} poster_image
 * @property {number} year
 * @property {string} access_type
 * @property {boolean} is_published
 * @property {string} created_date
 * @property {Country} country
 * @property {Genre[]} genres
 * @property {number|null} get_avg_rating
 * @property {number} get_ratings_count
 */

/**
 * @typedef {FilmList & {
 *   description: string|null,
 *   language: string,
 *   duration: number,
 *   video: string,
 *   trailer: string,
 *   persons: Person[],
 *   rent_price: number|null,
 *   views_count: number
 * }} FilmDetail
 */

/**
 * @typedef {Object} SeriesList
 * @property {number} id
 * @property {string} title
 * @property {string} image
 * @property {number} year
 * @property {Country} country
 * @property {string} language
 * @property {Genre[]} genres
 * @property {string} access_type
 * @property {boolean} is_published
 */

/**
 * @typedef {SeriesList & {
 *   season: number,
 *   description: string|null,
 *   trailer_url: string,
 *   video: string|null,
 *   persons: Person[],
 *   views_count: number,
 *   created_date: string
 * }} SeriesDetail
 */

/**
 * @typedef {Object} CartoonList
 * @property {number} id
 * @property {string} title
 * @property {string} cartoon_image
 * @property {number} year
 * @property {string} language
 * @property {string} age_rating
 * @property {Genre[]} genres
 * @property {string} access_type
 * @property {boolean} is_published
 * @property {Country} country
 */

/**
 * @typedef {CartoonList & {
 *   description: string|null,
 *   duration: number,
 *   video: string,
 *   trailer_url: string,
 *   views_count: number,
 *   created_date: string
 * }} CartoonDetail
 */

/**
 * @typedef {Object} FavoriteItem
 * @property {number} id
 * @property {FilmList|null} film
 * @property {SeriesList|null} series
 * @property {CartoonList|null} cartoon
 * @property {number|null} film_id
 * @property {number|null} series_id
 * @property {number|null} cartoon_id
 */

/**
 * @typedef {Object} Favorite
 * @property {number} id
 * @property {number} user
 * @property {FavoriteItem[]} film_item
 */

/**
 * @typedef {Object} Review
 * @property {number} id
 * @property {UserProfile} user_review
 * @property {number|null} film_id
 * @property {number|null} series_id
 * @property {number|null} cartoon_id
 * @property {number|null} stars
 * @property {string|null} text
 * @property {number|null} parent
 * @property {string} created_date
 */

/**
 * @typedef {Object} LoginResponse
 * @property {{ username: string, email: string }} user
 * @property {string} access
 * @property {string} refresh
 */

/**
 * @typedef {Object} RegisterData
 * @property {string} email
 * @property {string} username
 * @property {string} password
 * @property {string} [phone_number]
 */

/**
 * @template T
 * @typedef {Object} PageOf
 * @property {number} count
 * @property {string|null} next
 * @property {string|null} previous
 * @property {T[]} results
 */

/* ---------- Auth ---------- */

/**
 * @param {RegisterData} data
 * @returns {Promise<UserProfile>}
 */
export const registerUser = (data) =>
  api.post("/register/", data).then((r) => r.data);

/**
 * @param {{ username: string, password: string }} data
 * @returns {Promise<LoginResponse>}
 */
export const loginUser = (data) =>
  api.post("/login/", data).then((r) => r.data);

/**
 * @param {string} refresh
 * @returns {Promise<void>}
 */
export const logoutUser = (refresh) =>
  api.post("/logout/", { refresh }).then((r) => r.data);

/**
 * @returns {Promise<UserProfile[]>}
 */
export const fetchMe = () => api.get("/users/").then((r) => r.data);

/**
 * @param {number} id
 * @param {Partial<UserProfile>} data
 * @returns {Promise<UserProfile>}
 */
export const updateMe = (id, data) =>
  api.patch(`/users/${id}/`, data).then((r) => r.data);

/* ---------- Catalog ---------- */

/**
 * @param {Object} [params]
 * @returns {Promise<PageOf<FilmList>>}
 */
export const fetchFilms = (params) =>
  api.get("/film/", { params }).then((r) => r.data);

/**
 * @param {number} id
 * @returns {Promise<FilmDetail>}
 */
export const fetchFilm = (id) => api.get(`/film/${id}/`).then((r) => r.data);

/**
 * @param {Object} [params]
 * @returns {Promise<PageOf<SeriesList>>}
 */
export const fetchSeries = (params) =>
  api.get("/series/", { params }).then((r) => r.data);

/**
 * @param {number} id
 * @returns {Promise<SeriesDetail>}
 */
export const fetchSeriesDetail = (id) =>
  api.get(`/series/${id}/`).then((r) => r.data);

/**
 * @param {Object} [params]
 * @returns {Promise<PageOf<CartoonList>>}
 */
export const fetchCartoons = (params) =>
  api.get("/cartoon/", { params }).then((r) => r.data);

/**
 * @param {number} id
 * @returns {Promise<CartoonDetail>}
 */
export const fetchCartoon = (id) =>
  api.get(`/cartoon/${id}/`).then((r) => r.data);

/**
 * @returns {Promise<Genre[]>}
 */
export const fetchGenres = () => api.get("/genre/").then((r) => r.data);

/**
 * @returns {Promise<Country[]>}
 */
export const fetchCountries = () => api.get("/country/").then((r) => r.data);

/* ---------- Favorites ---------- */

/**
 * @returns {Promise<Favorite>}
 */
export const fetchFavorites = () => api.get("/favorite/").then((r) => r.data);

/**
 * @param {{ film_id?: number|null, series_id?: number|null, cartoon_id?: number|null }} payload
 * @returns {Promise<FavoriteItem>}
 */
export const addFavorite = (payload) =>
  api.post("/favoriteitem/", payload).then((r) => r.data);

/**
 * @param {number} id
 * @returns {Promise<void>}
 */
export const removeFavorite = (id) => api.delete(`/favoriteitem/${id}/`);

/* ---------- Reviews ---------- */

/**
 * @param {Object} [params]
 * @returns {Promise<PageOf<Review>>}
 */
export const fetchReviews = (params) =>
  api.get("/review/", { params }).then((r) => r.data);

/**
 * @param {{ film_id?: number|null, series_id?: number|null, cartoon_id?: number|null, stars: number, text: string, parent?: number|null }} payload
 * @returns {Promise<Review>}
 */
export const createReview = (payload) =>
  api.post("/review/", payload).then((r) => r.data);

/**
 * @param {number} id
 * @returns {Promise<void>}
 */
export const deleteReview = (id) => api.delete(`/review/${id}/`);
