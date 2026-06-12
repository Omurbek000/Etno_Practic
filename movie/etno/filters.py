from django_filters import FilterSet
from .models import Film, Series, Cartoon

class FilmFilter(FilterSet):
    class Meta:
        model = Film
        fields = {
            'year': ['gt', 'lt'],          # год: больше (gt) и меньше (lt)
            'country': ['exact'],          # точное совпадение страны (по id)
            'genres': ['exact'],           # жанр (по id жанра) – работает для ManyToMany как exact
            'access_type': ['exact'],      # тип доступа
            'language': ['exact'],         # язык
            # 'views_count': ['gte', 'lte'], # просмотры: больше/равно и меньше/равно
            # 'created_date': ['gte', 'lte'],# дата создания
        }

class SeriesFilter(FilterSet):
    class Meta:
        model = Series
        fields = {
            'year': ['gt', 'lt'],
            'country': ['exact'],
            'genres': ['exact'],
            'access_type': ['exact'],
            'language': ['exact'],
            # 'views_count': ['gte', 'lte'],
            # 'created_date': ['gte', 'lte'],
            'season__season_number': ['exact'],  # фильтр по номеру сезона (через связь)
        }

class CartoonFilter(FilterSet):
    class Meta:
        model = Cartoon
        fields = {
            'year': ['gt', 'lt'],
            'country': ['exact'],
            'genres': ['exact'],
            'access_type': ['exact'],
            'language': ['exact'],
            'age_rating': ['exact'],
            # 'duration': ['gte', 'lte'],
            # 'views_count': ['gte', 'lte'],
            # 'created_date': ['gte', 'lte'],
        }