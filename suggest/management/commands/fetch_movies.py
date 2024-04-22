import requests
from django.core.management.base import BaseCommand
from suggest.models import Movie
from datetime import datetime
import csv
class Command(BaseCommand):
    help = 'Fetches movies from TMDB API using titles and saves them to the database'

    def handle(self, *args, **kwargs):
        api_key = '4d4699147b6f9a8d0b0631f8db1da2f8'
        base_url = 'https://api.themoviedb.org/3/search/movie'

        # CSV dosyası adı ve yolu
        csv_file = './dataset1mb/output.csv'

        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            # CSV dosyasını oku
            movies = csv.DictReader(csvfile)
            for movie in movies:
                title = movie['title']

                # TMDB API'sine başlıkla filmi aramak için istek gönder
                params = {
                    'api_key': api_key,
                    'query': title,
                    'language': 'en-US'
                }
                response = requests.get(base_url, params=params)
                data = response.json()

                if data['results']:
                    movie_data = data['results'][0]

                    # Convert release_date to datetime object if available
                    release_date = None
                    if movie_data.get('release_date'):
                        release_date = datetime.strptime(movie_data['release_date'], '%Y-%m-%d').date()

                    # Movie modelini güncelle
                    movie_obj, created = Movie.objects.get_or_create(
                        title=movie_data['title'],
                        defaults={
                            'adult': movie_data['adult'],
                            'original_language': movie_data['original_language'],
                            'original_title': movie_data['original_title'],
                            'overview': movie_data['overview'],
                            'popularity': movie_data['popularity'],
                            'poster_path': movie_data['poster_path'],
                            'release_date': release_date,
                            'video': movie_data['video'],
                            'vote_average': movie_data['vote_average'],
                            'vote_count': movie_data['vote_count']
                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Movie '{title}' saved to the database."))
                    else:
                        self.stdout.write(self.style.WARNING(f"Movie '{title}' already exists in the database. Skipping..."))
                else:
                    self.stdout.write(self.style.WARNING(f"Movie '{title}' not found on TMDB. Skipping..."))
