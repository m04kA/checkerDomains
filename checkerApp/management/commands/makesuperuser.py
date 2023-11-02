import os
import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


User = get_user_model()

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_NAME', default='admin')
        email = os.environ.get('ADMIN_EMAIL', default='admin@example.com')
        password = os.environ.get('ADMIN_PASS', default='password')
        try:
            user = None
            if not User.objects.filter(username=username).exists() and not User.objects.filter(
                    is_superuser=True).exists():
                logger.info('Admin user not found, creating one')

                user = User.objects.create_superuser(username, email, password)
                logger.info(f'A superuser "{username}" was created with email "{email}" ')

            else:
                logger.info('Аdmin user found by. Skipping super user creation')
        except Exception as e:
            logger.error(f'There was an error: {e}')
