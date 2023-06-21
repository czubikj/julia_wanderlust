from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Topic(models.Model):
    name = models.CharField(
        max_length=50,
        null= False, #default, but name is required!
        unique=True  # No duplicates!
    )
    slug = models.SlugField(
        unique=True,
        null=False #default, but slug is required!
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=self.model.PUBLISHED)
    def draft(self):
        return self.filter(status=self.model.DRAFT)

class Post(models.Model):
    """
    Represents a blog post
    """
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]

    title = models.CharField(
        max_length=255,
        null=False # This is a required field, though I know default for CharField is null=False
    )
    slug = models.SlugField(
        null=False,
        help_text='The date & time this article was published',
        unique_for_date='published',  # Slug is unique for publication date
    )
    topics = models.ManyToManyField(
        Topic,
        related_name='blog_posts'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # The Django auth user model
        on_delete=models.PROTECT,  # Prevent posts from being deleted
        related_name='blog_posts',  # "This" on the user model
        null=False
    )
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)  # Sets on create
    updated = models.DateTimeField(auto_now=True)  # Updates on each save
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "published" to make this post publicly visible',
    )
    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date & time this article was published',
    )

    objects = PostQuerySet.as_manager()

    def publish(self):
        """Publishes this post"""
        self.status = self.PUBLISHED
        self.published = timezone.now()
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Comment(models.Model): #Comment model where visitors can write comments on your posts
    post = models.ForeignKey( #	A relationship to the Post model
        Post,
        on_delete=models.CASCADE, #if post is deleted, so will the comment
        related_name='comments',
        null=False
    )
    name = models.CharField( #The name of the person making the comment
        max_length=50, #limited number of characters
        null=False #this a required field!
    )
    email = models.EmailField( #The email address for the commenter, emailfield validates the email!
        max_length=100, #max length for email
        null=False #this is a required field!
    )
    text = models.TextField( #field containing the actual comment
        null=False,
        max_length = 1000 #limit the number of characters so users don't get carried away (optional)
    )
    approved = models.BooleanField( #boolean field intended for comment moderation
        default=False
    )
    created = models.DateTimeField(auto_now_add=True)  # Sets on create
    updated = models.DateTimeField(auto_now=True)  # Updates on each save

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return 'Comment by '+ str(self.name)
