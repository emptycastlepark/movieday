# Generated by Django 2.1.15 on 2020-06-13 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_moviereview'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviereview',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]