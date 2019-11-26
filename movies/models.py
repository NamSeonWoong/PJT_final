from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms

# Create your models here.
# class Genre(models.Model):
#     name = models.CharField(max_length=20)

class Movie(models.Model):
    title = models.CharField(max_length=30)
    pubdate = models.CharField(max_length=50)
    director = models.TextField()
    cast = models.TextField()
    audience = models.IntegerField()
    poster_url = models.CharField(max_length=140)
    genre = models.CharField(max_length=50)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_movies")

class Review(models.Model):
    content = models.CharField(max_length=140)
    score = models.IntegerField(
                        validators=[MinValueValidator(1),MaxValueValidator(10)],)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
