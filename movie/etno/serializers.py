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
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({"email": "Пользователь с таким email не найден"})

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
