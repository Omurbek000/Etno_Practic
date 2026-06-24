from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register(r"country", CountryViewSet, basename="countrys")
router.register(r"subscription", SubscriptionViewSet, basename="subscriptions")
router.register(r"favoriteitem", FavoriteItemViewSet, basename="favoriteitems")
router.register(r"review", ReviewViewSet, basename="reviews")

urlpatterns = [
    path("", include(router.urls)),
    path("users/", UserProfileListAPIView.as_view(), name="users_list"),
    path("users/<int:pk>/", UserProfileDetailAPIView.as_view(), name="users_detail"),
    path("film/", FilmListAPIView.as_view(), name="film_list"),
    path("film/<int:pk>/", FilmDetailAPIView.as_view(), name="film_detail"),
    path("genre/", GenreAPIView.as_view(), name="genre_list"),
    path("genre/<int:pk>/", GenreDetailAPIView.as_view(), name="genre_detail"),
    path("person/", PersonListAPIView.as_view(), name="person_list"),
    path("person/<int:pk>/", PersonDetailAPIView.as_view(), name="person_detail"),
    path("series/", SeriesListAPIView.as_view(), name="series_list"),
    path("series/<int:pk>/", SeriesDetailAPIView.as_view(), name="series_detail"),
    path("season/", SeasonListAPIView.as_view(), name="season_list"),
    path("season/<int:pk>/", SeasonDetailAPIView.as_view(), name="season_detail"),
    path("cartoon/", CartoonListAPIView.as_view(), name="cartoon_list"),
    path("cartoon/<int:pk>/", CartoonDetailAPIView.as_view(), name="cartoon_detail"),
    path("register/", RegisterView.as_view(), name="register_list"),
    path("login/", CustomLoginView.as_view(), name="login_list"),
    path("logout/", LogoutView.as_view(), name="logout_list"),
    path("favorite/", FavoriteAPIView.as_view(), name="favorite_detail"),
]
