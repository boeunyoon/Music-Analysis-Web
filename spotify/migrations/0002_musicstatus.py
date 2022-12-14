# Generated by Django 4.1.1 on 2022-10-18 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MusicStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_id', models.TextField()),
                ('title', models.TextField()),
                ('artist', models.TextField()),
                ('acousticness', models.FloatField()),
                ('danceability', models.FloatField()),
                ('energy', models.FloatField()),
                ('liveness', models.FloatField()),
                ('loudness', models.FloatField()),
                ('valence', models.FloatField()),
                ('mode', models.FloatField()),
            ],
        ),
    ]
