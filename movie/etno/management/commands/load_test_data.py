# etno/management/commands/load_test_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import datetime, timedelta
from etno.models import (
    UserProfile, Genre, Person, Country, Film, Series, Season, Cartoon,
    Subscription, Favorite, FavoriteItem, Review
)

class Command(BaseCommand):
    help = 'Заполняет БД тестовыми данными на трёх языках (ru, ky, uz)'

    def handle(self, *args, **options):
        self.stdout.write("Начинаю заполнение базы данных...")

        # --- 1. Пользователи (10 штук) + суперпользователь ---
        users_data = [
            {"username": "alisher_n", "first_name": "Алишер", "last_name": "Набиев", "phone": "+996700111111", "status": "VIP"},
            {"username": "ainura_k", "first_name": "Айнура", "last_name": "Калыкова", "phone": "+996700222222", "status": "Free"},
            {"username": "bekzat_m", "first_name": "Бекзат", "last_name": "Маматов", "phone": "+996700333333", "status": "VIP"},
            {"username": "chinara_t", "first_name": "Чинара", "last_name": "Токтогулова", "phone": "+996700444444", "status": "Free"},
            {"username": "ermek_s", "first_name": "Эрмек", "last_name": "Сагынбаев", "phone": "+996700555555", "status": "VIP"},
            {"username": "gulnara_j", "first_name": "Гульнара", "last_name": "Жумабекова", "phone": "+996700666666", "status": "Free"},
            {"username": "kanat_u", "first_name": "Канат", "last_name": "Усубалиев", "phone": "+996700777777", "status": "VIP"},
            {"username": "maya_z", "first_name": "Майя", "last_name": "Закирова", "phone": "+996700888888", "status": "Free"},
            {"username": "nurlan_b", "first_name": "Нурлан", "last_name": "Байбосунов", "phone": "+996700999999", "status": "VIP"},
            {"username": "zhibek_r", "first_name": "Жибек", "last_name": "Рыскулова", "phone": "+996701000000", "status": "Free"},
        ]

        users = []
        for data in users_data:
            user, created = UserProfile.objects.get_or_create(
                username=data["username"],
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "phone_number": data["phone"],
                    "subscription_status": data["status"],
                    "password": make_password("admin"),
                    "email": f"{data['username']}@example.com"
                }
            )
            users.append(user)
            self.stdout.write(f"Пользователь {user.username} создан/найден")

        # Суперпользователь
        admin, _ = UserProfile.objects.get_or_create(
            username="admin",
            defaults={
                "first_name": "Admin",
                "last_name": "Adminov",
                "is_superuser": True,
                "is_staff": True,
                "password": make_password("admin"),
                "email": "admin@example.com"
            }
        )
        self.stdout.write("Суперпользователь admin создан (пароль: admin)")

        # --- 2. Жанры (на трёх языках) ---
        genres_data = [
            {"ru": "Комедия", "ky": "Комедия", "uz": "Komediya", "slug": "comedy"},
            {"ru": "Драма", "ky": "Драма", "uz": "Drama", "slug": "drama"},
            {"ru": "Боевик", "ky": "Боевик", "uz": "Jangari", "slug": "action"},
            {"ru": "Фантастика", "ky": "Фантастика", "uz": "Fantastika", "slug": "sci-fi"},
            {"ru": "Ужасы", "ky": "Үркүтүү", "uz": "Qo‘rqinchli", "slug": "horror"},
            {"ru": "Романтика", "ky": "Романтика", "uz": "Romantika", "slug": "romance"},
            {"ru": "Приключения", "ky": "Приключения", "uz": "Sarguzasht", "slug": "adventure"},
            {"ru": "Детектив", "ky": "Детектив", "uz": "Detektiv", "slug": "detective"},
            {"ru": "Мелодрама", "ky": "Мелодрама", "uz": "Melodrama", "slug": "melodrama"},
            {"ru": "Криминал", "ky": "Криминал", "uz": "Jinoyat", "slug": "crime"},
        ]
        genres = []
        for g in genres_data:
            genre, _ = Genre.objects.get_or_create(
                slug=g["slug"],
                defaults={
                    "name_ru": g["ru"],
                    "name_ky": g["ky"],
                    "name_uz": g["uz"]
                }
            )
            genres.append(genre)
            self.stdout.write(f"Жанр {genre.name_ru} создан")

        # --- 3. Страны (на трёх языках) ---
        countries_data = [
            {"ru": "США", "ky": "АКШ", "uz": "AQSh"},
            {"ru": "Россия", "ky": "Орусия", "uz": "Rossiya"},
            {"ru": "Великобритания", "ky": "Улуу Британия", "uz": "Buyuk Britaniya"},
            {"ru": "Кыргызстан", "ky": "Кыргызстан", "uz": "Qirg‘iziston"},
            {"ru": "Казахстан", "ky": "Казакстан", "uz": "Qozog‘iston"},
            {"ru": "Южная Корея", "ky": "Түштүк Корея", "uz": "Janubiy Koreya"},
            {"ru": "Япония", "ky": "Япония", "uz": "Yaponiya"},
            {"ru": "Франция", "ky": "Франция", "uz": "Fransiya"},
            {"ru": "Германия", "ky": "Германия", "uz": "Germaniya"},
            {"ru": "Турция", "ky": "Түркия", "uz": "Turkiya"},
        ]
        countries = []
        for c in countries_data:
            country, _ = Country.objects.get_or_create(
                country_ru=c["ru"],
                defaults={
                    "country_ky": c["ky"],
                    "country_uz": c["uz"]
                }
            )
            countries.append(country)
            self.stdout.write(f"Страна {country.country_ru} создана")

        # --- 4. Персоны (актёры, режиссёры) ---
        persons_data = [
            {"first": "Киану", "last": "Ривз", "role": "Actor", "image": ""},
            {"first": "Том", "last": "Хэнкс", "role": "Actor", "image": ""},
            {"first": "Скарлетт", "last": "Йоханссон", "role": "Actress", "image": ""},
            {"first": "Кристофер", "last": "Нолан", "role": "Director", "image": ""},
            {"first": "Квентин", "last": "Тарантино", "role": "Director", "image": ""},
            {"first": "Марго", "last": "Робби", "role": "Actress", "image": ""},
            {"first": "Леонардо", "last": "ДиКаприо", "role": "Actor", "image": ""},
            {"first": "Актан", "last": "Арым Кубат", "role": "both", "image": ""},
            {"first": "Тынчтык", "last": "Абылкасымов", "role": "Actor", "image": ""},
            {"first": "Жылдыз", "last": "Акматова", "role": "Actress", "image": ""},
        ]
        persons = []
        for p in persons_data:
            person, _ = Person.objects.get_or_create(
                first_name=p["first"],
                last_name=p["last"],
                defaults={"role": p["role"]}
            )
            persons.append(person)
            self.stdout.write(f"Персона {person.first_name} {person.last_name} создана")

        # --- 5. Фильмы (по 10, с переводами) ---
        films_data = [
            {
                "title_ru": "Матрица", "title_ky": "Матрица", "title_uz": "Matritsa",
                "desc_ru": "Хакер Нео узнаёт реальность", "desc_ky": "Хакер Нео чыныгы дүйнөнү тааныйт", "desc_uz": "Xaker Neo haqiqatni biladi",
                "year": 1999, "country": countries[0], "duration": 136, "lang": "Russian",
                "access": "Free", "rent_price": None
            },
            {
                "title_ru": "Форрест Гамп", "title_ky": "Форрест Гамп", "title_uz": "Forrest Gamp",
                "desc_ru": "История парня из Алабамы", "desc_ky": "Алабамадан келген жигиттин тарыхы", "desc_uz": "Alabamalik yigitning hikoyasi",
                "year": 1994, "country": countries[0], "duration": 142, "lang": "Russian", "access": "Subscription", "rent_price": None
            },
            {
                "title_ru": "Один дома", "title_ky": "Үйдө жалгыз", "title_uz": "Uyda yolg‘iz",
                "desc_ru": "Мальчик защищает дом от грабителей", "desc_ky": "Бала үйдү каракчылардан коргойт", "desc_uz": "Bola uyni o‘g‘rilardan himoya qiladi",
                "year": 1990, "country": countries[0], "duration": 103, "lang": "Russian", "access": "Free", "rent_price": None
            },
            {
                "title_ru": "Начало", "title_ky": "Башталыш", "title_uz": "Boshlanish",
                "desc_ru": "Воровство снов", "desc_ky": "Түштөрдү уурдоо", "desc_uz": "Tushlarni o‘g‘irlash",
                "year": 2010, "country": countries[0], "duration": 148, "lang": "Other", "access": "Rent", "rent_price": 5.99
            },
            {
                "title_ru": "Криминальное чтиво", "title_ky": "Кылмыштуу окуя", "title_uz": "Jinoyat hikoyasi",
                "desc_ru": "Переплетение историй", "desc_ky": "Окуялардын байланышы", "desc_uz": "Hikoyalarning bog‘lanishi",
                "year": 1994, "country": countries[0], "duration": 154, "lang": "Other", "access": "Subscription", "rent_price": None
            },
            {
                "title_ru": "Титаник", "title_ky": "Титаник", "title_uz": "Titanik",
                "desc_ru": "Любовь на тонущем корабле", "desc_ky": "Батып бараткан кемедеги сүйүү", "desc_uz": "Cho‘kayotgan kemadagi sevgi",
                "year": 1997, "country": countries[0], "duration": 195, "lang": "Russian", "access": "Free", "rent_price": None
            },
            {
                "title_ru": "Салам, Нью-Йорк", "title_ky": "Салам, Нью-Йорк", "title_uz": "Salom, Nyu-York",
                "desc_ru": "Кыргызская драма", "desc_ky": "Кыргыз драмасы", "desc_uz": "Qirg‘iz dramasi",
                "year": 2021, "country": countries[3], "duration": 90, "lang": "Kyrgyz", "access": "Free", "rent_price": None
            },
            {
                "title_ru": "Аманат", "title_ky": "Аманат", "title_uz": "Amanat",
                "desc_ru": "Исторический фильм", "desc_ky": "Тарыхый фильм", "desc_uz": "Tarixiy film",
                "year": 2015, "country": countries[3], "duration": 120, "lang": "Kyrgyz", "access": "Free", "rent_price": None
            },
            {
                "title_ru": "Паразиты", "title_ky": "Паразиттер", "title_uz": "Parazitlar",
                "desc_ru": "Оскароносная драма", "desc_ky": "Оскар алган драма", "desc_uz": "Oskar mukofotiga sazovor bo‘lgan drama",
                "year": 2019, "country": countries[5], "duration": 132, "lang": "Other", "access": "Subscription", "rent_price": None
            },
            {
                "title_ru": "Побег из Шоушенка", "title_ky": "Шоушенктен качуу", "title_uz": "Shoushenkdan qochish",
                "desc_ru": "Дружба и надежда", "desc_ky": "Достук жана үмүт", "desc_uz": "Do‘stlik va umid",
                "year": 1994, "country": countries[0], "duration": 142, "lang": "Russian", "access": "Free", "rent_price": None
            },
        ]
        films = []
        for f in films_data:
            film, _ = Film.objects.get_or_create(
                title_ru=f["title_ru"],
                defaults={
                    "title_ky": f["title_ky"],
                    "title_uz": f["title_uz"],
                    "description_ru": f["desc_ru"],
                    "description_ky": f["desc_ky"],
                    "description_uz": f["desc_uz"],
                    "year": f["year"],
                    "country": f["country"],
                    "duration": f["duration"],
                    "language": f["lang"],
                    "access_type": f["access"],
                    "rent_price": f["rent_price"],
                    "is_published": True,
                }
            )
            # Добавляем жанры и персон
            film.genres.add(*genres[:3])
            film.persons.add(*persons[:4])
            films.append(film)
            self.stdout.write(f"Фильм {film.title_ru} создан")

        # --- 6. Сериалы (10) и сезоны (по 2-3 на каждый) ---
        series_data = [
            {"ru": "Игра престолов", "ky": "Тактылар оюну", "uz": "Taxtlar o‘yini", "year": 2011, "country": countries[0], "lang": "Other"},
            {"ru": "Во все тяжкие", "ky": "Бардык оор жолдор", "uz": "Hamma og‘ir yo‘llar", "year": 2008, "country": countries[0], "lang": "Other"},
            {"ru": "Шерлок", "ky": "Шерлок", "uz": "Sherlok", "year": 2010, "country": countries[2], "lang": "Russian"},
            {"ru": "Черное зеркало", "ky": "Кара күзгү", "uz": "Qora ko‘zgu", "year": 2011, "country": countries[2], "lang": "Other"},
            {"ru": "Кыргыз жыгачы", "ky": "Кыргыз жыгачы", "uz": "Qirg‘iz yog‘ochi", "year": 2020, "country": countries[3], "lang": "Kyrgyz"},
            {"ru": "Кардашьяндар", "ky": "Кардашьяндар", "uz": "Kardashyanlar", "year": 2007, "country": countries[0], "lang": "Other"},
            {"ru": "Ведьмак", "ky": "Ведьмак", "uz": "Vedmak", "year": 2019, "country": countries[0], "lang": "Other"},
            {"ru": "Очень странные дела", "ky": "Абдан кызык окуялар", "uz": "Juda g‘alati hodisalar", "year": 2016, "country": countries[0], "lang": "Other"},
            {"ru": "Мандалорец", "ky": "Мандалорец", "uz": "Mandalorets", "year": 2019, "country": countries[0], "lang": "Other"},
            {"ru": "Бумажный дом", "ky": "Кагаз үй", "uz": "Qog‘oz uy", "year": 2017, "country": countries[4], "lang": "Russian"},
        ]
        series_list = []
        for s in series_data:
            series, _ = Series.objects.get_or_create(
                title_ru=s["ru"],
                defaults={
                    "title_ky": s["ky"],
                    "title_uz": s["uz"],
                    "description_ru": f"Описание {s['ru']}",
                    "description_ky": f"Сүрөттөмө {s['ky']}",
                    "description_uz": f"Tavsif {s['uz']}",
                    "year": s["year"],
                    "country": s["country"],
                    "language": s["lang"],
                    "access_type": "Free",
                    "is_published": True,
                }
            )
            series.genres.add(*genres[2:5])
            series.persons.add(*persons[0:2])
            series_list.append(series)
            # Добавляем сезоны
            for num in range(1, 4):
                season, _ = Season.objects.get_or_create(
                    series=series,
                    season_number=num,
                    defaults={
                        "title_ru": f"Сезон {num}",
                        "title_ky": f"{num}-сезон",
                        "title_uz": f"{num}-mavsum",
                        "year": s["year"] + num - 1
                    }
                )
            self.stdout.write(f"Сериал {series.title_ru} создан с сезонами")

        # --- 7. Мультфильмы (10) ---
        cartoons_data = [
            {"ru": "Король Лев", "ky": "Арстан падыша", "uz": "Arslon podshoh", "year": 1994, "duration": 88, "age": "0+"},
            {"ru": "Шрек", "ky": "Шрек", "uz": "Shrek", "year": 2001, "duration": 90, "age": "6+"},
            {"ru": "Холодное сердце", "ky": "Муздак жүрөк", "uz": "Sovuq yurak", "year": 2013, "duration": 102, "age": "6+"},
            {"ru": "Головоломка", "ky": "Баш катырма", "uz": "Boshqotirma", "year": 2015, "duration": 95, "age": "6+"},
            {"ru": "В поисках Немо", "ky": "Немону издөө", "uz": "Nemonu qidirish", "year": 2003, "duration": 100, "age": "0+"},
            {"ru": "Как приручить дракона", "ky": "Ажыдаарды колго үйрөтүү", "uz": "Ajdarni qo‘lga o‘rgatish", "year": 2010, "duration": 98, "age": "12+"},
            {"ru": "Зверопой", "ky": "Айбандар ыры", "uz": "Hayvonlar qo‘shig‘i", "year": 2016, "duration": 108, "age": "0+"},
            {"ru": "Соник в кино", "ky": "Соник тасмада", "uz": "Sonik kino da", "year": 2020, "duration": 99, "age": "6+"},
            {"ru": "Тачки", "ky": "Тачкылар", "uz": "Machinalar", "year": 2006, "duration": 117, "age": "0+"},
            {"ru": "Рататуй", "ky": "Рататуй", "uz": "Ratatuy", "year": 2007, "duration": 111, "age": "0+"},
        ]
        for c in cartoons_data:
            cartoon, _ = Cartoon.objects.get_or_create(
                title_ru=c["ru"],
                defaults={
                    "title_ky": c["ky"],
                    "title_uz": c["uz"],
                    "description_ru": f"Описание {c['ru']}",
                    "description_ky": f"Сүрөттөмө {c['ky']}",
                    "description_uz": f"Tavsif {c['uz']}",
                    "year": c["year"],
                    "country": countries[0],
                    "language": "Russian",
                    "duration": c["duration"],
                    "age_rating": c["age"],
                    "access_type": "Free",
                    "is_published": True,
                }
            )
            cartoon.genres.add(*genres[0:2])
            self.stdout.write(f"Мультфильм {cartoon.title_ru} создан")

        # --- 8. Подписки для пользователей ---
        for i, user in enumerate(users[:5]):
            end_date = timezone.now() + timedelta(days=30)
            Subscription.objects.get_or_create(
                user=user,
                plan="monthly",
                defaults={
                    "end_date": end_date,
                    "is_activ": True,
                    "price": 500
                }
            )
        self.stdout.write("Подписки созданы")

        # --- 9. Избранное для каждого пользователя ---
        for user in users[:5]:
            fav, _ = Favorite.objects.get_or_create(user=user)
            for film in films[:3]:
                FavoriteItem.objects.get_or_create(watchlist=fav, film=film)
            for series in series_list[:2]:
                FavoriteItem.objects.get_or_create(watchlist=fav, series=series)
            for cartoon in Cartoon.objects.all()[:2]:
                FavoriteItem.objects.get_or_create(watchlist=fav, cartoon=cartoon)
        self.stdout.write("Избранное заполнено")

        # --- 10. Отзывы ---
        for i, user in enumerate(users):
            if i % 2 == 0:
                film = films[i % len(films)]
                Review.objects.get_or_create(
                    user=user,
                    film=film,
                    defaults={
                        "stars": i % 10 + 1,
                        "text": f"Отличный фильм! Очень понравился. (Оценка {i%10+1})"
                    }
                )
            else:
                series = series_list[i % len(series_list)]
                Review.objects.get_or_create(
                    user=user,
                    series=series,
                    defaults={
                        "stars": i % 10 + 1,
                        "text": f"Сериал супер, рекомендую! (Оценка {i%10+1})"
                    }
                )
        self.stdout.write("Отзывы добавлены")

        self.stdout.write(self.style.SUCCESS("База данных успешно заполнена тестовыми данными!"))