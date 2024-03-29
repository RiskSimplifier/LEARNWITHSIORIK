# Generated by Django 4.2.4 on 2023-10-20 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='BLOG',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_image', models.ImageField(null=True, upload_to='Media/Blog_Image')),
                ('blog_author', models.CharField(max_length=100, null=True)),
                ('blog_date', models.DateTimeField(auto_now_add=True)),
                ('blog_category', models.CharField(max_length=100)),
                ('blog_title', models.CharField(max_length=500)),
            ],
        ),
    ]
