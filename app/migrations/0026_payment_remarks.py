# Generated by Django 4.2.4 on 2024-02-09 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_delete_cybersourcetransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
    ]