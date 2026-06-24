# ТЗ для фронтенда: онлайн-кинотеатр «Театр Етно»

Стиль интерфейса: **iOS Glassmorphism + Black-Gold-Purple Premium UI**
Backend: REST API (автор API — Aziat)

---



## 4. Интеграция с API

### 4.1 Авторизация

**Регистрация**
```
POST /register/
Body: { email, username, password, phone_number }
→ 201 CREATED, возвращает данные пользователя (без токенов)
```

**Логин**
```
POST /login/
Body: { username, password }
→ { user: { username, email }, access, refresh }
```

**Логаут**
```
POST /logout/
Body: { refresh }
```

**Требования к фронтенду:**
- `access` токен хранить в памяти приложения (React Context), не в localStorage в чистом виде — допустимо хранить `refresh` в `httpOnly` cookie или localStorage, если backend не поддерживает cookie
- При 401 от любого запроса — пытаться обновить токен через refresh, при неудаче — разлогинивать пользователя
- При логауте — обязательно отправлять `refresh` на `/logout/`, затем чистить состояние

```js
// api/client.js — пример interceptor'а
client.interceptors.response.use(
  res => res,
  async (error) => {
    if (error.response?.status === 401 && !error.config._retry) {
      error.config._retry = true;
      const newAccess = await refreshToken();
      error.config.headers.Authorization = `Bearer ${newAccess}`;
      return client(error.config);
    }
    return Promise.reject(error);
  }
);
```

### 4.2 Профиль пользователя
```
GET    /users/        — профиль текущего пользователя
GET    /users/{id}/   — детали
PUT    /users/{id}/   — обновление
DELETE /users/{id}/   — удаление
```
Поля: `id, username, first_name, last_name, email, avatar, phone_number, subscription_status, date_register`

### 4.3 Фильмы
```
GET /film/        — список (фильтры: год, жанр, страна; пагинация)
GET /film/{id}/   — детали (требует подписку, если access_type = paid)
```
Список: `id, title, poster_image, year, access_type, country, genres, get_avg_rating, get_ratings_count`
Детали: `title, description, poster_image, year, language, duration, video, trailer, genres, persons, rent_price, views_count, created_date, country`

### 4.4 Жанры / Персоны
```
GET /genre/         GET /genre/{id}/    → { name, film_genre[] }
GET /person/        GET /person/{id}/
```

### 4.5 Сериалы / Сезоны
```
GET /series/        GET /series/{id}/   (требует подписку)
GET /season/        GET /season/{id}/   → { season_number, title, year, series_list[] }
```

### 4.6 Мультфильмы
```
GET /cartoon/       GET /cartoon/{id}/  (требует подписку)
```

### 4.7 Подписки
```
/subscription/ — ModelViewSet: list / create / update / delete
```

### 4.8 Избранное
```
GET /favorite/
→ { id, user, film_item: [{ id, film, series_id, cartoon_id }] }

POST /favoriteitem/
Body: { film_id } | { series_id } | { cartoon_id }
(дубликаты запрещены backend'ом — обрабатывать ошибку на фронте тостом)

DELETE /favoriteitem/{id}/
```

### 4.9 Отзывы
```
/review/ — ModelViewSet
POST: { film_id, stars, text }
Ответ включает: user_review, stars, text, created_date
```

---

## 5. Страницы фронтенда

| Страница | Содержимое |
|---|---|
| Главная | подборки: популярные, новинки, хедлайнер |
| Каталог фильмов | фильтры (год/жанр/страна), пагинация, сетка карточек |
| Страница фильма | описание, трейлер, актёры, отзывы, кнопка «В избранное» |
| Сериалы / Мультфильмы | аналогично каталогу фильмов, у сериалов — список сезонов/эпизодов |
| Профиль | данные пользователя, аватар, статус подписки, редактирование |
| Избранное | список добавленных фильмов/серий/мультфильмов с возможностью удалить |
| Авторизация | формы регистрации и входа |

---

## 6. Дизайн-система

### 6.1 Цветовая палитра

```css
:root {
  --bg-dark: #050509;
  --gold: #f5c76a;
  --gold-soft: #f1b24a;
  --purple: #a855f7;
  --purple-soft: #c084fc;
  --text-main: #f9fafb;
  --text-secondary: rgba(249, 250, 251, 0.6);
}
```

### 6.2 Фон приложения

Глубокий тёмный фон с мягкими золотыми и фиолетовыми бликами (эффект «iPhone Dynamic Island vibes»).

```css
body {
  margin: 0;
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", system-ui, sans-serif;
  color: var(--text-main);
  background:
    radial-gradient(circle at 10% 20%, rgba(248, 191, 82, 0.18) 0, transparent 55%),
    radial-gradient(circle at 80% 10%, rgba(168, 85, 247, 0.22) 0, transparent 55%),
    radial-gradient(circle at 50% 90%, rgba(192, 132, 252, 0.18) 0, transparent 55%),
    var(--bg-dark);
}
```

### 6.3 Стеклянные карточки (Glass Panels)

Базовый «стеклянный» контейнер — используется для форм, модалок, инфо-блоков.

```css
.glass-card {
  background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(15,15,20,0.85));
  border-radius: 24px;
  padding: 24px 22px;
  border: 1px solid rgba(255,255,255,0.16);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  box-shadow:
    0 18px 40px rgba(0,0,0,0.75),
    0 0 0 1px rgba(255,255,255,0.04);
}
```

### 6.4 Заголовки (Gold Glow Titles)

```css
.glass-title {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: 0.03em;
  color: var(--gold);
  text-shadow:
    0 0 10px rgba(245,199,106,0.6),
    0 0 24px rgba(168,85,247,0.4);
}
```

### 6.5 Поля ввода

```css
.glass-input {
  width: 100%;
  margin-top: 14px;
  background: rgba(10,10,15,0.8);
  border-radius: 14px;
  border: 1px solid rgba(192,132,252,0.5);
  padding: 12px 16px;
  color: var(--text-main);
  outline: none;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  transition: 0.25s;
}
.glass-input::placeholder { color: rgba(249,250,251,0.45); }
.glass-input:focus {
  border-color: var(--purple-soft);
  box-shadow:
    0 0 14px rgba(192,132,252,0.9),
    0 0 4px rgba(245,199,106,0.4);
}
```

### 6.6 Кнопки

```css
.glass-button {
  margin-top: 18px;
  width: 100%;
  border: none;
  border-radius: 16px;
  padding: 12px 18px;
  background: linear-gradient(135deg, var(--gold), var(--purple));
  color: #050509;
  font-weight: 600;
  cursor: pointer;
  box-shadow:
    0 12px 26px rgba(0,0,0,0.8),
    0 0 18px rgba(245,199,106,0.7);
  transition: 0.22s ease-out;
}
.glass-button:hover {
  transform: translateY(-2px);
  box-shadow:
    0 18px 36px rgba(0,0,0,0.9),
    0 0 24px rgba(192,132,252,0.9);
}
```

### 6.7 Карточка фильма (MovieCard) — стеклянная, в той же палитре

Карточка фильма в каталоге/подборках использует тот же стеклянный язык, что и `.glass-card`, но адаптирована под постер и метаданные фильма (`poster_image`, `title`, `get_avg_rating`, `access_type`).

```css
.movie-card {
  position: relative;
  border-radius: 18px;
  aspect-ratio: 2 / 3;
  overflow: hidden;
  cursor: pointer;
  background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(15,15,20,0.85));
  border: 1px solid rgba(255,255,255,0.16);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  box-shadow: 0 14px 30px rgba(0,0,0,0.6);
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}
.movie-card:hover {
  transform: translateY(-6px);
  border-color: rgba(245,199,106,0.5);
  box-shadow:
    0 0 26px rgba(245,199,106,0.45),
    0 0 40px rgba(168,85,247,0.25),
    0 16px 34px rgba(0,0,0,0.7);
}
.movie-card .poster {
  position: absolute; inset: 0;
  background-size: cover; background-position: center;
  opacity: 0.85;
}
.movie-card .poster::before {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(to top, rgba(5,5,9,0.92) 0%, rgba(5,5,9,0.1) 55%, transparent 100%);
}
.movie-card .badge-paid {
  position: absolute; top: 10px; left: 10px; z-index: 3;
  font-size: 10px; font-weight: 700;
  padding: 3px 9px; border-radius: 8px;
  background: linear-gradient(135deg, var(--gold), var(--purple));
  color: #050509;
}
.movie-card .rating {
  position: absolute; top: 10px; right: 10px; z-index: 3;
  font-size: 11px; font-weight: 700;
  padding: 3px 8px; border-radius: 20px;
  background: rgba(10,10,15,0.7);
  border: 1px solid rgba(245,199,106,0.4);
  color: var(--gold);
}
.movie-card .title {
  position: absolute; left: 0; right: 0; bottom: 0; z-index: 2;
  padding: 12px;
  font-size: 14px; font-weight: 600; color: var(--text-main);
}
.movie-card .play-button {
  position: absolute; top: 50%; left: 50%; z-index: 3;
  width: 42px; height: 42px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  background: rgba(245,199,106,0.18);
  border: 1px solid rgba(245,199,106,0.5);
  color: #fff;
  opacity: 0;
  transform: translate(-50%,-50%) scale(0.7);
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.movie-card:hover .play-button { opacity: 1; transform: translate(-50%,-50%) scale(1); }
```

```jsx
export function MovieCard({ title, posterImage, rating, accessType, onPlay }) {
  return (
    <article className="movie-card" tabIndex={0} onClick={onPlay}>
      <div className="poster" style={{ backgroundImage: `url(${posterImage})` }}>
        {accessType === 'paid' && <span className="badge-paid">Подписка</span>}
        {rating != null && <span className="rating">★ {rating.toFixed(1)}</span>}
        <button className="play-button" aria-label={`Смотреть «${title}»`}>▶</button>
        <h3 className="title">{title}</h3>
      </div>
    </article>
  );
}
```

---

## 7. Готовые базовые UI-компоненты

```jsx
// components/ui/GlassCard.jsx
export function GlassCard({ children }) {
  return <div className="glass-card">{children}</div>;
}

// components/ui/GlassTitle.jsx
export function GlassTitle({ children }) {
  return <h1 className="glass-title">{children}</h1>;
}

// components/ui/GlassInput.jsx
export function GlassInput(props) {
  return <input className="glass-input" {...props} />;
}

// components/ui/GlassButton.jsx
export function GlassButton({ children, ...props }) {
  return (
    <button className="glass-button" {...props}>
      {children}
    </button>
  );
}
```

### Пример экрана логина

```jsx
import { GlassCard, GlassTitle, GlassInput, GlassButton } from "./components/ui";
import { login } from "./api/auth";

export default function LoginScreen() {
  const [form, setForm] = useState({ username: "", password: "" });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const { access, refresh, user } = await login(form);
    // сохранить access в контексте, refresh — согласно п.4.1
  };

  return (
    <div className="screen-center">
      <GlassCard>
        <GlassTitle>Театр Етно</GlassTitle>
        <form onSubmit={handleSubmit}>
          <GlassInput
            placeholder="Имя пользователя"
            value={form.username}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
          />
          <GlassInput
            placeholder="Пароль"
            type="password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />
          <GlassButton type="submit">Войти</GlassButton>
        </form>
      </GlassCard>
    </div>
  );
}
```

---

## 8. Нефункциональные требования

- **Адаптивность**: каталог — `grid-template-columns: repeat(auto-fill, minmax(180px, 1fr))`; на мобильных — 2 колонки, формы авторизации — `100%` ширины контейнера
- **Доступность**: все интерактивные элементы фокусируемы, `aria-label` на иконных кнопках, контраст текста на постерах не ниже 4.5:1
- **`prefers-reduced-motion`**: отключать `transform`/анимации блика для пользователей с этой настройкой
- **Состояния загрузки**: skeleton-карточки на месте `.movie-card` пока грузится список с API
- **Обработка ошибок API**: тосты/алерты на 400/401/403/404, отдельная обработка «фильм уже в избранном» (дубликат) и «требуется подписка» (403 на платный контент)
- **Производительность**: `backdrop-filter` — дорогая операция, ограничивать количество карточек с блюром одновременно на экране (виртуализация длинных списков)

---

## 9. Чеклист для разработчика

1. Настроить `api/client.js` с JWT interceptor'ами (access + refresh)
2. Реализовать `AuthContext` (login/logout/register, хранение текущего пользователя)
3. Собрать базовые UI-компоненты (`GlassCard`, `GlassTitle`, `GlassInput`, `GlassButton`)
4. Реализовать `MovieCard` и подключить к `/film/`
5. Собрать страницы: Главная → Каталог → Страница фильма → Профиль → Избранное → Авторизация
6. Повторить логику `MovieCard`/каталога для `/series/` и `/cartoon/`
7. Подключить отзывы (`/review/`) на странице фильма
8. Протестировать сценарий «контент paid без подписки» → редирект/предложение оформить подписку
