# Generated by Django 4.1.2 on 2022-11-08 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0015_analysisbykeyword'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysisbykeyword',
            name='mode',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='top100bydate',
            name='mode',
            field=models.FloatField(),
        ),
    ]