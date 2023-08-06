from . import models

def base_context(request):
    authors = models.Post.objects.published() \
        .get_authors() \
        .order_by('first_name')
    pop_topics = models.Post.objects.get_popular_topics().distinct().order_by('-num_posts')


    return {
        'authors': authors,
        'pop_topics': pop_topics,
    }