# Generated by Django 4.1.2 on 2022-11-02 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0005_remove_date_rank_remove_musicstatus_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='musicstatus',
            name='img300',
            field=models.TextField(default=None),
        ),
        migrations.AddField(
            model_name='musicstatus',
            name='img64',
            field=models.TextField(default=None),
        ),
        migrations.AddField(
            model_name='musicstatus',
            name='img640',
            field=models.TextField(default=None),
        ),
    ]