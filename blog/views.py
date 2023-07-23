from django.shortcuts import render
from . import models

# Create your views here.
def home(request):
    """
    The Blog homepage
    """
    # get last 3 posts
    latest_posts = models.Post.objects.published().order_by('-published')[:3]
    authors = models.Post.objects.get_authors()
    # retrieve topics with annotated num_posts
    topics = models.Post.objects.get_topics()
    # retrieve the top 10 posts, popularity determined by the number of comments
    top_posts = models.Post.objects.post_popularity().order_by('-popularity')[:10]
    # retrieve the topics of the top 10 posts
    related_topics = top_posts.get_related_topics()
    # retrieve the topics for all the posts, annotated with number of posts, with annotations limited to top 10 posts
    pop_topics = models.Post.objects.get_popular_topics().distinct().order_by('-num_posts')


    context = {
        'authors': authors,
        'latest_posts': latest_posts,
        'topics': topics,
        'top_posts': top_posts,
        'related_topics': related_topics,
        'pop_topics': pop_topics,
    }

    return render(request, 'blog/home.html', context)
