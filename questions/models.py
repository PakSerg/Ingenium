from django.db import models
from users.models import User


class Category(models.Model): 
    title = models.CharField(max_length=30, null=False, unique=True) 
    description = models.CharField(max_length=200, null=False, unique=True)

    def __str__(self) -> str: 
        return f'{self.title}'
    

class Question(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=120, blank=False, null=False) 
    content = models.TextField(max_length=2000, blank=False, null=False) 
    created_at = models.DateTimeField(auto_now_add=True) 
    votes = models.IntegerField(default=0, null=False)

    def __str__(self) -> str:
        return f'{self.title} ({self.user.username})'
    
