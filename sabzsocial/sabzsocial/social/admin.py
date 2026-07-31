from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username' , 'email' , 'phone' , 'job' , 'date_of_birth']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information' , {'fields': ('date_of_birth', 'bio' , 'job' , 'phone' , 'photo')}),
    )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author' , 'created' , 'tag_list']
    ordering = ['created']
    list_filter = ['author' , 'created' ]
    search_fields = ['description']
    raw_id_fields = ['author']
    date_hierarchy = 'created'
    list_display_links = ['author']

    def get_queryset(self , request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self , obj):
        return " , ".join(o.name for o in obj.tags.all())

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post' , 'user' , 'active']
    ordering = ['created']
    list_filter = ['active']
    list_editable = ['active']
    list_display_links = ['post' , 'user']