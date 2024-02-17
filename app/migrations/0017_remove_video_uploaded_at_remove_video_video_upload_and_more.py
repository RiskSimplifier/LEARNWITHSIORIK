# Generated by Django 4.2.4 on 2023-11-10 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_video_uploaded_at_video_video_upload_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='uploaded_at',
        ),
        migrations.RemoveField(
            model_name='video',
            name='video_upload',
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]