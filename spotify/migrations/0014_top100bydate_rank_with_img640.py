# Generated by Django 4.1.2 on 2022-11-08 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0013_top100bydate_rank_with_artist_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='top100bydate',
            name='rank_with_img640',
            field=models.TextField(default=None, null=True),
        ),
    ]