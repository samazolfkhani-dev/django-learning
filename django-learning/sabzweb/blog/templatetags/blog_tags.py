from django import template
from ..models import Post , Comment
from django.db.models import Count
register = template.Library()

@register.simple_tag
def total_comment ():
    return Post.published.count()

@register.simple_tag
def total_comment():
    return Comment.objects.filter(active=True).count()

@register.simple_tag
def last_post_date():
    return Post.published.last().publish

@register.inclusion_tag('partials/last_posts.html')
def last_posts(count=4):
    l_posts = Post.published.order_by('-publish')[:count]
    context = {
        'l_posts': l_posts
    }
    return context

@register.simple_tag
def popular_posts(count=4):
    return Post.published.annotate(comment_count=Count('comments')).order_by('-comment_count')[:count]