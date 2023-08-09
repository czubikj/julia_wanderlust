from django.shortcuts import render
from . import models
from django.views import View
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from . import forms, models
from django.views.generic import DetailView, FormView, ListView
from django.urls import reverse_lazy
from django.contrib import messages


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

class ContextMixin:
    """
    Provides common context variables for blog views
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = models.Post.objects.published() \
            .get_authors() \
            .order_by('first_name')

        return context

class HomeView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        # Get the parent context
        context = super().get_context_data(**kwargs)

        latest_posts = models.Post.objects.published() \
            .order_by('-published')[:3]

        authors = models.Post.objects.published() \
            .get_authors() \
            .order_by('first_name')

        # Update the context with our context variables
        context.update({
            'authors': authors,
            'latest_posts': latest_posts
        })

        return context

class AboutView(TemplateView):
    template_name = 'blog/about.html'

class PostListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published().order_by('-published')

class PostDetailView(DetailView):
    model = models.Post

    def get_queryset(self):
        queryset = super().get_queryset().published()

        # If this is a `pk` lookup, use default queryset
        if 'pk' in self.kwargs:
            return queryset

        # Otherwise, filter on the published date
        return queryset.filter(
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        related_topics = post.topics.all()

        context['related_topics'] = related_topics
        return context

class TopicListView(ListView):
    model = models.Topic
    context_object_name = 'topics'
    queryset = models.Topic.objects.order_by('name')

class TopicDetailView(DetailView):
    model = models.Topic
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = self.get_object()

        related_posts = topic.blog_posts.filter(status='published').order_by('-published')
        context['related_posts'] = related_posts
        return context

    def get_absolute_url(self):
        return reverse(
            'topic-detail',
            kwargs={
                'slug': self.slug
            }
        )

def form_example(request):
    # Handle the POST
    if request.method == 'POST':
        # Pass the POST data into a new form instance for validation
        form = forms.ExampleSignupForm(request.POST)

        # If the form is valid, return a different template.
        if form.is_valid():
            # form.cleaned_data is a dict with valid form data
            cleaned_data = form.cleaned_data

            return render(
                request,
                'blog/form_example_success.html',
                context={'data': cleaned_data}
            )
    # If not a POST, return a blank form
    else:
        form = forms.ExampleSignupForm()

    # Return if either an invalid POST or a GET
    return render(request, 'blog/form_example.html', context={'form': form})

class FormViewExample(FormView):
    template_name = 'blog/form_example.html'
    form_class = forms.ExampleSignupForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Create a "success" message
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you for signing up!'
        )
        # Continue with default behaviour
        return super().form_valid(form)
def contest_form(request):
    if request.method == 'POST':
        contest_form = forms.PhotoForm(request.POST, request.FILES)
        if contest_form.is_valid():
            cleaned_data = contest_form.cleaned_data
            return render(
                request,
                'blog/photo_contest_success.html',
                context={'data': cleaned_data}
            )
    else:
        contest_form = forms.PhotoForm()
    return render(request, 'blog/photo_contest.html', context={'contest_form': contest_form})

class ContestFormView(FormView):
    template_name = 'blog/photo_contest.html'
    model = models.PhotoContestSubmission
    form_class = forms.PhotoForm
    success_url = reverse_lazy('home')
    fields = [
        'first_name',
        'last_name',
        'email',
        'photo',
    ]
    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        submission = models.PhotoContestSubmission.objects.create(
            first_name=cleaned_data['first_name'],
            last_name=cleaned_data['last_name'],
            email=cleaned_data['email'],
            photo=cleaned_data['photo'],)
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you! Your photo submission has been received!'
        )
        return super().form_valid(form)


def terms_and_conditions(request):
   return render(request, 'blog/terms_and_conditions.html')