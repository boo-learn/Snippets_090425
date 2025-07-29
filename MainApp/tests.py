import pytest
from django.test import TestCase
from .models import Snippet
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestSnippetModel:
    def test_create_snippet(self):
        Snippet.objects.create(
            name="Test Snippet",
            lang="python",
            code="print('Hello, World!')",
            public=True
        )

        snippet = Snippet.objects.get(id=1)

        assert snippet.name == "Test Snippet"
        assert snippet.lang == "python"
        assert snippet.views_count == 0
        assert snippet.public

    def test_user_create_snippet(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )

        snippet = Snippet.objects.create(
            name="User Snippet",
            lang="javascript",
            code="console.log('Hello');",
            user=user,
            public=False
        )

        assert snippet.user.username == "testuser"
        assert not snippet.public
        assert snippet.code == "console.log('Hello');"


# Преимущества:
# 1. Быстрая проверка на работоспособность и Проверка корректности логики кода
# 2. Убедиться в работоспособности старой логики, при добавлении новых фич
# 3. проверка перед деплоем
# 4. Проверка при рефакторинге
# 5. Обеспечение высокого качества кода