from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.contrib.auth.models import User

# def validate_even(val):
#     if val % 2 != 0:
#         raise ValidationError('Число %(value)s нечетно', code='Error price', params={'value': val})
    

# class MinMaxValueVallidator:
#     def __init__(self, min_value, max_value):
#         self.min_value = 5
#         self.max_value = 20

#     def __call__(self, val):
#         if val < self.min_value or val > self.max_value:
#             raise ValidationError(
#                 'Введенное значение далжно находиться в дипазоне от %(min)s до %(max)s',
#                 code='out_of_range',
#                 params={'min': self.min_value, 'max': self.max_value}
#             )

class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Spare(models.Model):
    name = models.CharField(max_length=30)

class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare)

class MagicFruit(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    color = models.CharField(max_length=50, verbose_name='Цвет')
    quantity = models.IntegerField(verbose_name='Количество')
    class Meta:
        verbose_name_plural = 'Магические фрукты'
        verbose_name = 'Магический фрукт'
class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')

    def get_absolute_url(self):
        return "/bboard/%s/" % self.pk
    
    # def save(self, *args, **kwargs):
    #     if self.is_model_correct():
    #         super().save(*args, **kwargs)
    #     else:
    #         print("Model is not correct. Not saving.")

    # def delete(self, *args, **kwargs):
    #     if self.need_to_delete():
    #         super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']

class Bb(models.Model):
    def clean(self):
        errors ={}
        if not self.content:
            errors['content'] = ValidationError('Укажите описание продаваемого товара')
        if self.price and self.price < 0:
            errors['price'] = ValidationError('Укажите правильное значение')
        if errors:
            errors[NON_FIELD_ERRORS] = ValidationError('Ошибка в модели')

    class Kinds(models.TextChoices):
        BUY = 'b', "Куплю"
        SELL = 's', "Продам"
        EXCHANGE = 'c', "Обменяю"
        RENT = 'r'

    kind = models.CharField(max_length=1, choices=Kinds.choices, default=Kinds.SELL)
    rubric = models.ForeignKey(Rubric, null=True, on_delete=models.PROTECT, verbose_name='Рубрика')
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(verbose_name='Опубликованно')

    def title_and_price(self):
        if self.price:
            return '%s (%.2f)' % (self.title, self.price)
        else:
            return self.title

    title_and_price.short_description = 'Название и цена'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['rubric']
        # order_with_respect_to = 'rubric'

class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    birthDate = models.DateField(null=True, blank=True, verbose_name='Дата Рождения')
    biography = models.TextField(null=True, blank=True, verbose_name='Биография')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Авторы'
        verbose_name = 'Автор'


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    publicationDate = models.DateField(verbose_name='Дата публикации')
    authors = models.ManyToManyField(Author, verbose_name='Авторы' )
    aboutBook = models.TextField(null=True, blank=True, verbose_name='О книге')

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'Книги'
        verbose_name = 'Книга'

class Archive(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    count = models.IntegerField(null=True,blank=True)


class Measure(models.Model):
    class Measurements(float, models.Choices):
        METERS = 1.0, 'Метры'
        FEET = 0.3048, 'Футы'
        YARDS = 0.9144, 'Ярда'

    measurement = models.FloatField(choices=Measurements.choices)



class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text