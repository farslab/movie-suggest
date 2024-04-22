import csv
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Removes dates from movie titles in a CSV file and creates a new CSV file'

    def add_arguments(self, parser):
        parser.add_argument('input_csv', type=str, help='Input CSV file path')
        parser.add_argument('output_csv', type=str, help='Output CSV file path')

    def handle(self, *args, **kwargs):
        input_csv = kwargs['input_csv']
        output_csv = kwargs['output_csv']

        with open(input_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Başlık satırını oku
            rows = []
            for row in reader:
                # Tarih bilgisini silerek yeni satırı oluştur
                new_row = [row[0]] + [row[1].split('(')[0].strip()] + [row[2]] + [row[3]] + [row[4]]
                rows.append(new_row)

        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)  # Başlık satırını yaz
            writer.writerows(rows)   # Yeni satırları yaz

        self.stdout.write(self.style.SUCCESS(f"New CSV file created: {output_csv}"))
