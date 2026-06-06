from rest_framework import serializers
from .models import *


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'last_name','first_name','email','avatar','phone_number','date_register','subscription_status','subscription_end']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']
        
        
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
        


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country']
        

class FilmSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    genres = GenreSerializer(many=True)
    persons = PersonSerializer(many=True)
    class Meta:
        model = Film
        fields = ['id','title','description','poster_image','year','language','duration','video','trailer',
                  'genres','persons','access_type','rent_price','is_published','views_count','created_date','country']


        
class SeriesSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    genres = GenreSerializer(many=True)
    persons = PersonSerializer(many=True)
    season_title = serializers.CharField(source='season.title', read_only=True)

    class Meta:
        model = Series
        fields = [
            'id', 'season', 'season_title', 'title', 'description', 'image', 
            'year', 'country', 'language', 'trailer_url', 'video', 
            'genres', 'persons', 'access_type', 'is_published', 
            'views_count', 'created_date'
        ]        


class SeasonSerializer(serializers.ModelSerializer):
    series_list = SeriesSerializer(many=True, read_only=True)
    class Meta:
        model = Season
        fields = ['id', 'season_number', 'title', 'year', 'series_list']
        
        
class CartoonSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    genres = GenreSerializer(many=True)
    
    class Meta:
        model = Cartoon
        fields = ['title','description','cartoon_image','year','language','duration','video','trailer_url','age_rating',
                  'genres','access_type','is_published','views_count','created_date','country']
        
        
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        
        
class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
        
        
class FavoriteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteItem
        fields = '__all__'
        

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'