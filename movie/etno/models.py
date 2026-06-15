from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator


LANGUAGE_CHOICES = (
    ("Kyrgyz", "Kyrgyz"),
    ("Russian", "Russian"),
    ("Other", "Other"),
)

ACCESS_TYPE = (("Free", "Free"), ("Subscription", "Subscription"), ("Rent", "Rent"))

AGE_CHOICES = (
    ("0+", "0+"),
    ("6+", "6+"),
    ("12+", "12+"),
    ("16+", "16+"),
    ("18+", "18+"),
)


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

    def __str__(self) -> str:
        return self.username


class Genre(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(
        max_length=32,
        unique=True,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


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

    def __str__(self):
        return f"{self.first_name} - {self.last_name}, {self.role}"


class Country(models.Model):
    country = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.country


class Film(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    poster_image = models.ImageField(upload_to="poster_image")
    year = models.PositiveIntegerField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField()
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    video = models.FileField(upload_to="film_video")
    trailer = models.URLField()
    genres = models.ManyToManyField(Genre, related_name='film_genre')
    persons = models.ManyToManyField(Person)
    access_type = models.CharField(max_length=15, choices=ACCESS_TYPE)
    rent_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveBigIntegerField(default=0)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    
    def get_avf_rating(self):
        ratings =  self.film_rating.all()
        if ratings.exists():
            return sum([i.stars for i in ratings]) / ratings.count()
        return 0 
    
    
    def get_count_people(self):
        return self.film_rating.count()
        

class Season(models.Model):
    season_number = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"Season {self.season_number}: {self.title}"


class Series(models.Model):
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name="series_list"
    )
    title = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="series_images")
    year = models.PositiveIntegerField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    language = models.CharField(max_length=15, choices=LANGUAGE_CHOICES)
    trailer_url = models.URLField()
    video = models.FileField(upload_to="series_videos", blank=True, null=True)
    genres = models.ManyToManyField(Genre)
    persons = models.ManyToManyField(Person)
    access_type = models.CharField(max_length=15, choices=ACCESS_TYPE)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveBigIntegerField(default=0)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Cartoon(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    cartoon_image = models.ImageField(upload_to="cartoon_image")
    year = models.PositiveIntegerField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    language = models.CharField(max_length=15, choices=LANGUAGE_CHOICES)
    duration = models.PositiveIntegerField()
    video = models.FileField(upload_to="film_video")
    trailer_url = models.URLField()
    age_rating = models.CharField(max_length=10, choices=AGE_CHOICES)
    genres = models.ManyToManyField(Genre)
    access_type = models.CharField(max_length=15, choices=ACCESS_TYPE)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveBigIntegerField(default=0)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    PLAN_CHOICES = (("daily", "daily"), ("monthly", "monthly"), ("year", "year"))
    plan = models.CharField(max_length=15, choices=PLAN_CHOICES)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_activ = models.BooleanField(default=False)
    price = models.PositiveIntegerField()


class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)


class FavoriteItem(models.Model):
    watchlist = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, null=True, blank=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, blank=True)
    cartoon = models.ForeignKey(
        Cartoon, on_delete=models.CASCADE, null=True, blank=True
    )
    added_date = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='user_review')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, null=True, blank=True,related_name='film_rating')
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, blank=True)
    cartoon = models.ForeignKey(
        Cartoon, on_delete=models.CASCADE, null=True, blank=True
    )
    stars = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        null=True,
        blank=True,
    )
    text = models.TextField(null=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
