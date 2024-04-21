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

    email = models.CharField(max_length=30, default='', unique=True) 
    grade = models.CharField(max_length=3, choices=Grade.choices, default=Grade.BEGINNER) 
    given_answers_count = models.IntegerField(default=0) 

    REQUIRED_FIELDS = ['username', 'grade', 'given_answers_count']
    USERNAME_FIELD = 'email' 
    