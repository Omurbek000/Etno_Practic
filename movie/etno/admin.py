from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin

class SeasonInline(TranslationInlineModelAdmin, admin.TabularInline):
    model = Season
    extra = 1

@admin.register(Series)
class SeriesAdmin(TranslationAdmin):
    inlines = [SeasonInline]
    class Media:
        js = (
            "https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }

@admin.register(Genre, Country, Film, Cartoon) 
class AllAdmin(TranslationAdmin):
    class Media:
        js = (
            "https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }



admin.site.register(UserProfile)
admin.site.register(Person)
admin.site.register(Subscription)
admin.site.register(Favorite)
admin.site.register(FavoriteItem)
admin.site.register(Review)