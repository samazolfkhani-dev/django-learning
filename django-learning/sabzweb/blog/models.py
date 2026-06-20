from email.mime import image

from django.db import models
from django_jalali.db import models as jmodels
from django.urls import reverse
from django.template.defaultfilters import slugify
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

    def save(self , *args , **kwargs):
        self.description = censor_text(self.description)
        super().save(*args , **kwargs)

    def delete(self , *args , **kwargs):
        for img in self.images.all() :
            storage , path = img.image_file.storage , img.image_file.path
            storage.delete(path)
        super().delete(*args , **kwargs)

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail' , args=[self.id])

    def save(self , *args , **kwargs):
        self.slug = slugify(self.title)
        super().save(*args , **kwargs)

class Ticket(models.Model):
    message = models.TextField(verbose_name='Message')
    name = models.TextField(verbose_name='Name' , max_length=250)
    email = models.EmailField(verbose_name='Email')
    phone = models.TextField(verbose_name='Phone')
    subject = models.TextField(verbose_name='Subject')

    def save(self , *args , **kwargs):
        self.message = censor_text(self.message)
        super().save(*args , **kwargs)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.subject

def censor_text(text):
    bad_words = ["loser"]
    for word in bad_words:
        text = text.replace(word , "*" * len(word))
    return text

class Comment(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="comments" , verbose_name="post")
    name = models.CharField(verbose_name="name" , max_length=250)
    body = models.TextField(verbose_name="message")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    def save(self , *args , **kwargs):
        self.body = censor_text(self.body)
        super().save(*args , **kwargs)

    class Meta :
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = "comment"
        verbose_name_plural = "comments"

    def __str__(self):
        return f"{self.name} : {self.post}"

class Image(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="images" , verbose_name="post")
    image_file = models.ImageField(upload_to="post_images") #verbose_name = A Name Which Is Shown To Users In Admin Panel & Forms ...
    title = models.CharField(max_length=250 , null=True , blank=True)
    description = models.TextField(null=True , blank=True)
    created = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = "image"
        verbose_name_plural = "images"

    def __str__(self):
        return self.title if self.title else self.image_file.name

    def delete(self , *args , **kwargs):
        storage , path = self.image_file.storage , self.image_file.path
        storage.delete(path)
        super().delete(*args , **kwargs)