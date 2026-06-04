from django.urls import path , include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register(r'user', UserProfileViewSet, basename='users')
router.register(r'genre', GenreViewSet , basename='genres')
router.register(r'person', PersonViewSet, basename='persons')
router.register(r'country', CountryViewSet, basename='countrys')
router.register(r'film', FilmViewSet, basename='films')
router.register(r'serie', SeriesViewSet, basename='series')
router.register(r'season', SeasonViewSet, basename='seasons')
router.register(r'cartoon', CartoonViewSet, basename='cartoons')
router.register(r'subscription', SubscriptionViewSet, basename='subscriptions')
router.register(r'favorite', FavoriteViewSet, basename='favorites')
router.register(r'favoriteitem', FavoriteItemViewSet, basename='favoriteitems')
router.register(r'review', ReviewViewSet, basename='reviews')


urlpatterns = [
    path('', include(router.urls)),
]