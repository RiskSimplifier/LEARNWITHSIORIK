# Generated by Django 4.2.4 on 2024-01-20 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CAMS_Res', '0002_cams_files_files_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cams_files',
            name='owner',
        ),
    ]