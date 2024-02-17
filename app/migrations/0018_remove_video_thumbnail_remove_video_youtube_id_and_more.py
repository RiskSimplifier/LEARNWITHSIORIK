# Generated by Django 4.2.4 on 2023-11-10 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_remove_video_uploaded_at_remove_video_video_upload_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='thumbnail',
        ),
        migrations.RemoveField(
            model_name='video',
            name='youtube_id',
        ),
        migrations.AddField(
            model_name='video',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='video_file',
            field=models.FileField(null=True, upload_to='Media/videos/'),
        ),
    ]
