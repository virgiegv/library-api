# Generated by Django 4.2.1 on 2023-06-03 02:25

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('subtitle', models.CharField(max_length=300)),
                ('authors', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(), size=None)),
                ('categories', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(), size=None)),
                ('published_date', models.DateField(blank=True, null=True)),
                ('editor', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True)),
                ('image', models.URLField(blank=True, null=True)),
            ],
        ),
    ]