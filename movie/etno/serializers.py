from rest_framework import serializers
from .models import *

from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('email', 'username', 'password', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        user = UserProfile(email=email, username=username, **validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            user = UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({"username": "Пользователь с таким именем не найден"})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Неверный пароль"})

        self.context['user'] = user
        return data

    def to_representation(self, instance):
        user = self.context['user']
        refresh = RefreshToken.for_user(user)

        return {
            'user': {
                'username': user.username,
                'email': user.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get('refresh')
        try:
            RefreshToken(token)
        except Exception:
            raise serializers.ValidationError({"refresh": "Невалидный токен"})
        return attrs


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "username", "first_name", "last_name", "email", "avatar", "phone_number", "subscription_status", "date_register"]


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "phone_number",
            "subscription_status",
            "date_register",
        ]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "country"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class PersonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["id", "last_name", "person_image", "role"]


class PersonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["id", "first_name", "last_name", "person_image", "role"]


class FilmListSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    genres = GenreSerializer(many=True)
    get_avg_rating = serializers.SerializerMethodField(read_only=True)
    get_ratings_count = serializers.SerializerMethodField(read_only=True)

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
            "get_ratings_count",
        ]

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_ratings_count(self, obj):
        return obj.get_ratings_count()


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
            "id",
            "title",
            "cartoon_image",
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
            "id",
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


class FavoriteItemSerializer(serializers.ModelSerializer):
    film = FilmListSerializer(read_only=True)
    film_id = serializers.PrimaryKeyRelatedField(
        queryset=Film.objects.all(),
        write_only=True,
        source='film',
        required=False,
        allow_null=True,
    )
    series_id = serializers.PrimaryKeyRelatedField(
        queryset=Series.objects.all(),
        write_only=True,
        source='series',
        required=False,
        allow_null=True,
    )
    cartoon_id = serializers.PrimaryKeyRelatedField(
        queryset=Cartoon.objects.all(),
        write_only=True,
        source='cartoon',
        required=False,
        allow_null=True,
    )

    class Meta:
        model = FavoriteItem
        fields = ['id', 'film', 'film_id', 'series_id', 'cartoon_id']


class FavoriteSerializer(serializers.ModelSerializer):
    film_item = FavoriteItemSerializer(read_only=True, many=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'film_item']


class ReviewSerializer(serializers.ModelSerializer):
    user_review = UserProfileListSerializer(read_only=True, source='user')
    film_id = serializers.PrimaryKeyRelatedField(
        queryset=Film.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    series_id = serializers.PrimaryKeyRelatedField(
        queryset=Series.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    cartoon_id = serializers.PrimaryKeyRelatedField(
        queryset=Cartoon.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "user_review",
            "film_id",
            "series_id",
            "cartoon_id",
            "stars",
            "text",
            "parent",
            "created_date",
        ]

    def create(self, validated_data):
        film = validated_data.pop('film_id', None)
        series = validated_data.pop('series_id', None)
        cartoon = validated_data.pop('cartoon_id', None)
        user = validated_data.pop('user')
        return Review.objects.create(
            user=user,
            film=film,
            series=series,
            cartoon=cartoon,
            **validated_data,
        )
