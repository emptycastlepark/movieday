# Generated by Django 2.1.15 on 2020-06-11 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200611_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='profile'),
        ),
    ]
