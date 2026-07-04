# ТАСМА — фронтенд для Etno_Practic (movie)

React (Vite) + React Router + Axios фронтенд под твой Django REST API
(`Omurbek000/Etno_Practic/movie`): каталог фильмов/сериалов/мультфильмов
с фильтрами и пагинацией, страницы деталей с видео/трейлером/актёрами,
отзывы и оценки, избранное, регистрация/вход на JWT, профиль.

## 1. Куда положить папку

Скопируй папку `frontend` рядом с папкой `movie` (где `manage.py`), например:

```
твой_проект/
├── movie/        ← Django-бэкенд (уже есть)
└── frontend/      ← эта папка
```

## 2. Установка и запуск

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Откроется `http://localhost:5173`.

## 3. ОБЯЗАТЕЛЬНО: включи CORS на бэкенде

В `movie/settings.py` пакет `corsheaders` уже добавлен в `INSTALLED_APPS`,
но **миддлвара не подключена** — без неё браузер будет блокировать запросы
с `localhost:5173` к `localhost:8000`. Добавь в `movie/settings.py`:

```python
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",   # ← добавить первой/одной из первых
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

Без этого фикса фронтенд не получит ни одного ответа от API.

## 4. Языковой префикс

`movie/urls.py` оборачивает все роуты в `i18n_patterns`, а `LANGUAGE_CODE = 'ru-ru'`.
Поэтому реальные адреса — `http://127.0.0.1:8000/ru/film/`, `/ru/login/` и т.д.
Фронтенд уже это учитывает (`src/api/client.js`, переменная `VITE_API_LANG=ru` в `.env`).
Если поменяешь язык в Django — поменяй и `VITE_API_LANG`.

## 5. Запусти бэкенд

```bash
cd movie
python manage.py migrate
python manage.py runserver
```

Бэкенд должен быть на `http://127.0.0.1:8000` (адрес можно поменять в `frontend/.env`).

## 6. Известные ограничения текущего API (не фронтенда)

- **Отзывы не фильтруются по фильму/сериалу/мультфильму.** `ReviewViewSet`
  в `etno/views.py` не подключает `filterset_class`, и `ReviewSerializer`
  не отдаёт `film`/`series`/`cartoon` в ответе — поэтому `GET /review/?film_id=1`
  технически вернёт **все** отзывы. Фронтенд отправляет фильтр, но если
  увидишь чужие отзывы на странице фильма — это нужно чинить на бэкенде:
  добавить `filterset_fields = ['film_id', 'series_id', 'cartoon_id']` в
  `ReviewViewSet` (через `django_filters`) либо отдельные query-параметры
  в `get_queryset`.
- **Избранное показывает только фильмы.** `FavoriteItemSerializer` отдаёт
  вложенный объект только для `film` (поле `film = FilmListSerializer(...)`),
  для `series`/`cartoon` — только id на запись. Страница «Избранное»
  поэтому показывает карточки только для фильмов; сериалы/мультфильмы
  добавляются в избранное, но не отрисуются, пока в сериализатор не
  добавят `series`/`cartoon` как read-only вложенные поля.
- Детали фильма/сериала/мультфильма с `access_type != "Free"` доступны
  только пользователям с `subscription_status == "VIP"` — это логика
  `CheckSubscription`, фронтенд просто покажет ошибку, если доступа нет.

## 7. Структура проекта

```
src/
├── api/           axios-клиент с JWT + все запросы к API
├── context/       AuthContext (вход/регистрация/выход, текущий юзер)
├── components/     Navbar, PosterCard, FilterBar, Pagination,
│                    ReviewSection, FavoriteButton, States, ProtectedRoute
└── pages/          Home, Films/Series/Cartoons (+ Detail), Login,
                     Register, Profile, Favorites, NotFound
```

Дизайн: тёмная киношная тема со «стрипом» киноплёнки (перфорация по краям
постеров), Bebas Neue для заголовков, JetBrains Mono для цифр/мета.
