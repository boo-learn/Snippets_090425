import pytest
from .models import Tag, Snippet, Comment
from .factories import TagFactory, SnippetFactory, CommentFactory


# Задание-1



@pytest.mark.django_db
def test_create_tags(tag_factory):
    # Создаст три тега, с указанными именами
    tags = tag_factory(names=["js", "basic", "oop"])

    assert Tag.objects.count() == 3

# Задание-2
@pytest.fixture
def snippet():
    return SnippetFactory()


@pytest.fixture
def comment_factory():
    def _create_commenys_to_snippet(snippet, n):
        return CommentFactory.create_batch(n, snippet=snippet)
    return _create_commenys_to_snippet


@pytest.mark.django_db
def test_create_comments(snippet, comment_factory):
    comment_factory(snippet=snippet, n=6)

    assert Comment.objects.count() == 6
    for comment in Comment.objects.all():
        assert comment.snippet == snippet