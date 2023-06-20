# Generated by Django 4.2.1 on 2023-06-20 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(help_text='The date & time this article was published', null=True, unique_for_date='published'),
        ),
    ]
