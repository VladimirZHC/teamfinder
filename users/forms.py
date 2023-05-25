from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm
    )
from django import forms
from .models import CustomUser, Profile, Team
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['full_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Имя и Фамилия'
        })

        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Телефон'
        })

        self.fields['password1'].widget.attrs.update({
            'autocomplete': 'new-password',
            'class': 'form-control',
            'placeholder': 'Пароль'
        })

        self.fields['password2'].widget.attrs.update({
            'autocomplete': 'new-password',
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Еmail'
        })

        self.fields['date_birth'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Год рождения'
        })

    # def clean_email(self):
    #     form_data = self.cleaned_data
    #     mail = str(form_data['email'])
    #     domen = mail.split('@')
    #     if domen[1] != 'edu.hse.ru':
    #         msg = 'Неправильное окончание домена второго уровня! Должно быть - edu.hse.ru'
    #         self.add_error('email', msg)
    #     return mail

    full_name = forms.CharField(max_length=100, label='', required=True)
    phone_number = forms.CharField(max_length=50, label='', required=False)
    password1 = forms.CharField(widget=forms.PasswordInput, label='', required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label='', required=True)
    email = forms.EmailField(max_length=100, label='', required=True)
    date_birth = forms.CharField(max_length=50, label='', required=False)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'phone_number', 'password1', 'password2', 'email', 'date_birth']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['full_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ''
        })

        self.fields['date_birth'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ''
        })

        self.fields['town'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ''
        })

        self.fields['instagram'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Instagram'
        })

        self.fields['vk'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'VK'
        })

        self.fields['facebook'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Facebook'
        })

        self.fields['twitter'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Instagram'
        })

        self.fields['info'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ''
        })

        self.fields['education'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ''
        })

        self.fields['work_experience'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ''
        })

        self.fields['public_activities'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ''
        })

    full_name = forms.CharField(max_length=100, label='Ваше имя', required=False)
    date_birth = forms.CharField(max_length=50, label='Дата рождения', required=False)
    town = forms.CharField(max_length=50, label='Город проживания', required=False)
    instagram = forms.URLField(max_length=150, widget=forms.URLInput, label='', required=False)
    vk = forms.URLField(max_length=150, widget=forms.URLInput, label='', required=False)
    facebook = forms.URLField(max_length=150, widget=forms.URLInput, label='', required=False)
    twitter = forms.URLField(max_length=150, widget=forms.URLInput, label='', required=False)
    info = forms.CharField(max_length=400, label='О себе', widget=forms.TextInput, required=False)
    education = forms.CharField(max_length=50, label='Образование', required=False)
    work_experience = forms.CharField(max_length=512, label='Опыт работы', required=False)
    public_activities = forms.CharField(max_length=512, label='Ощественная деятельность', required=False)

    class Meta:
        model = Profile
        fields = (
            'full_name',
            'date_birth',
            'town',
            'instagram',
            'vk',
            'facebook',
            'twitter',
            'info',
            'education',
            'work_experience',
            'public_activities'
            )


class ProfileImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['img'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Обновите фотографию'
        })

    img = forms.ImageField(label='Выбрать фотографию', required=False, widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['img']


class TeamCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Название команды'
        })

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Описание команды'
        })

        self.fields['count_of_players'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Колличество человек'
        })

        self.fields['members'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Колличество человек',
        })

    name = forms.CharField(max_length=50, label='', required=False)
    description = forms.CharField(max_length=512, label='', widget=forms.TextInput, required=False)
    count_of_players = forms.CharField(max_length=50, widget=forms.NumberInput, label='', required=False)
    members = forms.ModelMultipleChoiceField(queryset=Profile.objects.all(), label='Участники команды', required=False)

    class Meta:
        model = Team
        fields = ['name', 'description', 'count_of_players', 'members']
