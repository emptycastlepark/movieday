# Generated by Django 2.1.15 on 2020-06-11 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200611_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='like_genres',
            field=models.ManyToManyField(default='default.jpg', related_name='genre_like_users', to='movies.Genre'),
        ),
    ]
