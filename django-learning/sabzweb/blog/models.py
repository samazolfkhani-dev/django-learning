from django.db import models
from django_jalali.db import models as jmodels
from django.urls import reverse
# Create your models here.

#Managers
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = Post.Status.PUBLISHED)

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF' , 'Draft'
        PUBLISHED = 'PB' , 'Published'
        REJECTED = 'RJ' , 'Rejected'
    #relational
    author = models.ForeignKey(User , on_delete=models.CASCADE , related_name='user_posts')
    #data field
    title = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(max_length=250)
    #date
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #choice field
    status = models.CharField(max_length=2 , choices=Status.choices, default=Status.DRAFT)

    reading_time = models.PositiveIntegerField()

    #Managers
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail' , args=[self.id])

class Ticket(models.Model):
    message = models.TextField(verbose_name='Message')
    name = models.TextField(verbose_name='Name' , max_length=250)
    email = models.EmailField(verbose_name='Email')
    phone = models.TextField(verbose_name='Phone')
    subject = models.TextField(verbose_name='Subject')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.subject


class Comment(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="comments" , verbose_name="post")
    name = models.CharField(verbose_name="name" , max_length=250)
    body = models.TextField(verbose_name="message")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta :
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = "comment"
        verbose_name_plural = "comments"

    def __str__(self):
        return f"{self.name} : {self.post}"