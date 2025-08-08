from types import NoneType
from django.db.models import F

from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.contrib.auth.models import User
from MainApp.models import Comment, Notification

import logging

logger = logging.getLogger(__name__)

# Сигналы
snippet_view = Signal()

@receiver(post_save, sender=User)
def send_message(sender, instance, created, **kwargs):
    if created:
        print(f"Пользователь {instance.username} зарегистрирован!!!")


@receiver(snippet_view, sender=None)
def add_views_count(sender, snippet, **kwargs):
    snippet.views_count = F('views_count') + 1
    snippet.save(update_fields=["views_count"])  # -> SET v_c = 11 | SET v_c =  v_c + 1
    snippet.refresh_from_db()


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.snippet.user and instance.author != instance.snippet.user:
        Notification.objects.create(
            recipient=instance.snippet.user,
            notification_type='comment',
            title=f'Новый комментарий к сниппету "{instance.snippet.name}"',
            message=f'Пользователь {instance.author.username} оставил комментарий: "{instance.text[:50]}{"..." if len(instance.text) > 50 else ""}"',
        )