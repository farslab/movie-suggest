from django.core.management.base import BaseCommand
from suggest.models import Movie
import csv

class Command(BaseCommand):
    help = 'Update csv_id field in Movie model from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file_path']
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                movie_id = int(row['movieId'])
                title = row['title']
                try:
                    print(title)
                    movie = Movie.objects.get(title=title)
                    movie.csv_id = movie_id
                    movie.save()
                    self.stdout.write(self.style.SUCCESS(f"Id eklendi {movie_id}."))

                except Movie.DoesNotExist:
                    # Film bulunamazsa yeni bir film oluşturun
                    self.stdout.write(self.style.WARNING(f"Movie with title '{title}' does not exist. Created a new movie with csv_id {movie_id}."))

