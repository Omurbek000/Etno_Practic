from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()


router.register(r"country", CountryViewSet, basename="countrys")
router.register(r"subscription", SubscriptionViewSet, basename="subscriptions")
router.register(r"favorite", FavoriteViewSet, basename="favorites")
router.register(r"favoriteitem", FavoriteItemViewSet, basename="favoriteitems")
router.register(r"review", ReviewViewSet, basename="reviews")


urlpatterns = [
    path("", include(router.urls)),
    path("users/", UserProfileListAPIView.as_view(), name="users_list"),
    path("users/<int:pk>/", UserProfileDetailAPIView.as_view(), name="users_detail"),
    path("film/", FilmListAPIView.as_view(), name="film_list"),
    path("film/<int:pk>", FilmDetailAPIView.as_view(), name="film_detail"),
    path("genre/", GenreAPIView.as_view(), name="ganre_list"),
    path("genre/<int:pk>/", GenreDetailAPIView.as_view(), name="ganre_detail"),
    path("person/", PersonListAPIView.as_view(), name="person_list"),
    path("person/<int:pk>/", PersonDetailAPIView.as_view(), name="person_detail"),
    path("series/", SeriesListAPIView.as_view(), name="series_list"),
    path("series/<int:pk>/", SeriesDetailAPIView.as_view(), name="series_detail"),
    path("season", SeasonListAPIView.as_view(), name="season_list"),
    path("season/<int:pk>", SeasonDetailAPIView.as_view(), name="season_detail"),
    path("cartoon", CartoonListAPIView.as_view(), name="caroon_list"),
    path("cartoon/<int:pk>", CartoonDetailAPIView.as_view(), name="cartoon_detail"),
]
