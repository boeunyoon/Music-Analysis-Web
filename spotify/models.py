from email.policy import default
from django.db import models


class Date(models.Model):
    date = models.CharField(max_length=10)

class Period(models.Model):
    start_date = models.CharField(max_length=10)
    end_date = models.CharField(max_length=10)

class Keyword(models.Model):
    keyword = models.TextField()

class StatusInput(models.Model):
    name = models.TextField()
    input = models.FloatField()

class Recommendation(models.Model):
    track_id = models.TextField()
    artist_id = models.TextField()
    genre = models.TextField(default = None, null=True)

class Top100ByDate(models.Model):
    date = models.CharField(max_length=10, primary_key=True)
    rank = models.TextField()
    rank_with_artist = models.TextField(default = None, null=True)
    rank_with_img64 = models.TextField(default = None, null=True)
    rank_with_img300 = models.TextField(default = None, null=True)
    rank_with_img640 = models.TextField(default = None, null=True)
    #top100까지의 평균 스탯
    acousticness = models.FloatField(default = None, null=True) 
    danceability = models.FloatField(default = None, null=True)
    energy = models.FloatField(default = None, null=True)
    liveness = models.FloatField(default = None, null=True)
    loudness = models.FloatField(default = None, null=True)
    valence = models.FloatField(default = None, null=True)
    mode = models.FloatField(default = None, null=True)
    speechiness = models.FloatField(default = None, null=True)
    instrumentalness = models.FloatField(default = None, null=True)
    tempo = models.FloatField(default = None, null=True)
    duration_ms = models.IntegerField(default = None, null=True)
    popularity = models.IntegerField(default = 0)
    lastweek_rank = models.TextField(default = None, null = True)
    def __str__(self):
        return self.date


class AnalysisByKeyword(models.Model):
    keyword = models.TextField()
    start_date = models.CharField(max_length=10)
    end_date = models.CharField(max_length=10)
    #키워드별 평균 스탯
    acousticness = models.FloatField() 
    danceability = models.FloatField()
    energy = models.FloatField()
    liveness = models.FloatField()
    loudness = models.FloatField()
    valence = models.FloatField()
    mode = models.FloatField() 
    speechiness = models.FloatField()
    instrumentalness = models.FloatField()
    tempo = models.FloatField()
    duration_ms = models.IntegerField()
    popularity = models.IntegerField(default = 0)

class SearchTitle(models.Model):
    search = models.TextField()

    def __str__(self):
        return self.search


class AlbumImage(models.Model):
    track_id = models.TextField(primary_key=True)
    title = models.TextField()
    artist = models.TextField()
    img640 = models.TextField()
    img300 = models.TextField()
    img64 = models.TextField()

class MusicStatus(models.Model):
    track_id = models.TextField(primary_key=True)
    title = models.TextField()
    artist = models.TextField()
    artist_id = models.TextField(null=True)
    acousticness = models.FloatField(null=True) 
    danceability = models.FloatField(null=True)
    energy = models.FloatField(null=True)
    liveness = models.FloatField(null=True)
    loudness = models.FloatField(null=True)
    valence = models.FloatField(null=True)
    mode = models.IntegerField(null=True) #  major(장조) = 1, minor(단조) =0
    #새로 추가된 모델
    speechiness = models.FloatField(null=True)
    instrumentalness = models.FloatField(null=True)
    tempo = models.FloatField(null=True)
    duration_ms = models.IntegerField(null=True)
    popularity = models.IntegerField(default = 0, null=True)

class ArtistInfo(models.Model):
    artist_id = models.TextField(primary_key=True)
    artist = models.TextField()
    followers = models.IntegerField()
    genres = models.TextField()
    img640 = models.TextField()
    img300 = models.TextField()
    img64 = models.TextField()
    popularity = models.IntegerField()
    related_artists = models.TextField()

class ArtistTopTracks(models.Model):
    artist_id = models.TextField(primary_key=True)
    top_tracks = models.TextField()
    acousticness = models.FloatField() 
    danceability = models.FloatField()
    energy = models.FloatField()
    liveness = models.FloatField()
    loudness = models.FloatField()
    valence = models.FloatField()
    mode = models.FloatField() 
    speechiness = models.FloatField()
    instrumentalness = models.FloatField()
    tempo = models.FloatField()
    duration_ms = models.IntegerField()
    popularity = models.IntegerField()