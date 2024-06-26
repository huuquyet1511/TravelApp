# Generated by Django 5.0.4 on 2024-05-09 17:31

import ckeditor.fields
import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travels', '0006_ticket_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='active_like',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AlterField(
            model_name='tour',
            name='image',
            field=models.ImageField(null=True, upload_to='image/tours'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='avatar'),
        ),
    ]
