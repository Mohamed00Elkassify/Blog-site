from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
# PublishedManager is a custom manager that retrieves all posts with the status of published
class PublishedManager(models.Manager):
    def get_queryset(self):
        return (super().get_queryset().filter(status=Post.Status.PUBLISHED))

# Post model is a database table that stores blog posts
class Post(models.Model):
    # Status is a class that defines a set of choices for the status field
    class Status(models.TextChoices): 
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, 
                            unique_for_date='publish')# unique_for_date creates unique slugs for posts published on the same date
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
        )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created  = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    objects = models.Manager() # the default manager
    published = PublishedManager() # the custom manager

    # metadata
    class Meta:
        # newest posts first
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
    
    # get_absolute_url method returns the canonical URL for the object
    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[self.publish.year,
                  self.publish.month,
                  self.publish.day,
                  self.slug]
                )
    
# comment model to store comments on blog posts
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default = True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

        def __str__(self):
            return f'comment by {self.name} on {self.post}'
        
