# Generated by Django 5.0.4 on 2024-05-07 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travels', '0003_alter_tour_options_alter_tour_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.ImageField(null=True, upload_to='image/news'),
        ),
    ]
