from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.movie_list, name='movie_list'),
    path('search/', views.search_movies, name='search_movies'),
    path('recommendations/', views.recommendations, name='recommendations_page'),
]