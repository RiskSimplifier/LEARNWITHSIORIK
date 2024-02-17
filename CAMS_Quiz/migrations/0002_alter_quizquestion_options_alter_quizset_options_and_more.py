# Generated by Django 4.2.4 on 2024-01-21 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CAMS_Quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quizquestion',
            options={'verbose_name_plural': 'Questions'},
        ),
        migrations.AlterModelOptions(
            name='quizset',
            options={'verbose_name_plural': 'Quiz Sets'},
        ),
        migrations.RemoveField(
            model_name='quizquestion',
            name='level',
        ),
        migrations.RemoveField(
            model_name='quizquestion',
            name='time_limit',
        ),
        migrations.AddField(
            model_name='quizset',
            name='time_limit',
            field=models.IntegerField(default=0),
        ),
    ]