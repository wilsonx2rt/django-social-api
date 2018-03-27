from django.db import models
from django.conf import settings
# Create your models here.

class Tags(models.Model):
    name = models.CharField(
        verbose_name='tag name',
        max_length=20,
    )


class Post(models.Model):
    user = models.ForeignKey(
        verbose_name='user',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )

    tags = models.ManyToManyField(
        verbose_name='tags',
        to=Tags,
    )
    content = models.TextField(
        verbose_name ="post content",
    )
    created = models.DateTimeField(
        verbose_name = "post created",
        auto_now_add=True,
    )


    class Meta: # changes default settings
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created']


class Like(models.Model):
    user = models.ForeignKey(
        verbose_name='user',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='likes',
        null=True,
    )
    post = models.ForeignKey(
        verbose_name='post',
        to='feed.post',
        related_name='likes',
        on_delete=models.CASCADE,
    )


    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        unique_together = [
            ('user', 'post'),
        ]


import random
def code_generator():
    return ''.join(random.sample('0123456789', 5))

# def code_generator(length=5):
#     numbers = '0123456789'
#     return ''.join(random.choice(numbers) for i in range(length))

class UserProfile(models.Model):
    user = models.OneToOneField(
        verbose_name='user',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    following = models.ManyToManyField(
        verbose_name='following',
        to=settings.AUTH_USER_MODEL,
        related_name='followers',
    )
    registration_code = models.CharField(
        verbose_name='registration code',
        max_length=15,
        unique=True,
        default=code_generator
    )
