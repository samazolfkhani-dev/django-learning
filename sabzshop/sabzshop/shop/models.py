from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model) : 
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length = 255 , unique = True)

    class Meta :
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category' , args = [self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category , on_delete=models.CASCADE , related_name='products')
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length = 250)
    description = models.TextField(max_length = 400)
    inventory = models.PositiveIntegerField(default = 0)
    price = models.PositiveIntegerField(default = 0)
    off = models.PositiveIntegerField(default = 0)
    new_price = models.PositiveIntegerField(default = 0)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    weight = models.PositiveIntegerField(default = 0)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields = ['id' , 'slug']) ,
            models.Index(fields = ['name']) ,
            models.Index(fields = ['-created'])
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail' , args = [self.id , self.slug])

class Image(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name = 'images')
    file = models.ImageField(upload_to='product_images')
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields = ['-created'])
        ]

class ProductFeature(models.Model):
    name = models.CharField(max_length = 250)
    value = models.CharField(max_length = 250)
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} : {self.value}'

