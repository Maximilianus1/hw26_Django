# Generated by Django 4.2.13 on 2024-08-12 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0007_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('birthDate', models.DateField(blank=True, null=True, verbose_name='Дата Рождения')),
                ('biography', models.TextField(blank=True, null=True, verbose_name='Биография')),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('publicationDate', models.DateField(verbose_name='Дата публикации')),
                ('aboutBook', models.TextField(blank=True, null=True, verbose_name='О книге')),
                ('authors', models.ManyToManyField(to='bboard.author', verbose_name='Авторы')),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Книги',
            },
        ),
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bboard.author')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bboard.book')),
            ],
        ),
    ]