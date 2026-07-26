from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from django.urls import reverse

# Create your models here.

class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    job = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    photo = models.ImageField(upload_to='accounts_images/', null=True, blank=True)

class Post(models.Model):
    #relational
    author = models.ForeignKey(User , on_delete=models.CASCADE , related_name='user_posts')
    #data field
    description = models.TextField()
    #date
    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #tags
    tags = TaggableManager()
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.author.username

    def get_absolute_url(self):
        return reverse('social:post_detail' , args=[self.id])

