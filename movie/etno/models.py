from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to="profile_image", null=True, blank=True)
    phone_number = PhoneNumberField(
        region="KG",
        null=True,
        blank=True,
    )
    date_register = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (("Free", "Free"), ("VIP", "VIP"))
    subscription_status = models.CharField(
        max_length=5, choices=STATUS_CHOICES, default="Free"
    )
    subscription_end = models.DateTimeField(null=True, blank=True)


class Genre(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(
        max_length=32,
        unique=True,
        null=True,
        blank=True,
    )


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    person_image = models.ImageField(upload_to="person_image")
    ROLE_CHOICES = (
        ("Actor", "Actor"),
        ("Actress", "Actress"),
        ("Director", "Director"),
        ("both", "both"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


class Country(models.Model):
    country = models.CharField(max_length=100, unique=True)


class Film(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    poster_image = models.ImageField(upload_to="poster_image")
    year = models.PositiveIntegerField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField()
    LANGUAGE_CHOICES = (
        (" Kyrgyz", "Kyrgyz"),
        ("Russian", "Russian"),
        ("Other", "Other"),
    )
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    video = models.FileField(upload_to="film_video")
    trailer = models.URLField()
    genres = models.ManyToManyField(Genre)
    persons = models.ManyToManyField(Person)
    ACCESS_TYPE = (("Free", "Free"), ("Subscription", "Subscription"), ("Rent", "Rent"))
    access_type = models.CharField(max_length=15, choices=ACCESS_TYPE)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveBigIntegerField()
    created_date = models.DateField(auto_now_add=True)
    
