# Generated by Django 4.1.2 on 2022-11-08 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0016_alter_analysisbykeyword_mode_alter_top100bydate_mode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='date',
            name='date',
        ),
        migrations.AddField(
            model_name='date',
            name='end_date',
            field=models.CharField(default=None, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='date',
            name='start_date',
            field=models.CharField(default=None, max_length=10),
            preserve_default=False,
        ),
    ]
