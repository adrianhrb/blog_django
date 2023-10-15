from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone


# Manager to filter only published Posts
class PublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    # Status field possible values
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    # Model fields

    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    objects = models.Manager()  # Default manager
    published = PublishedManager()  # Our custom manager

    class Meta:
        """Defines metadata for the model with some attributes"""

        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]

    def __str__(self):
        return self.title
