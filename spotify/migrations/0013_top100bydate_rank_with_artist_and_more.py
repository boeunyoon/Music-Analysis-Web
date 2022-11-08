# Generated by Django 4.1.2 on 2022-11-08 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0012_alter_musicstatus_popularity'),
    ]

    operations = [
        migrations.AddField(
            model_name='top100bydate',
            name='rank_with_artist',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='top100bydate',
            name='rank_with_img300',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='top100bydate',
            name='rank_with_img64',
            field=models.TextField(default=None, null=True),
        ),
    ]