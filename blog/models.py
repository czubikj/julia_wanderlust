from django.conf import settings
from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField


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

    def get_absolute_url(self):
        return reverse(
            'topic-detail',
            kwargs={
                'slug': self.slug
            }
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
    def get_authors(self):
        User = get_user_model()
        # Get the users who are authors of this queryset
        return User.objects.filter(blog_posts__in=self).distinct()
    def get_topics(self):
        #retrieve all topics with an annotated number of posts
        return Topic.objects.annotate(num_posts=Count('blog_posts')).order_by('-num_posts')
    def post_popularity(self):
        #determine the popularity of the post by counting comments
        return self.annotate(popularity=Count('comments'))
    def get_related_topics(self):
        #retrieve the topics related to a given post
        return Topic.objects.filter(blog_posts__in=self)
    def get_popular_topics(self):
        #retrieve the top 10 posts by popularity
        top_10_posts = self.post_popularity().order_by('-popularity')[:10]
        #get the id's of the top 10 posts
        top_10_post_ids = top_10_posts.values_list('id')
        #annotate all topics with the number of posts, limited to the top 10 posts
        annotated_topics = Topic.objects.annotate(num_posts=Count('blog_posts', filter=models.Q(blog_posts__in=top_10_post_ids))).order_by('-num_posts')
        return annotated_topics
    def get_comments(self):
        rel_comments = Comment.objects.filter(blog_posts__in=selft)
        return rel_comments


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
    content = RichTextUploadingField()
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

    banner = models.ImageField(
        blank=True,
        null=True,
        help_text='A banner image for the post'
    )

    objects = PostQuerySet.as_manager()

    def publish(self):
        """Publishes this post"""
        self.status = self.PUBLISHED
        self.published = timezone.now()
    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        if self.published:
            kwargs = {
                'year': self.published.year,
                'month': self.published.month,
                'day': self.published.day,
                'slug': self.slug
            }
        else:
            kwargs = {'pk': self.pk}

        return reverse('post-detail', kwargs=kwargs)

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

    likes = models.PositiveIntegerField(default=0) #likes for comments
    dislikes = models.PositiveIntegerField(default=0) #dislikes for comments

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return 'Comment by '+ str(self.name)

class PhotoContestSubmission(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    photo = models.ImageField(upload_to='contest_photos/')
    submission_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.submission_datetime}"