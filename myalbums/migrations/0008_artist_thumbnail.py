# Generated by Django 3.1 on 2020-08-26 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myalbums', '0007_song_song'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='thumbnail',
            field=models.ImageField(default='default.jpeg', upload_to='thumbnails'),
        ),
    ]
