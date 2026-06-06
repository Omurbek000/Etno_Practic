# ваше_приложение/management/commands/populate_db.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

from ...models import (
    UserProfile, Genre, Person, Country, Film, Season, Series, Cartoon,
    Subscription, Favorite, FavoriteItem, Review
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with test data (10 items per model, 3 languages)'

    def handle(self, *args, **options):
        self.stdout.write('Clearing old data...')
        self.clear_data()
        self.stdout.write('Creating new data...')

        # 1. Пользователи
        users = self.create_users()

        # 2. Жанры, страны, персоны
        genres = self.create_genres()
        countries = self.create_countries()
        persons = self.create_persons()

        # 3. Фильмы
        films = self.create_films(genres, countries, persons)

        # 4. Сезоны и серии
        seasons = self.create_seasons()
        series_list = self.create_series(seasons, genres, countries, persons)

        # 5. Мультфильмы (без persons)
        cartoons = self.create_cartoons(genres, countries)

        # 6. Подписки
        self.create_subscriptions(users)

        # 7. Избранное
        favorites = self.create_favorites(users)
        self.create_favorite_items(favorites, films, series_list, cartoons)

        # 8. Отзывы
        self.create_reviews(users, films, series_list, cartoons)

        self.stdout.write(self.style.SUCCESS('Database successfully populated!'))

    def clear_data(self):
        Review.objects.all().delete()
        FavoriteItem.objects.all().delete()
        Favorite.objects.all().delete()
        Subscription.objects.all().delete()
        Cartoon.objects.all().delete()
        Series.objects.all().delete()
        Season.objects.all().delete()
        Film.objects.all().delete()
        Person.objects.all().delete()
        Country.objects.all().delete()
        Genre.objects.all().delete()
        User.objects.all().delete()

    def create_users(self):
        usernames = [
            'anna', 'ivan', 'maria', 'alexey', 'elena',
            'dmitry', 'olga', 'sergey', 'tatyana', 'nikolay'
        ]
        users = []
        for username in usernames:
            user = User.objects.create_user(
                username=username,
                password='admin',
                first_name=username.capitalize(),
                last_name='Testov',
                email=f'{username}@example.com',
                phone_number=f'+996{random.randint(700000000, 799999999)}',
                subscription_status=random.choice(['Free', 'VIP']),
                subscription_end=timezone.now() + timedelta(days=random.randint(0, 365))
            )
            users.append(user)
            self.stdout.write(f'  Created user: {username}')
        return users

    def create_genres(self):
        genres_data = [
            {'ru': 'Боевик', 'ky': 'Экшн', 'uz': 'Jangari'},
            {'ru': 'Комедия', 'ky': 'Комедия', 'uz': 'Komediya'},
            {'ru': 'Драма', 'ky': 'Драма', 'uz': 'Drama'},
            {'ru': 'Ужасы', 'ky': 'Коркунучтуу', 'uz': 'Qo‘rqinchli'},
            {'ru': 'Фантастика', 'ky': 'Фантастика', 'uz': 'Fantastika'},
            {'ru': 'Романтика', 'ky': 'Романтика', 'uz': 'Romanika'},
            {'ru': 'Триллер', 'ky': 'Триллер', 'uz': 'Triller'},
            {'ru': 'Детектив', 'ky': 'Детектив', 'uz': 'Detektiv'},
            {'ru': 'Приключения', 'ky': 'Сагарга', 'uz': 'Sarguzasht'},
            {'ru': 'Мелодрама', 'ky': 'Мелодрама', 'uz': 'Melodrama'}
        ]
        genres = []
        for data in genres_data:
            genre = Genre.objects.create(
                name_ru=data['ru'],
                name_ky=data['ky'],
                name_uz=data['uz'],
                slug=data['ru'].lower()
            )
            genres.append(genre)
            self.stdout.write(f'  Created genre: {genre.name_ru}')
        return genres

    def create_countries(self):
        countries_data = [
            {'ru': 'США', 'ky': 'АКШ', 'uz': 'AQSh'},
            {'ru': 'Россия', 'ky': 'Орусия', 'uz': 'Rossiya'},
            {'ru': 'Великобритания', 'ky': 'Улуу Британия', 'uz': 'Buyuk Britaniya'},
            {'ru': 'Франция', 'ky': 'Франция', 'uz': 'Fransiya'},
            {'ru': 'Германия', 'ky': 'Германия', 'uz': 'Germaniya'},
            {'ru': 'Италия', 'ky': 'Италия', 'uz': 'Italiya'},
            {'ru': 'Япония', 'ky': 'Япония', 'uz': 'Yaponiya'},
            {'ru': 'Корея', 'ky': 'Корея', 'uz': 'Koreya'},
            {'ru': 'Индия', 'ky': 'Индия', 'uz': 'Hindiston'},
            {'ru': 'Казахстан', 'ky': 'Казакстан', 'uz': 'Qozog‘iston'}
        ]
        countries = []
        for data in countries_data:
            country = Country.objects.create(
                country_ru=data['ru'],
                country_ky=data['ky'],
                country_uz=data['uz']
            )
            countries.append(country)
            self.stdout.write(f'  Created country: {country.country_ru}')
        return countries

    def create_persons(self):
        persons_data = [
            ('Леонардо', 'ДиКаприо', 'Actor'),
            ('Киану', 'Ривз', 'Actor'),
            ('Скарлетт', 'Йоханссон', 'Actress'),
            ('Кристофер', 'Нолан', 'Director'),
            ('Квентин', 'Тарантино', 'Director'),
            ('Мерил', 'Стрип', 'Actress'),
            ('Том', 'Хэнкс', 'Actor'),
            ('Эмма', 'Уотсон', 'Actress'),
            ('Дэвид', 'Финчер', 'Director'),
            ('Анжелина', 'Джоли', 'both')
        ]
        persons = []
        for first, last, role in persons_data:
            person = Person.objects.create(
                first_name=first,
                last_name=last,
                role=role,
                person_image='person_image/default.jpg'
            )
            persons.append(person)
            self.stdout.write(f'  Created person: {first} {last} ({role})')
        return persons

    def create_films(self, genres, countries, persons):
        films_data = [
            ('Начало', 'Гениальный вор крадет идеи из снов...', 2010, 'Кыргыз', 148, 'https://youtu.be/example1'),
            ('Матрица', 'Программист узнает, что мир - симуляция...', 1999, 'Russian', 136, 'https://youtu.be/example2'),
            ('Бойцовский клуб', 'Офисный работник и мыловар создают подпольный клуб...', 1999, 'Russian', 139, 'https://youtu.be/example3'),
            ('Форрест Гамп', 'История человека с низким IQ, который повлиял на историю США...', 1994, 'Russian', 142, 'https://youtu.be/example4'),
            ('Зеленая книга', 'Итальянский вышибала возит черного пианиста по югу США...', 2018, 'Russian', 130, 'https://youtu.be/example5'),
            ('Остров проклятых', 'Два маршала расследуют исчезновение пациентки в психиатрической больнице...', 2010, 'Russian', 138, 'https://youtu.be/example6'),
            ('Интерстеллар', 'Путешествие через червоточину в поисках новой планеты...', 2014, 'Russian', 169, 'https://youtu.be/example7'),
            ('Джокер', 'История становления культового злодея...', 2019, 'Russian', 122, 'https://youtu.be/example8'),
            ('Паразиты', 'Семья бедняков внедряется в дом богатых...', 2019, 'Кыргыз', 132, 'https://youtu.be/example9'),
            ('Довод', 'Шпион использует инверсию времени для предотвращения Третьей мировой...', 2020, 'Russian', 150, 'https://youtu.be/example10')
        ]
        films = []
        access_types = ['Free', 'Subscription', 'Rent']
        for title_ru, desc_ru, year, lang, dur, trailer in films_data:
            title_ky = f'{title_ru} (ky)'
            title_uz = f'{title_ru} (uz)'
            desc_ky = f'{desc_ru} (кыргызча котормосу)'
            desc_uz = f'{desc_ru} (o‘zbekcha tarjimasi)'
            access = random.choice(access_types)
            rent_price = random.randint(5, 20) if access == 'Rent' else None
            film = Film.objects.create(
                title_ru=title_ru,
                title_ky=title_ky,
                title_uz=title_uz,
                description_ru=desc_ru,
                description_ky=desc_ky,
                description_uz=desc_uz,
                year=year,
                country=random.choice(countries),
                duration=dur,
                language=lang,
                trailer=trailer,
                access_type=access,
                rent_price=rent_price,
                is_published=True,
                views_count=random.randint(0, 10000),
                poster_image='poster_image/default.jpg',
                video='film_video/default.mp4'
            )
            film.genres.set(random.sample(genres, random.randint(1, 3)))
            film.persons.set(random.sample(persons, random.randint(2, 4)))
            films.append(film)
            self.stdout.write(f'  Created film: {film.title_ru}')
        return films

    def create_seasons(self):
        seasons = []
        for i in range(1, 11):
            title_ru = f'Сезон {i}'
            season = Season.objects.create(
                season_number=i,
                title_ru=title_ru,
                title_ky=f'{title_ru} (ky)',
                title_uz=f'{title_ru} (uz)',
                year=2020 + (i % 5)
            )
            seasons.append(season)
            self.stdout.write(f'  Created season: {season.title_ru}')
        return seasons

    def create_series(self, seasons, genres, countries, persons):
        series_list = []
        access_types = ['Free', 'Subscription', 'Rent']
        for i in range(1, 11):
            title_ru = f'Серия {i}'
            desc_ru = f'Описание серии {i}'
            series = Series.objects.create(
                season=random.choice(seasons),
                title_ru=title_ru,
                title_ky=f'{title_ru} (ky)',
                title_uz=f'{title_ru} (uz)',
                description_ru=desc_ru,
                description_ky=f'{desc_ru} (ky)',
                description_uz=f'{desc_ru} (uz)',
                year=2021,
                country=random.choice(countries),
                language=random.choice(['Russian', 'Кыргыз']),
                trailer_url='https://youtu.be/series_trailer',
                access_type=random.choice(access_types),
                is_published=True,
                views_count=random.randint(0, 5000),
                image='series_images/default.jpg',
                video='series_videos/default.mp4'
            )
            series.genres.set(random.sample(genres, random.randint(1, 2)))
            series.persons.set(random.sample(persons, random.randint(2, 3)))
            series_list.append(series)
            self.stdout.write(f'  Created series: {series.title_ru}')
        return series_list

    def create_cartoons(self, genres, countries):
        cartoons_data = [
            ('Шрек', 'Зеленый огр спасает принцессу...', 2001, 90),
            ('Король Лев', 'Львенок Симба становится королем...', 1994, 88),
            ('История игрушек', 'Игрушки оживают, когда хозяина нет...', 1995, 81),
            ('Холодное сердце', 'Принцесса ищет сестру с магией льда...', 2013, 102),
            ('Головоломка', 'Эмоции управляют девочкой...', 2015, 95),
            ('Тайна Коко', 'Мальчик попадает в мир мертвых...', 2017, 105),
            ('Как приручить дракона', 'Викинг дружит с драконом...', 2010, 98),
            ('Зверополис', 'Зайчиха-полицейский раскрывает заговор...', 2016, 108),
            ('Душа', 'Учитель музыки знакомится с душой...', 2020, 100),
            ('Лука', 'Мальчик-монстр дружит с человеком...', 2021, 95)
        ]
        cartoons = []
        access_types = ['Free', 'Subscription', 'Rent']
        age_ratings = ['0+', '6+', '12+', '16+', '18+']
        for title_ru, desc_ru, year, dur in cartoons_data:
            title_ky = f'{title_ru} (ky)'
            title_uz = f'{title_ru} (uz)'
            desc_ky = f'{desc_ru} (кыргызча)'
            desc_uz = f'{desc_ru} (o‘zbekcha)'
            access = random.choice(access_types)
            cartoon = Cartoon.objects.create(
                title_ru=title_ru,
                title_ky=title_ky,
                title_uz=title_uz,
                description_ru=desc_ru,
                description_ky=desc_ky,
                description_uz=desc_uz,
                year=year,
                country=random.choice(countries),
                language='Russian',
                duration=dur,
                trailer_url='https://youtu.be/cartoon_trailer',
                age_rating=random.choice(age_ratings),
                access_type=access,
                is_published=True,
                views_count=random.randint(0, 10000),
                cartoon_image='cartoon_image/default.jpg',
                video='film_video/default.mp4'
            )
            cartoon.genres.set(random.sample(genres, random.randint(1, 3)))
            # У Cartoon нет поля persons — строку ниже удалили
            cartoons.append(cartoon)
            self.stdout.write(f'  Created cartoon: {cartoon.title_ru}')
        return cartoons

    def create_subscriptions(self, users):
        plans = ['daily', 'monthly', 'year']
        for user in random.sample(users, k=min(5, len(users))):
            plan = random.choice(plans)
            duration = {'daily': 1, 'monthly': 30, 'year': 365}[plan]
            end_date = timezone.now() + timedelta(days=duration)
            price = {'daily': 100, 'monthly': 500, 'year': 5000}[plan]
            Subscription.objects.create(
                user=user,
                plan=plan,
                end_date=end_date,
                is_activ=True,
                price=price
            )
            self.stdout.write(f'  Created subscription for {user.username} ({plan})')

    def create_favorites(self, users):
        favorites = []
        for user in users:
            fav = Favorite.objects.create(user=user)
            favorites.append(fav)
            self.stdout.write(f'  Created favorite list for {user.username}')
        return favorites

    def create_favorite_items(self, favorites, films, series_list, cartoons):
        for fav in favorites:
            all_media = films + series_list + cartoons
            items_count = random.randint(2, 4)
            chosen = random.sample(all_media, min(items_count, len(all_media)))
            for media in chosen:
                item = FavoriteItem.objects.create(watchlist=fav)
                if isinstance(media, Film):
                    item.film = media
                elif isinstance(media, Series):
                    item.series = media
                elif isinstance(media, Cartoon):
                    item.cartoon = media
                item.save()
            self.stdout.write(f'  Added {len(chosen)} items to favorite of user {fav.user.username}')

    def create_reviews(self, users, films, series_list, cartoons):
        all_media = films + series_list + cartoons
        for _ in range(30):
            user = random.choice(users)
            media = random.choice(all_media)
            stars = random.randint(1, 10)
            text = random.choice([
                'Отличный фильм!', 'Не понравилось.', 'Среднячок.',
                'Лучшее, что я видел!', 'Скучно.', 'Рекомендую!'
            ])
            review = Review.objects.create(
                user=user,
                stars=stars,
                text=text,
                created_date=timezone.now() - timedelta(days=random.randint(0, 100))
            )
            if isinstance(media, Film):
                review.film = media
            elif isinstance(media, Series):
                review.series = media
            else:
                review.cartoon = media
            review.save()
            self.stdout.write(f'  Created review by {user.username} for {str(media)}')
        # Создаём несколько ответов
        parent_reviews = Review.objects.exclude(parent__isnull=False)[:10]
        for parent in parent_reviews:
            Review.objects.create(
                user=random.choice(users),
                text='Согласен с вашим мнением!',
                parent=parent,
                film=parent.film,
                series=parent.series,
                cartoon=parent.cartoon,
                stars=None
            )
            self.stdout.write(f'  Created reply to review {parent.id}')