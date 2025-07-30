import pytest
from .views import index_page, add_snippet_page, snippets_page, snippet_detail
from django.urls import reverse
from django.test import Client
from django.test import RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from .models import Snippet


class TestIndexPage:
    def test_index(self):
        client = Client()
        response = client.get(reverse('home'))

        assert response.status_code == 200
        assert 'Добро пожаловать' in response.content.decode()
        assert response.context.get('pagename') == 'PythonBin'


@pytest.mark.django_db
class TestAddSnippetPage:
    def setup_method(self):
        self.factory = RequestFactory()

    def test_gest_user(self):
        request = self.factory.get(reverse('snippet-add'))
        request.user = AnonymousUser()
        response = add_snippet_page(request)

        assert response.status_code == 302

    def test_auth_user(self):
        request = self.factory.get(reverse('snippet-add'))
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        request.user = user
        response = add_snippet_page(request)

        assert response.status_code == 200

    def test_post_form_data(self):
        form_data = {
            "name": "Test form snippet",
            "lang": "python",
            "code": "simple py code",
            "public": True,
        }
        user = User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
            password="testpass123"
        )
        request = self.factory.post(reverse('snippet-add'), form_data)
        request.user = user
        response = add_snippet_page(request)

        snippet = Snippet.objects.get(id=1)

        assert response.status_code == 302
        assert snippet.name == form_data["name"]
        assert snippet.lang == form_data["lang"]
        assert snippet.public == form_data["public"]


