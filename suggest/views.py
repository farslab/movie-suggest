import subprocess
from django.shortcuts import render
from .models import Movie
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.core import serializers
import random
import pandas as pd
import numpy as np
import argparse
import json
def movie_list(request):
    query = request.GET.get('q')

    
    movie_list = Movie.objects.all()

    paginator = Paginator(movie_list, 50) # Show 50 movies per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'movie_list.html', {'page_obj': page_obj})


def search_movies(request):
    query = request.GET.get('q', '')
    if query:
        # Perform a search query based on the 'query' parameter
        results = Movie.objects.filter(title__icontains=query)
        if not results:
            # If no results found, fall back to the movie_list view for pagination
            return movie_list(request)
    else:
        # If the query is empty, fall back to the movie_list view for pagination
        return movie_list(request)
        
    # Serialize the queryset to JSON
    serialized_results = [{'id': movie.id, 'title': movie.title, 'poster_path': movie.poster_path, 'release_date': movie.release_date, 'overview': movie.overview} for movie in results]
    return JsonResponse(serialized_results, safe=False)
def recommendations(request):
    selected_movies = request.GET.get('selectedMovies', '')
    selected_movies_list = selected_movies.split(',') if selected_movies else []
    # Seçili filmlerin ID'lerine göre ilgili film nesnelerini al
    movies = Movie.objects.filter(id__in=selected_movies_list)
    user_id = random.randint(9999,9999999)
    # Run the ysa.py function with the random user ID
    null_csv_id= Movie.objects.all()
    print(null_csv_id.count())
    print(user_id)
    subprocess.call(['python', 'ysa.py', str(user_id)])
    return render(request, 'recommendations_page.html', {'movies': movies})