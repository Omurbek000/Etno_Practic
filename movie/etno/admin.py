from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Genre)
admin.site.register(Person)
admin.site.register(Country)
admin.site.register(Film)
admin.site.register(Series)
admin.site.register(Season)
admin.site.register(Cartoon)
admin.site.register(Subscription)
admin.site.register(Favorite)
admin.site.register(FavoriteItem)
admin.site.register(Review)