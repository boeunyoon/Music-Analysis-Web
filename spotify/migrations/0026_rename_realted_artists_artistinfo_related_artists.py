# Generated by Django 4.1.2 on 2022-11-22 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0025_remove_artistinfo_id_alter_artistinfo_artist_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artistinfo',
            old_name='realted_artists',
            new_name='related_artists',
        ),
    ]
