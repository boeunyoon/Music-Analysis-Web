# Generated by Django 4.1.2 on 2022-11-15 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0022_recommendation'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='genre',
            field=models.TextField(default=None, null=True),
        ),
    ]
