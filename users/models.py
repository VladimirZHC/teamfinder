import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from .managers import CustomUserManager
from PIL import Image


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(
        'Имя Фамилия', 
        max_length=40, 
        null=True, 
        blank=True
        )
    phone_number = models.CharField(
        'Телефон пользователя', 
        null=True, 
        blank=True,
        max_length=30
        )
    date_birth = models.CharField(
        'Возраст пользователя',
        null=True, 
        blank=True, 
        max_length=50)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        related_name='profile',
        on_delete=models.CASCADE
        )
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(
        'Имя Фамилия', 
        max_length=40, 
        null=True, 
        blank=True
        )
    town = models.CharField(
        ('Город пользователя'), 
        null=True, 
        max_length=20, 
        blank=True
        )
    phone_number = models.CharField(
        'Телефон пользователя', 
        null=True, 
        blank=True,
        max_length=30 
        )
    date_birth = models.CharField(
        'Возраст пользователя',
        null=True, 
        blank=True, 
        max_length=50)
    img = models.ImageField(
        'Фото пользователя', 
        default='default.png', 
        upload_to='user_images'
        )
    info = models.TextField('Информация о пользователе')
    education = models.CharField(
        'Информация об образовании', 
        max_length=50, 
        null=True, 
        blank=True
        )
    work_experience = models.TextField('Опыт работы',null=True, blank=True)
    public_activities = models.TextField('Общественная деятельность',null=True, blank=True)
    teams = models.ManyToManyField(
        'Team',
        verbose_name='Мои команды',
        blank=True,
        related_name='teams'
        )
    
    instagram = models.URLField(
        max_length=100, 
        blank=True, 
        null=True, 
        )
    vk = models.URLField(
        max_length=100, 
        blank=True, 
        null=True, 
        )
    facebook = models.URLField(
        max_length=100, 
        blank=True, 
        null=True, 
        )
    twitter = models.URLField(
        max_length=100, 
        blank=True, 
        null=True, 
        )
    active_team_id = models.IntegerField(default=0)
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        super().save()
        
        image = Image.open(self.img.path)
        
        if image.height > 512 or image.width > 512:
            resize = (512, 512)
            image.thumbnail(resize)
            image.save(self.img.path)
            
    def get_date_birth(self):
        now = datetime.datetime.now()
        if self.date_birth:
            year = int(self.date_birth)
            age = now.year - year
            if 11 <= age <= 19 or age % 10 == 1:
                return f"{age} год"
            elif 2 <= age % 10 <= 4:
                return f"{age} года"
            else:
                return f"{age} лет"
        else:
            return self.date_birth
        
    def get_userprofile_teams(self):
        return self.teams.name     
        
    
    def __str__(self):
        return f'{self.user.email}'
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
    
class Team(models.Model):
    
    #Cтатус команды
    ACTIVE = 'active'
    DELETED = 'deleted'
    
    CHOICES_STATUS  = (
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted')
    )
    
    name = models.CharField(
        'Наименование команды',
        max_length=64, 
        )
    description = models.CharField(
        'Описание команды', 
        max_length=1024,
        null=True, 
        blank=True
        )
    owner = models.ForeignKey(
        CustomUser, 
        related_name='created_teams',
        verbose_name='Автор команды', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        )
    members = models.ManyToManyField(
        CustomUser, 
        related_name='users_teams',
        verbose_name='Участники',
        blank=True,
        )
    count_of_players = models.IntegerField('Число участников')
    created_at = models.DateTimeField(
        'Дата cоздания команды', 
        auto_now_add=True, 
        null=True, 
        blank=True
        )
    img = models.ImageField(
        'Фото команды', 
        default='default-team.png', 
        upload_to='user_images'
        )
    
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=ACTIVE)
    
    def __str__(self):
        return f'{self.name}'
    
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Команду'
        verbose_name_plural = 'Команды'
             
        
      
STATUS_CHOICES  = (
        ('send', 'send'),
        ('accepted', 'accepted')
    )  
        
class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    to_team = models.ForeignKey(Team, related_name='to_team', on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    created = models.DateTimeField(
        'Cоздание', 
        auto_now_add=True, 
        null=True, 
        blank=True
        )
    updated = models.DateTimeField(
        'Обновление', 
        auto_now_add=True, 
        null=True, 
        blank=True
        )
    
    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
    
    
    class Meta:
        verbose_name = 'Приглашение'
        verbose_name_plural = 'Приглашения'