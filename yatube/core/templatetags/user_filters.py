from django import template
from django.db.models import Count
from posts.models import Post
from users.models import User

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.simple_tag
def total_posts():
    """Выводит общее количество постов."""
    return Post.objects.count()


@register.simple_tag
def total_users():
    """Выводит общее количество зарегистрированных пользователей."""
    return User.objects.count()


@register.inclusion_tag('posts/includes/latest_posts.html')
def show_latest_posts(count=5):
    """Выводит 5 последних постов."""
    latest_posts = Post.objects.order_by('-pub_date')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    """Выводит самые обсуждаемые записи."""
    return Post.objects.annotate(
        total_comments=Count('comments')).order_by('-total_comments')[:count]
