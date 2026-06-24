export interface User { id: number; username: string; email: string; first_name: string; last_name: string; avatar: string | null; phone_number: string; subscription_status: 'Free' | 'VIP'; }
export interface Genre { id: number; name: string; slug?: string; film_genre?: Film[]; }
export interface Country { id: number; country: string; }
export interface Person { id: number; first_name: string; last_name: string; person_image: string; role: string; }
export interface Film { id: number; title: string; description?: string; poster_image: string; year: number; duration?: number; language?: string; video?: string; trailer?: string; country: Country; genres: Genre[]; persons?: Person[]; access_type: string; rent_price?: string; is_published: boolean; views_count?: number; created_date?: string; get_avg_rating?: number; get_ratings_count?: number; }
export interface Season { id: number; season_number: number; title: string; year: number; series_list?: Series[]; }
export interface Series { id: number; season?: number; title: string; description?: string; image: string; year: number; country: Country; language?: string; trailer_url?: string; video?: string; genres: Genre[]; persons?: Person[]; access_type: string; is_published: boolean; views_count?: number; created_date?: string; }
export interface Cartoon { id: number; title: string; description?: string; cartoon_image: string; year: number; country: Country; language?: string; duration?: number; video?: string; trailer_url?: string; age_rating: string; genres: Genre[]; access_type: string; is_published: boolean; views_count?: number; created_date?: string; }
export interface FavoriteItem { id: number; film: Film | null; film_id?: number; series_id?: number; cartoon_id?: number; }
export interface Favorite { id: number; user: number; film_item: FavoriteItem[]; }
export interface Review { id: number; user_review: { id: number; first_name: string; last_name: string; avatar: string | null; }; film_id?: number; stars: number; text: string; parent: number | null; created_date: string; }
export interface PaginatedResponse<T> { count: number; next: string | null; previous: string | null; results: T[]; }
export interface LoginResponse { user: { username: string; email: string }; access: string; refresh: string; }
