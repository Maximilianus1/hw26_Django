# Generated by Django 4.2.13 on 2024-08-19 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0009_archive_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='MagicFruit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('color', models.CharField(max_length=50, verbose_name='Цвет')),
                ('quantity', models.IntegerField(verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Магический фрукт',
                'verbose_name_plural': 'Магические фрукты',
            },
        ),
    ]
