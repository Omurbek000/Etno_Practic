from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()



router.register(r"person", PersonViewSet, basename="persons")
router.register(r"country", CountryViewSet, basename="countrys")
router.register(r"season", SeasonViewSet, basename="seasons")
router.register(r"cartoon", CartoonViewSet, basename="cartoons")
router.register(r"subscription", SubscriptionViewSet, basename="subscriptions")
router.register(r"favorite", FavoriteViewSet, basename="favorites")
router.register(r"favoriteitem", FavoriteItemViewSet, basename="favoriteitems")
router.register(r"review", ReviewViewSet, basename="reviews")


urlpatterns = [
    path("", include(router.urls)),
    path("users/", UserProfileListAPIView.as_view(), name="users_list"),
    path("users/<int:pk>/", UserProfileDetailAPIView.as_view(), name="users_detail"),
    path('film/', FilmListAPIView.as_view(),name='film_list'),
    path('film/<int:pk>', FilmDetailAPIView.as_view(), name='film_detail'),
    path('genre/', GenreAPIView.as_view(),name='ganre_list'),
    path('genre/<int:pk>/',GenreDetailAPIView.as_view(),name='ganre_detail'),
]
