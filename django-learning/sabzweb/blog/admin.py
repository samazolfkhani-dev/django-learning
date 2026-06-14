from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin
# Register your models here.

#inlines
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ['body']
    readonly_fields = ['name' , 'created' , 'body']

class ImageInline(admin.TabularInline):
    model = Image
    extra = 0
    readonly_fields = ['created']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [ 'title' , 'author' , 'publish' , 'status' ]
    ordering = ['title' , 'publish']
    list_filter = ['status' , 'author' , 'publish' ]
    search_fields = ['title' , 'description']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    prepopulated_fields = {'slug' : ['title']}
    list_editable = ['status' ]
    list_display_links = ['title' , 'author']
    inlines = [ CommentInline , ImageInline ]

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['subject' , 'name' , 'phone']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin) :
    list_display = ['post' , 'name' , 'created' , 'active']
    list_filter = ['created' , 'active' , 'updated']
    serach_fields = ['name' , 'body']
    list_editable = [ 'active']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post' , 'title' , 'created' ]