from rest_framework import viewsets, generics, permissions
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from .filters import FilmFilter, SeriesFilter, CartoonFilter
from .pagination import (
    FilmPagination,
    SeriesPagination,
    CartoonPagination,
    SubscriptionPagination,
    ReviewPagination,
)
from .permissions import CheckSubscription, CheckUser

class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer


class GenreAPIView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreDetailAPIView(generics.RetrieveAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreDetailSerializer


class PersonListAPIView(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonListSerializer


class PersonDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonDetailSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class FilmListAPIView(generics.ListAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FilmFilter
    pagination_class = FilmPagination


class FilmDetailAPIView(generics.RetrieveAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmDetailSerializer
    permission_classes = [permissions.IsAuthenticated, CheckSubscription]


class SeriesListAPIView(generics.ListAPIView):
    queryset = Series.objects.all()
    serializer_class = SeriesListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SeriesFilter
    pagination_class = SeriesPagination


class SeriesDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Series.objects.all()
    serializer_class = SeriesDetailSerializer


class SeasonListAPIView(generics.ListAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonListSerializer


class SeasonDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonDetailSerializer
    permission_classes = [permissions.IsAuthenticated, CheckSubscription]


class CartoonListAPIView(generics.ListAPIView):
    queryset = Cartoon.objects.all()
    serializer_class = CartoonListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CartoonFilter
    pagination_class = CartoonPagination


class CartoonDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Cartoon.objects.all()
    serializer_class = CartoonDetailSerializer
    permission_classes = [permissions.IsAuthenticated, CheckSubscription]


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    pagination_class = SubscriptionPagination


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class FavoriteItemViewSet(viewsets.ModelViewSet):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckUser]
