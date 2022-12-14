# Generated by Django 4.1.2 on 2022-11-08 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0014_top100bydate_rank_with_img640'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisByKeyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.TextField()),
                ('start_date', models.CharField(max_length=10)),
                ('end_date', models.CharField(max_length=10)),
                ('acousticness', models.FloatField()),
                ('danceability', models.FloatField()),
                ('energy', models.FloatField()),
                ('liveness', models.FloatField()),
                ('loudness', models.FloatField()),
                ('valence', models.FloatField()),
                ('mode', models.IntegerField()),
                ('speechiness', models.FloatField()),
                ('instrumentalness', models.FloatField()),
                ('tempo', models.FloatField()),
                ('duration_ms', models.IntegerField()),
                ('popularity', models.IntegerField(default=0)),
            ],
        ),
    ]
