import logging
import typing

from checkerApp.models import UserDomainsHistory
from checkerApp.serializers import DomainsHistorySerializer
from checkerDomains.celery import app

logger = logging.getLogger(__name__)


# тут нужны ретраи
@app.task
def add_data_in_database(user_id: str, domains: typing.List[str], now: int):
    logger.info('Start task for load data user_id: %s', user_id)

    for domain in domains:
        data = {
            'user_id': user_id,
            'domain': domain,
            'created_at': now
        }
        serializer_row_database = DomainsHistorySerializer(data=data)

        if not serializer_row_database.is_valid():
            logger.info(
                'Error during saving data; user_id: %s; domain: %s; created_at: %s; err: %s',
                user_id,
                domain,
                now,
                serializer_row_database.errors
            )
            continue
        # что нужно было сделать
        '''
        1. пытаешься добавить запись в базу
        2. если получилось, то все круто, продолжаешь
        3. если упал с ошибкой DuplicateError, значит ты уже записывал инфу о связке пользователь - время - домен, такую ошибку мы просто игнорируем
        4. остальные ошибки не игнорируем, падаем
        '''
        try:
            UserDomainsHistory.objects.create(**serializer_row_database.validated_data)
        except Exception as exc:  # too common
            logger.error('Error while save history data; user_id: %s; Error: %s', user_id, exc)
            raise exc
    logger.info('Finish task for load data user_id: %s', user_id)
