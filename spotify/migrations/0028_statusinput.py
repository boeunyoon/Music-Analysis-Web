# Generated by Django 4.1.2 on 2022-11-28 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0027_artisttoptracks_remove_artistinfo_top_tracks'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('input', models.TextField()),
            ],
        ),
    ]
