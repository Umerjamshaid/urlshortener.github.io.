# Generated by Django 4.1.13 on 2024-09-21 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_url', models.URLField(max_length=500)),
                ('short_code', models.CharField(blank=True, max_length=6, unique=True)),
            ],
        ),
    ]
