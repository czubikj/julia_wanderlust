from model_bakery import baker
import pytest

import datetime as dt
from freezegun import freeze_time

from blog.models import Post

# Mark this test module as requiring the database
pytestmark = pytest.mark.django_db

def test_published_posts_only_returns_those_with_published_status():
    # Create a published Post by setting the status to "published"
    published = baker.make('blog.Post', status=Post.PUBLISHED)
    # Create a draft Post
    baker.make('blog.Post', status=Post.DRAFT)

    # We expect only the "published" object to be returned
    expected = [published]
    # Cast the result as a list so we can compare apples with apples!
    # Lists and querysets are of different types.
    result = list(Post.objects.published())

    assert result == expected

def test_draft_posts_only_returns_those_with_draft_status():
    # Create a published Post by setting the status to "published"
    draft = baker.make('blog.Post', status=Post.DRAFT)
    # Create a draft Post
    baker.make('blog.Post', status=Post.PUBLISHED)

    # We expect only the "published" object to be returned
    expected = [draft]
    # Cast the result as a list so we can compare apples with apples!
    # Lists and querysets are of different types.
    result = list(Post.objects.draft())

    assert result == expected

def test_publish_sets_status_to_published():
    post = baker.make('blog.Post', status=Post.DRAFT)
    post.publish()
    assert post.status == Post.PUBLISHED

@freeze_time(dt.datetime(2030, 6, 1, 12), tz_offset=0)  # Replaces now()
def test_publish_sets_published_to_current_datetime():
    # Create a new post, and ensure no published datetime is set
    post = baker.make('blog.Post', published=None)
    post.publish()

    # Set the timezone to UTC (to match tz_offset=0)
    assert post.published == dt.datetime(2030, 6, 1, 12, tzinfo=dt.timezone.utc)

def test_get_authors_returns_users_who_have_authored_a_post(django_user_model):
    # Create a user
    author = baker.make(django_user_model)
    # Create a post that is authored by the user
    baker.make('blog.Post', author=author)
    # Create another user – but this one won't have any posts
    baker.make(django_user_model)

    assert list(Post.objects.get_authors()) == [author]

def test_get_authors_returns_unique_users(django_user_model):
    # Create a user
    author = baker.make(django_user_model)
    # Create multiple posts. The _quantity argument can be used
    # to specify how many objects to create.
    baker.make('blog.Post', author=author, _quantity=3)

    assert list(Post.objects.get_authors()) == [author]
