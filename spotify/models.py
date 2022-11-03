from email.policy import default
from django.db import models


class Date(models.Model):
    date = models.CharField(max_length=11)
    
    def __str__(self):
        return self.date

class Top100ByDate(models.Model):
    date = models.CharField(max_length=10, primary_key=True)
    rank = models.TextField()
    #top100까지의 평균 스탯
    acousticness = models.FloatField() 
    danceability = models.FloatField()
    energy = models.FloatField()
    liveness = models.FloatField()
    loudness = models.FloatField()
    valence = models.FloatField()
    mode = models.IntegerField() #  major(장조) = 1, minor(단조) =0
    speechiness = models.FloatField()
    instrumentalness = models.FloatField()
    tempo = models.FloatField()
    duration_ms = models.IntegerField()
    popularity = models.IntegerField(default = 0)
    def __str__(self):
        return self.date

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
    acousticness = models.FloatField() 
    danceability = models.FloatField()
    energy = models.FloatField()
    liveness = models.FloatField()
    loudness = models.FloatField()
    valence = models.FloatField()
    mode = models.IntegerField() #  major(장조) = 1, minor(단조) =0
    #새로 추가된 모델
    speechiness = models.FloatField()
    instrumentalness = models.FloatField()
    tempo = models.FloatField()
    duration_ms = models.IntegerField()
    popularity = models.IntegerField(default = 0)
