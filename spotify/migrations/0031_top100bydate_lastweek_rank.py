# Generated by Django 4.1.2 on 2022-12-08 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0030_alter_top100bydate_acousticness_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='top100bydate',
            name='lastweek_rank',
            field=models.TextField(default=None, null=True),
        ),
    ]