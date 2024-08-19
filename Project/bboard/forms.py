from django.forms import ModelForm, Form, CharField,DecimalField
from django import forms
from .models import Bb,AdvUser,MagicFruit
from django.core import validators
from django.core.validators import ValidationError
from django.utils import timezone
class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric', 'published')
class BbCheckForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'price')


class RegUserForm(forms.ModelForm):
    nickname = forms.CharField(label="Имя пользователя", widget=forms.widgets.TextInput,
                               help_text='Ваше имя пользователя не должно содержать спец. символов кроме пробела и нижнего подчёркивания его видят пользователи сайта',
                                   validators=[validators.RegexValidator(regex='^[a-zA-Z0-9_ ]+$')])
    login = forms.BooleanField(label="Логин", widget=forms.widgets.TextInput, help_text='Логин служит для входа на сайт не должен содержать спец. символы кроме нижнего подчёркивания',
                                   validators=[validators.RegexValidator(regex='^[a-zA-Z0-9_]+$')])
    # password = forms.PasswordInput(label='Пароль', widget=forms.widgets.TextInput,
    #                                help_text='Вводите пароль больше шести символов чтобы потом входить на сайт',
    #                                validators=[validators.RegexValidator(regex='^.(6,)$')])
    birth_date = forms.DateField(label='Дата рождния', widget=forms.widgets.DateInput, help_text='Введите важу дату рождения, нужно для подтверждения правомерности прибывания на сайте')
    email = forms.EmailField(label='Электронная почта', widget=forms.widgets.EmailInput,
                             help_text='Введите вашу электронную почту, нужно для передачи вам уведомлений и средство связи с вами в случае необходимости',
                             validators=[validators.RegexValidator(regex='^[a-zA-Z0-9._%+-]+@example\.com$')])
    class Meta:
        model=AdvUser
        fields = ('nickname','login','birth_date','email')
    def clean(self):
        super().clean()
        errors = {}
        if (timezone.now().date() - self.cleaned_data.get('birth_date')).year < 18:
            errors['birth_date']= ValidationError("Вы должны быть совершеннолетним")
        if errors:
            raise ValidationError(errors)

class MagicFruitForm(forms.ModelForm):
    name = forms.CharField(label='Название магического фрукта', widget=forms.widgets.TextInput,
                           help_text="Имя магического фрукта не должно содержать спец символов и цифр кроме пробела",
                           validators=[validators.RegexValidator(regex='^[a-zA-Zа-яА-ЯЁё ]+$')])
    color = forms.CharField(label='Цвет фрукта', widget=forms.widgets.TextInput,
                            help_text="Имя магического фрукта не должно содержать спец символов и цифр кроме тире ",
                            validators=[validators.RegexValidator(regex='^[a-zA-Zа-яА-ЯЁё\- ]+$')])
    quantity = forms.IntegerField(label='Количество фруктов', widget=forms.widgets.TextInput,
                                  help_text="Ничего кроме целых чисел")
    class Meta:
        model=MagicFruit
        fields = ('name','color','quantity')