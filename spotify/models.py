from django.db import models

class Date(models.Model):
    date = models.CharField(max_length=11)

    def __str__(self):
        return self.date
 