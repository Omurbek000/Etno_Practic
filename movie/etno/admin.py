from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin


# Миксин для того, чтобы не дублировать JS/CSS настройки перевода в каждом классе
class TranslationMediaMixin:
    class Media:
        js = (
            "https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }


class SeriesInline(TranslationInlineModelAdmin, admin.TabularInline):
    model = Series
    extra = 1
    fields = ["title", "year", "language", "is_published"]


class FavoriteItemInline(admin.TabularInline):
    model = FavoriteItem
    extra = 1
    raw_id_fields = ["film", "series", "cartoon"]


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fk_name = "parent"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "phone_number",
        "subscription_status",
        "date_register",
    )
    list_filter = ("subscription_status",)
    search_fields = ("username", "email", "phone_number")


@admin.register(Genre)
class GenreAdmin(TranslationMediaMixin, TranslationAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Country)
class CountryAdmin(TranslationMediaMixin, TranslationAdmin):
    list_display = ("country",)
    search_fields = ("country",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "role")
    list_filter = ("role",)
    search_fields = ("first_name", "last_name")


@admin.register(Film)
class FilmAdmin(TranslationMediaMixin, TranslationAdmin):
    list_display = (
        "title",
        "year",
        "country",
        "access_type",
        "is_published",
        "views_count",
    )
    list_filter = ("is_published", "access_type", "year", "language")
    search_fields = ("title", "description")
    filter_horizontal = ("genres", "persons")
    list_editable = ("is_published",)


@admin.register(Cartoon)
class CartoonAdmin(TranslationMediaMixin, TranslationAdmin):
    list_display = ("title", "year", "age_rating", "access_type", "is_published")
    list_filter = ("is_published", "age_rating", "access_type", "language")
    search_fields = ("title", "description")
    filter_horizontal = ("genres",)
    list_editable = ("is_published",)


@admin.register(Season)
class SeasonAdmin(TranslationMediaMixin, TranslationAdmin):
    list_display = ("title", "season_number", "year")
    search_fields = ("title",)
    inlines = [SeriesInline]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "price", "is_active", "start_date", "end_date")
    list_filter = ("plan", "is_active")
    search_fields = ("user__username", "user__email")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user",)
    inlines = [FavoriteItemInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "stars", "created_date", "film", "series", "cartoon")
    list_filter = ("stars", "created_date")
    search_fields = ("user__username", "text")
    inlines = [ReviewInline]
