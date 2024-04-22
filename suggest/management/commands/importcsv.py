# management/commands/importcsv.py

from django.core.management.base import BaseCommand
import pandas as pd
from datetime import datetime
from suggest.models import Dataset  # Django modelinizi içeri aktarın

class Command(BaseCommand):
    help = 'Import data from a CSV file into the Dataset model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='The file path of the CSV file to import')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file_path']

        # CSV dosyasını oku
        df = pd.read_csv(csv_file_path)

        # DataFrame'deki her satır için döngü
        for index, row in df.iterrows():
            # DataFrame'den verileri al
            movie_id = row['movieId']
            title = row['title']
            genres = row['genres']
            user_id = row['userId']
            rating = row['rating']

            # Django modeline verileri kaydet
            dataset = Dataset.objects.create(
                movie_id=movie_id,
                title=title,
                genres=genres,
                user_id=user_id,
                rating=rating,
            )

        self.stdout.write(self.style.SUCCESS("Veri başarıyla içeri aktarıldı."))
