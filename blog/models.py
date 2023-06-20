from django.conf import settings
from django.db import models

# Create your models here.
class Post(models.Model):
    """
    Represents a blog post
    """
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # The Django auth user model
        on_delete=models.PROTECT,  # Prevent posts from being deleted
        related_name='blog_posts',  # "This" on the user model
        null=True
    )
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)  # Sets on create
    updated = models.DateTimeField(auto_now=True)  # Updates on each save
    def __str__(self):
        return self.title