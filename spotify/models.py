from django.db import models


class Date(models.Model):
    date = models.CharField(max_length=11)

    def __str__(self):
        return self.date

class SearchTitle(models.Model):
    search = models.TextField()


class MusicStatus(models.Model):
    track_id = models.TextField()
    title = models.TextField()
    artist = models.TextField()
    acousticness = models.FloatField() 
    danceability = models.FloatField()
    energy = models.FloatField()
    liveness = models.FloatField()
    loudness = models.FloatField()
    valence = models.FloatField()
    mode = models.FloatField() #  major(장조) = 1, minor(단조) = 0 