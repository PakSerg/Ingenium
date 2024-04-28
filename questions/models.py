from django.db import models
from users.models import User


class Question(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    title = models.CharField(max_length=120, blank=False, null=False) 
    content = models.TextField(max_length=2000, blank=False, null=False) 
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self) -> str:
        return f'{self.title} ({self.user.username})'