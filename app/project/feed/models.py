from django.db import models
from django.conf import settings
from project.api.helpers import code_generator


class Tag(models.Model):
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
        to=Tag,
        blank=True
    )
    content = models.TextField(
        verbose_name="post content",
    )
    created = models.DateTimeField(
        verbose_name="post created",
        auto_now_add=True,
    )
    shared = models.ForeignKey(
        verbose_name='shared',
        to='self',
        on_delete=models.CASCADE,
        related_name='shares',
        null=True
    )

    class Meta:  # changes default settings
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
        to='Post',
        related_name='likes',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        unique_together = [
            ('user', 'post'),
        ]


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

    def new_code(self):
        self.registration_code = code_generator()
        self.save()
        return self.registration_code

    def __str__(self):
        return self.user.username


class FriendRequests(models.Model):
    DEFAULT_STATUS = 'open'
    STATUS_CHOICES = [
        (DEFAULT_STATUS, 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    request_from = models.ForeignKey(
        verbose_name='sent friend request',
        to=settings.AUTH_USER_MODEL,
        related_name='sent_requests',
        on_delete=models.CASCADE,
    )
    request_to = models.ForeignKey(
        verbose_name='received friend request',
        to=settings.AUTH_USER_MODEL,
        related_name='received_requests',
        on_delete=models.CASCADE,

    )
    request_status = models.CharField(
        verbose_name='request status',
        max_length=20,
        choices=STATUS_CHOICES,
        default=DEFAULT_STATUS,
    )

    class Meta:
        verbose_name = 'FriendRequest'
        verbose_name_plural = 'FriendRequests'
        unique_together = [
            ('request_from', 'request_to'),
            ('request_to', 'request_from')
        ]
