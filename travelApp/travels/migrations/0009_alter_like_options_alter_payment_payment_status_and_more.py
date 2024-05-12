# Generated by Django 5.0.4 on 2024-05-12 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travels', '0008_rename_active_like_like_liked_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='like',
            options={},
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'news')},
        ),
    ]
