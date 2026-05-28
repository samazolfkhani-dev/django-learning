from django import template
from ..models import Post , Comment

register = template.Library()

@register.simple_tag
def total_post ():
    return Post.published.count()

@register.simple_tag
def total_comment():
    return Comment.objects.filter(active=True).count()

@register.simple_tag
def last_post():
    return Post.published.last().publish