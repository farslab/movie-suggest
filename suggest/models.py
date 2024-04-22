# models.py

from django.db import models

class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

class ProductionCompany(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    origin_country = models.CharField(max_length=2)

class ProductionCountry(models.Model):
    iso_3166_1 = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=100)

class SpokenLanguage(models.Model):
    english_name = models.CharField(max_length=100)
    iso_639_1 = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=100)

class Movie(models.Model):
    adult = models.BooleanField(null=True)
    backdrop_path = models.CharField(max_length=255)
    belongs_to_collection = models.CharField(max_length=255, null=True, blank=True)
    original_language = models.CharField(max_length=10)
    original_title = models.CharField(max_length=255)
    overview = models.TextField(null=True)
    popularity = models.FloatField(null=True)
    poster_path = models.CharField(max_length=255,null=True)
    release_date = models.DateField(null=True,)
    title = models.CharField(max_length=255)
    video = models.BooleanField(null=True)
    vote_average = models.FloatField(null=True)
    vote_count = models.IntegerField(null=True)
    genres = models.ManyToManyField(Genre)
    spoken_languages = models.ManyToManyField(SpokenLanguage)
    csv_id = models.IntegerField(default=0, null=True) 
    def __str__(self):
        return self.title
class Dataset(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    genres = models.CharField(max_length=255)
    user_id = models.IntegerField()
    rating = models.FloatField()
