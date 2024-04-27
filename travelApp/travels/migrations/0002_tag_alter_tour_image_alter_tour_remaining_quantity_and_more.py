# Generated by Django 5.0.4 on 2024-04-27 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('tag_name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='tour',
            name='image',
            field=models.ImageField(upload_to='image/tours'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='remaining_quantity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(upload_to='image/avatar'),
        ),
        migrations.AddField(
            model_name='tour',
            name='tags',
            field=models.ManyToManyField(to='travels.tag'),
        ),
    ]