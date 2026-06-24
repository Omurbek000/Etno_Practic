from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    UserProfile, Genre, Country, Person, Film, Series, Season,
    Cartoon, Subscription, Favorite, FavoriteItem, Review,
)

PREFIX = "/ru"


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


class RegisterViewTest(APITestCase):
    def test_register_success(self):
        data = {
            "email": "test@test.com",
            "username": "testuser",
            "password": "TestPass123!",
            "phone_number": "+996700123456",
        }
        response = self.client.post(f"{PREFIX}/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(UserProfile.objects.first().email, "test@test.com")

    def test_register_duplicate_email(self):
        UserProfile.objects.create_user(
            username="existing", email="dup@test.com", password="Pass123!"
        )
        data = {
            "email": "dup@test.com",
            "username": "newuser",
            "password": "Pass123!",
        }
        response = self.client.post(f"{PREFIX}/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_missing_fields(self):
        response = self.client.post(f"{PREFIX}/register/", {"email": "a@b.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(
            username="loginuser", email="login@test.com", password="Pass123!"
        )

    def test_login_success(self):
        data = {"email": "login@test.com", "password": "Pass123!"}
        response = self.client.post(f"{PREFIX}/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["email"], "login@test.com")

    def test_login_wrong_password(self):
        data = {"email": "login@test.com", "password": "WrongPass!"}
        response = self.client.post(f"{PREFIX}/login/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_nonexistent_user(self):
        data = {"email": "noone@test.com", "password": "Pass123!"}
        response = self.client.post(f"{PREFIX}/login/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutViewTest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(
            username="logoutuser", email="logout@test.com", password="Pass123!"
        )
        self.tokens = get_tokens(self.user)

    def test_logout_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.tokens['access']}")
        response = self.client.post(
            f"{PREFIX}/logout/", {"refresh": self.tokens["refresh"]}
        )
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.tokens['access']}")
        response = self.client.post(f"{PREFIX}/logout/", {"refresh": "badtoken"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserProfileTest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(
            username="profileuser",
            email="profile@test.com",
            password="Pass123!",
            first_name="John",
            last_name="Doe",
        )
        self.tokens = get_tokens(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.tokens['access']}")

    def test_user_list(self):
        response = self.client.get(f"{PREFIX}/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

    def test_user_detail(self):
        response = self.client.get(f"{PREFIX}/users/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "John")

    def test_user_update(self):
        response = self.client.patch(
            f"{PREFIX}/users/{self.user.id}/", {"first_name": "Jane"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Jane")


class GenreTest(APITestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Action")

    def test_genre_list(self):
        response = self.client.get(f"{PREFIX}/genre/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Action")

    def test_genre_detail(self):
        response = self.client.get(f"{PREFIX}/genre/{self.genre.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Action")


class CountryTest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_superuser(
            username="admin", email="admin@test.com", password="Pass123!"
        )
        self.tokens = get_tokens(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.tokens['access']}")
        self.country = Country.objects.create(country="Kyrgyzstan")

    def test_country_list(self):
        response = self.client.get(f"{PREFIX}/country/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_country_create(self):
        response = self.client.post(
            f"{PREFIX}/country/", {"country": "Kazakhstan"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Country.objects.count(), 2)

    def test_country_delete(self):
        response = self.client.delete(f"{PREFIX}/country/{self.country.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Country.objects.count(), 0)


class PersonTest(APITestCase):
    def setUp(self):
        self.person = Person.objects.create(
            first_name="Tom", last_name="Cruise", role="Actor",
            person_image="test.jpg",
        )

    def test_person_list(self):
        response = self.client.get(f"{PREFIX}/person/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_person_detail(self):
        response = self.client.get(f"{PREFIX}/person/{self.person.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Tom")


class FilmTest(APITestCase):
    def setUp(self):
        self.country = Country.objects.create(country="USA")
        self.genre = Genre.objects.create(name="Action")
        self.person = Person.objects.create(
            first_name="Tom", last_name="Cruise", role="Actor",
            person_image="test.jpg",
        )
        self.film = Film.objects.create(
            title="Mission Impossible",
            description="Secret agent movie",
            poster_image="poster.jpg",
            year=2023,
            country=self.country,
            duration=120,
            language="Russian",
            video="video.mp4",
            trailer="https://youtube.com/watch?v=123",
            access_type="Free",
            is_published=True,
        )
        self.film.genres.add(self.genre)
        self.film.persons.add(self.person)

    def test_film_list(self):
        response = self.client.get(f"{PREFIX}/film/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["title"], "Mission Impossible")

    def test_film_detail_free(self):
        user = UserProfile.objects.create_user(
            username="viewer", email="viewer@test.com", password="Pass123!"
        )
        tokens = get_tokens(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.get(f"{PREFIX}/film/{self.film.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_film_detail_requires_auth(self):
        response = self.client.get(f"{PREFIX}/film/{self.film.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_film_detail_subscription_required(self):
        self.film.access_type = "Subscription"
        self.film.save()
        user = UserProfile.objects.create_user(
            username="basic", email="basic@test.com", password="Pass123!"
        )
        tokens = get_tokens(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.get(f"{PREFIX}/film/{self.film.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_film_detail_subscription_vip_ok(self):
        self.film.access_type = "Subscription"
        self.film.save()
        user = UserProfile.objects.create_user(
            username="vip", email="vip@test.com", password="Pass123!",
            subscription_status="VIP",
        )
        tokens = get_tokens(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.get(f"{PREFIX}/film/{self.film.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_film_filter_by_year(self):
        Film.objects.create(
            title="Old Film", description="Old", poster_image="old.jpg",
            year=2000, country=self.country, duration=90,
            language="Russian", video="v.mp4",
            trailer="https://youtube.com/watch?v=1",
            access_type="Free", is_published=True,
        )
        response = self.client.get(f"{PREFIX}/film/", {"year__gt": 2010})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_film_filter_by_genre(self):
        response = self.client.get(f"{PREFIX}/film/", {"genres": self.genre.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_film_filter_by_language(self):
        response = self.client.get(f"{PREFIX}/film/", {"language": "Russian"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_film_detail_not_found(self):
        user = UserProfile.objects.create_user(
            username="viewer2", email="viewer2@test.com", password="Pass123!"
        )
        tokens = get_tokens(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.get(f"{PREFIX}/film/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SeriesTest(APITestCase):
    def setUp(self):
        self.country = Country.objects.create(country="USA")
        self.genre = Genre.objects.create(name="Drama")
        self.season = Season.objects.create(
            season_number=1, title="Season 1", year=2023
        )
        self.series = Series.objects.create(
            season=self.season,
            title="Episode 1",
            description="Pilot",
            image="ep1.jpg",
            year=2023,
            country=self.country,
            language="Russian",
            trailer_url="https://youtube.com/watch?v=123",
            video="ep1.mp4",
            access_type="Free",
            is_published=True,
        )
        self.series.genres.add(self.genre)

    def test_series_list(self):
        response = self.client.get(f"{PREFIX}/series/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_series_detail(self):
        user = UserProfile.objects.create_user(
            username="seriesviewer", email="sv@test.com", password="Pass123!"
        )
        tokens = get_tokens(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.get(f"{PREFIX}/series/{self.series.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Episode 1")

    def test_series_full_auth_required(self):
        response = self.client.get(f"{PREFIX}/series/{self.series.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_series_filter_by_season(self):
        response = self.client.get(
            f"{PREFIX}/series/", {"season__season_number": 1}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)


class SeasonTest(APITestCase):
    def setUp(self):
        self.season = Season.objects.create(
            season_number=1, title="Season 1", year=2023
        )

    def test_season_list(self):
        response = self.client.get(f"{PREFIX}/season/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_season_detail(self):
        response = self.client.get(f"{PREFIX}/season/{self.season.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_season_detail_no_auth_required(self):
        response = self.client.get(f"{PREFIX}/season/{self.season.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CartoonTest(APITestCase):
    def setUp(self):
        self.country = Country.objects.create(country="USA")
        self.genre = Genre.objects.create(name="Comedy")
        self.cartoon = Cartoon.objects.create(
            title="Test Cartoon",
            description="Funny cartoon",
            cartoon_image="cartoon.jpg",
            year=2023,
            country=self.country,
            language="Russian",
            duration=80,
            video="cartoon.mp4",
            trailer_url="https://youtube.com/watch?v=123",
            age_rating="6+",
            access_type="Free",
            is_published=True,
        )
        self.cartoon.genres.add(self.genre)

    def test_cartoon_list(self):
        response = self.client.get(f"{PREFIX}/cartoon/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_cartoon_detail(self):
        user = UserProfile.objects.create_user(
            username="cv", email="cv@test.com", password="Pass123!"
        )
        tokens = get_tokens(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.get(f"{PREFIX}/cartoon/{self.cartoon.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cartoon_detail_requires_auth(self):
        response = self.client.get(f"{PREFIX}/cartoon/{self.cartoon.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cartoon_filter_by_age_rating(self):
        response = self.client.get(f"{PREFIX}/cartoon/", {"age_rating": "6+"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)


class FavoriteTest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(
            username="favuser", email="fav@test.com", password="Pass123!"
        )
        self.tokens = get_tokens(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.tokens['access']}")
        self.country = Country.objects.create(country="USA")
        self.film = Film.objects.create(
            title="Fav Film", description="Desc", poster_image="p.jpg",
            year=2023, country=self.country, duration=100,
            language="Russian", video="v.mp4",
            trailer="https://youtube.com/watch?v=1",
            access_type="Free", is_published=True,
        )

    def test_get_favorite(self):
        response = self.client.get(f"{PREFIX}/favorite/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_to_favorite(self):
        response = self.client.post(
            f"{PREFIX}/favoriteitem/", {"film_id": self.film.id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FavoriteItem.objects.count(), 1)

    def test_remove_from_favorite(self):
        fav = Favorite.objects.create(user=self.user)
        item = FavoriteItem.objects.create(watchlist=fav, film=self.film)
        response = self.client.delete(f"{PREFIX}/favoriteitem/{item.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_favorite_requires_auth(self):
        self.client.credentials()
        response = self.client.get(f"{PREFIX}/favorite/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReviewTest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(
            username="reviewer", email="rev@test.com", password="Pass123!"
        )
        self.tokens = get_tokens(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.tokens['access']}")
        self.country = Country.objects.create(country="USA")
        self.film = Film.objects.create(
            title="Review Film", description="Desc", poster_image="p.jpg",
            year=2023, country=self.country, duration=100,
            language="Russian", video="v.mp4",
            trailer="https://youtube.com/watch?v=1",
            access_type="Free", is_published=True,
        )

    def test_create_review(self):
        data = {"text": "Great movie!", "stars": 9, "film_id": self.film.id}
        response = self.client.post(f"{PREFIX}/review/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().user, self.user)
        self.assertEqual(Review.objects.first().film, self.film)

    def test_review_list(self):
        Review.objects.create(user=self.user, film=self.film, text="Good", stars=8)
        response = self.client.get(f"{PREFIX}/review/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_requires_auth(self):
        self.client.credentials()
        data = {"text": "test", "film_id": self.film.id}
        response = self.client.post(
            f"{PREFIX}/review/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_own_review(self):
        review = Review.objects.create(
            user=self.user, film=self.film, text="Mine", stars=7
        )
        response = self.client.delete(f"{PREFIX}/review/{review.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_user_review(self):
        other = UserProfile.objects.create_user(
            username="other", email="other@test.com", password="Pass123!"
        )
        review = Review.objects.create(
            user=other, film=self.film, text="Not mine", stars=5
        )
        response = self.client.delete(f"{PREFIX}/review/{review.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTest(APITestCase):
    def setUp(self):
        self.admin = UserProfile.objects.create_superuser(
            username="admin", email="admin@test.com", password="Pass123!"
        )
        self.tokens = get_tokens(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.tokens['access']}")
        self.user = UserProfile.objects.create_user(
            username="subuser", email="sub@test.com", password="Pass123!"
        )

    def test_create_subscription(self):
        from django.utils import timezone
        from datetime import timedelta

        data = {
            "user": self.user.id,
            "plan": "monthly",
            "end_date": (timezone.now() + timedelta(days=30)).isoformat(),
            "price": 500,
            "is_active": True,
        }
        response = self.client.post(
            f"{PREFIX}/subscription/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscription_list(self):
        response = self.client.get(f"{PREFIX}/subscription/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SeriesSubscriptionAccessTest(APITestCase):
    """Separate TestCase to avoid credential contamination from setUp"""

    def test_series_subscription_access(self):
        """Series with Subscription access requires auth + VIP"""
        admin = UserProfile.objects.create_superuser(
            username="ad", email="ad@test.com", password="Pass123!"
        )
        country = Country.objects.create(country="Test")
        season = Season.objects.create(season_number=1, title="S1", year=2023)
        series = Series.objects.create(
            season=season, title="Auth Series", description="",
            image="test.jpg", year=2023, country=country,
            language="Russian", trailer_url="https://youtube.com/watch?v=1",
            video="v.mp4", access_type="Subscription", is_published=True,
        )
        # Anonymous user — 401
        response = self.client.get(f"{PREFIX}/series/{series.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated but not VIP — 403
        user = UserProfile.objects.create_user(
            username="basic", email="basic@test.com", password="Pass123!"
        )
        tokens = get_tokens(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.get(f"{PREFIX}/series/{series.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # VIP user — 200
        vip = UserProfile.objects.create_user(
            username="vipuser", email="vip@test.com", password="Pass123!",
            subscription_status="VIP",
        )
        vip_tokens = get_tokens(vip)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {vip_tokens['access']}")
        response = self.client.get(f"{PREFIX}/series/{series.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PermissionCheckTest(APITestCase):
    def test_anonymous_users_list(self):
        response = self.client.get(f"{PREFIX}/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_favorite_returns_401(self):
        response = self.client.get(f"{PREFIX}/favorite/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
