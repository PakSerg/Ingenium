from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class Grade(models.TextChoices):
        BEGINNER = 'BEG', 'Новичок'
        HELPER = 'HLP', 'Помощник'
        MASTER = 'MAS', 'Мастер'
        EXPERT = 'EXP', 'Эксперт'
        PROFESSIONAL = 'PRO', 'Профессионал' 
        GURU = 'GUR', 'Гуру' 
        VIRTUOSO = 'VIR', 'Виртуоз' 
        SAGE = 'SAG', 'Мудрец' 
        LEGEND = 'LEG', 'Легенда'

    email = models.EmailField(unique=True) 
    grade = models.CharField(max_length=3, choices=Grade.choices, default=Grade.BEGINNER) 
    given_answers_count = models.IntegerField(default=0) 
    image = models.ImageField(upload_to='users/%Y/%m/%d', default='users/default_profile_image.png', null=False)
    description = models.CharField(max_length=120, default="", null=False, blank=True)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']

    def __str__(self): 
        return f'{self.username}'