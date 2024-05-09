# Generated by Django 5.0.4 on 2024-05-07 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travels', '0002_tag_alter_tour_image_alter_tour_remaining_quantity_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tour',
            options={},
        ),
        migrations.AlterField(
            model_name='tour',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterUniqueTogether(
            name='tour',
            unique_together={('tour_name', 'category')},
        ),
    ]