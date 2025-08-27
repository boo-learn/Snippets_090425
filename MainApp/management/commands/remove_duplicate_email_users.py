from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db.models import Count, Q


class Command(BaseCommand):
    help = 'Удаляет пользователей с одинаковыми email'

    def handle(self, *args, **options):
        duplicates_email = User.objects.values('email').annotate(count=Count('email')).filter(count__gt=1)
        user_count = 0
        # print(duplicates_email)
        for data in duplicates_email:
            delete_users = User.objects.filter(email=data['email']).order_by('date_joined')[1:]
            user_count += data['count'] - 1
            for user in delete_users:
                user.delete()

        print(f"Удалено {user_count} пользователей")
