# Generated by Django 4.1.2 on 2022-11-15 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0019_keyword'),
    ]

    operations = [
        migrations.AddField(
            model_name='musicstatus',
            name='artist_id',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='musicstatus',
            name='genre',
            field=models.TextField(null=True),
        ),
    ]