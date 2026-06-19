from rest_framework import serializers
from .models import *


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "first_name", "last_name", "avatar"]


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "last_name",
            "first_name",
            "email",
            "avatar",
            "phone_number",
        ]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["country"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["name"]


class PersonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["last_name", "person_image", "role"]


class PersonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["id", "first_name", "last_name", "person_image", "role"]


class FilmListSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    genres = GenreSerializer(many=True)
    get_avg_rating = serializers.SerializerMethodField(read_only=True)
    get_count_people = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Film
        fields = [
            "id",
            "title",
            "poster_image",
            "year",
            "access_type",
            "is_published",
            "created_date",
            "country",
            "genres",
            "get_avg_rating",
            "get_count_people",
        ]

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class GenreDetailSerializer(serializers.ModelSerializer):
    film_genre = FilmListSerializer(many=True, read_only=True)

    class Meta:
        model = Genre
        fields = ["name", "film_genre"]


class FilmDetailSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    genres = GenreSerializer(many=True)
    persons = PersonListSerializer(many=True)

    class Meta:
        model = Film
        fields = [
            "id",
            "title",
            "description",
            "poster_image",
            "year",
            "language",
            "duration",
            "video",
            "trailer",
            "genres",
            "persons",
            "access_type",
            "rent_price",
            "is_published",
            "views_count",
            "created_date",
            "country",
        ]


class SeriesListSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Series
        fields = [
            "id",
            "title",
            "image",
            "year",
            "country",
            "language",
            "genres",
            "access_type",
            "is_published",
        ]


class SeriesDetailSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    genres = GenreSerializer(many=True)
    persons = PersonListSerializer(many=True)

    class Meta:
        model = Series
        fields = [
            "id",
            "season",
            "season_title",
            "title",
            "description",
            "image",
            "year",
            "country",
            "language",
            "trailer_url",
            "video",
            "genres",
            "persons",
            "access_type",
            "is_published",
            "views_count",
            "created_date",
        ]


class SeasonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ["id", "season_number", "title", "year"]


class SeasonDetailSerializer(serializers.ModelSerializer):
    series_list = SeriesDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Season
        fields = ["id", "season_number", "title", "year", "series_list"]


class CartoonListSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Cartoon
        fields = [
            "title",
            "year",
            "language",
            "age_rating",
            "genres",
            "access_type",
            "is_published",
            "country",
        ]


class CartoonDetailSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Cartoon
        fields = [
            "title",
            "description",
            "cartoon_image",
            "year",
            "language",
            "duration",
            "video",
            "trailer_url",
            "age_rating",
            "genres",
            "access_type",
            "is_published",
            "views_count",
            "created_date",
            "country",
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"


class FavoriteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteItem
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    user_review = UserProfileListSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["user_review", "text", "parent", "created_date"]
