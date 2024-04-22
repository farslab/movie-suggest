from django.contrib import admin
from suggest.models import Movie
# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    pass