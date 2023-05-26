import re

from django import forms

from web.models import User, StockMarket, StockType


class RegistrationForm(forms.Form):
    email = forms.EmailField(label="Электропочта:")
    username = forms.CharField(label="Имя пользователя:")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-field"}), label="Пароль:")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-field"}), label="Повторите пароль:")
    avatar = forms.ImageField(required=False, label="Аватар:")
    # avatar.widget.attrs.update({"class": "center"})
    # email.widget.attrs.update({"class": "form-field"})
    # username.widget.attrs.update({"class": "form-field"})

    def clean(self):
        cleaned_data = super().clean()
        if not re.search(r'^(?=.*\W)(?=.*\D)(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,15}$',
                         cleaned_data['password']):
            self.add_error('password', 'Пароль слишком простой! '
                                       'Он должен включать в себя '
                                       'как минимум одну заглавную латинскую букву, '
                                       'одну строчную, одну цифру и один небуквенный '
                                       'и нецифровой символ. '
                                       'Количество символов в пароле '
                                       'должно быть от 8 до 15.')
        elif cleaned_data['password'] != cleaned_data['password2']:
            self.add_error('password2', 'Пароли не совпадают!')
        elif User.objects.filter(username=cleaned_data['username']).exists():
            self.add_error('username', 'Пользователь с таким именем уже существует!')
        elif User.objects.filter(email=cleaned_data['email']).exists():
            self.add_error('email', 'Пользователь с такой почтой уже существует!')
        return cleaned_data


class AuthorizationForm(forms.Form):
    username = forms.CharField(label="Имя пользователя:")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-field"}), label="Пароль:")
    username.widget.attrs.update({"class": "form-field"})


class StockFilterForm(forms.Form):
    all_markets = StockMarket.objects.all()
    all_types = StockType.objects.all()
    market_list, type_list = [], []

    for market in all_markets:
        market_list.append((market.id, market.title))
    for type in all_types:
        type_list.append((type.id, type.title))

    market = forms.ChoiceField(
        choices=(
            ('', 'Все'),
            *market_list
        ),
        required=False,
        label='Биржа:'
    )

    type = forms.ChoiceField(
        choices=(
            ('', 'Все'),
            *type_list
        ),
        required=False,
        label='Тип ЦБ:'
    )

    search_title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Поиск по названию'}),
        required=False,
        label='Название:'
    )

    search_tag = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Поиск по тегу'}),
        required=False,
        label='Тег:'
    )
