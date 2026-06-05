from django import template
from django.db.models.aggregates import Min

from ..models import Post , Comment
from django.db.models import Count
from markdown import markdown
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def total_post ():
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

@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))

@register.simple_tag
def max_read_time() :
    return Post.published.order_by('-reading_time')[0]

@register.simple_tag
def min_read_time() :
    return Post.published.order_by('reading_time')[0]