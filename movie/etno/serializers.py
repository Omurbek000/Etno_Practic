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
    class Meta:
        model = Series
        fields = ['title','description','series_image','year','country','language','views_count','created_date',
                  'country','trailer_url','video_series','genres','persons','access_type','is_published']        
        
class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ['title','season_number','series','year']
        
        
class CartoonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartoon
        fields = '__all__'
        
        
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