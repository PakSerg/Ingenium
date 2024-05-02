from django.db import models
from users.models import User
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class Category(models.Model): 
    title = models.CharField(max_length=30, null=False, unique=True) 
    description = models.CharField(max_length=200, null=False, unique=True) 
    slug = models.SlugField(null=False, default="", unique=True)

    def __str__(self) -> str: 
        return f'{self.title}'
    
    def get_absolute_url(self): 
        return reverse('questions:category',
                        args=[self.slug])
    
    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.title))
        return super(Category, self).save(*args, **kwargs)
    

class Tag(models.Model): 
    text = models.CharField(max_length=20, null=False, unique=True)
    slug = models.SlugField(unique=True, null=False)
    category = models.ForeignKey(Category, null=False, default=1, on_delete=models.CASCADE, 
                                 related_name='tags')
    
    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.text))
        return super(Tag, self).save(*args, **kwargs)
    
    def get_absolute_url(self): 
        return reverse('questions:tag',
                        args=[self.slug])


class Question(models.Model): 

    class Status(models.TextChoices): 
        DRAFT = 'DF', 'Черновик'
        PUBLISHED = 'PB', 'Опубликован'
        BANNED = 'BN', 'В бане'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions') 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, 
                                 related_name='categories')
    title = models.CharField(max_length=120, blank=False, null=False) 
    content = models.TextField(max_length=2000, blank=False, null=False) 
    created_at = models.DateTimeField(auto_now_add=True) 
    votes = models.IntegerField(default=0, null=False)
    slug = models.SlugField(null=False, default="", unique=True)
    tags = models.ManyToManyField(Tag, related_name='questions')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager()

    class PublishedManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status=Question.Status.PUBLISHED) 
    published = PublishedManager()
        
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.title))
        return super(Question, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.title} ({self.user.username})' 
    
    def get_absolute_url(self): 
        return reverse('questions:single_question',
                        args=[self.created_at.year,
                                self.created_at.month,
                                self.created_at.day,
                                self.slug])
    