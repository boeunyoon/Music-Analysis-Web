# Generated by Django 4.1.2 on 2022-11-22 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0023_recommendation_genre'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtistInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_id', models.TextField()),
                ('artist', models.TextField()),
                ('followers', models.IntegerField()),
                ('genres', models.TextField()),
                ('img640', models.TextField()),
                ('img300', models.TextField()),
                ('img64', models.TextField()),
                ('popularity', models.IntegerField()),
                ('realted_artists', models.TextField()),
                ('top_tracks', models.TextField()),
            ],
        ),
    ]
