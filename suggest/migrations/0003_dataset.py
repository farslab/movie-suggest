# Generated by Django 5.0.4 on 2024-04-17 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggest', '0002_remove_movie_production_companies_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('genres', models.CharField(max_length=255)),
                ('user_id', models.IntegerField()),
                ('rating', models.FloatField()),
                ('timestamp', models.DateTimeField()),
            ],
        ),
    ]