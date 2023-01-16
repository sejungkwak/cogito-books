# Generated by Django 3.2 on 2023-01-16 10:58

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=254)),
            ],
            options={
                'ordering': ['full_name'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, unique=True)),
                ('friendly_name', models.CharField(blank=True, max_length=254, null=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, unique=True)),
                ('friendly_name', models.CharField(blank=True, max_length=254, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=254)),
                ('desc', models.TextField()),
                ('cover_url', models.URLField(blank=True, max_length=1024, null=True)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('pages', models.IntegerField()),
                ('dimension_x', models.FloatField()),
                ('dimension_y', models.FloatField()),
                ('dimension_z', models.FloatField()),
                ('lang', models.CharField(blank=True, max_length=50, null=True)),
                ('publisher', models.CharField(max_length=254)),
                ('pub_date', models.DateField()),
                ('isbn10', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10)])),
                ('isbn13', models.CharField(max_length=13, validators=[django.core.validators.MinLengthValidator(13)])),
                ('discount_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('amount_sold', models.IntegerField()),
                ('author', models.ManyToManyField(related_name='books', to='books.Author')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='books', to='books.category')),
                ('genre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='books', to='books.genre')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
    ]
