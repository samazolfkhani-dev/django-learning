from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from django.urls import reverse
from django_resized import ResizedImageField
# Create your models here.

class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    job = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    photo = ResizedImageField(upload_to='accounts_images/', size = [500 , 500] , quality = 75 , crop = ['middle' , 'center'] , null=True, blank=True)
    following = models.ManyToManyField('self' , through = 'Contact' , related_name = "followers" , symmetrical = False)


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

    likes = models.ManyToManyField(User , related_name="liked_posts" , blank=True)
    saved_by = models.ManyToManyField(User , related_name = "saved_post" , null = True)
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.author.username

    def get_absolute_url(self):
        return reverse('social:post_detail' , args=[self.id])


def censor_text(text):
    bad_words = ["loser" , "sheet"]
    for word in bad_words:
        text = text.replace(word , "*" * len(word))
    return text
class Comment(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="comments" , verbose_name="post")
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='comments')
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
        return f"{self.user.username} : {self.post}"


class Image(models.Model) :
    title = models.CharField(null = True , blank = True)
    post = models.ForeignKey(Post , on_delete = models.CASCADE , related_name = "images" , verbose_name = "image")
    description = models.CharField(null = True , blank = True)
    image_file = ResizedImageField(upload_to = "post_images/" , size = [500 , 500] , quality = 75 , crop = ['middle' , 'center'])
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta :
        indexes = [
            models.Index(fields = ['title' , 'description' , 'id'])
        ]

    def __str__(self):
        return f"{self.title} : {self.description}"
    

class contact(models.Model):
    user_from = models.ForeignKey(User , related_name = "rel_from_set" , on_delete = models.CASCADE)
    user_to = models.ForeignKey(User , related_name = "rel_to_set" , on_delete = models.CASCADE)
    created = models.DateField(auto_now_add = True)

    class Meta:
        indexes = [
            models.Index(fields=['-created'])
        ]
        ordering = ['-created']

    def __str__(self):
        return f"{self.user_from.username} Follows {self.user_to.username}."

