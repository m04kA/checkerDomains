import datetime
import typing
import logging

import pytz
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from checkerApp.models import UserDomainsHistory
from checkerApp.serializers import DomainsHistorySerializer
from checkerApp.src import linksParser
from checkerApp import serializers
from checkerApp.tasks import add_data_in_database

logger = logging.getLogger(__name__)


# Create your views here.
class LinksView(APIView):
    def post(self, request: Request):
        user_id = request.META.get('HTTP_X_USER_ID')
        if not user_id:
            return Response(
                {'message': 'Request has not X-User-Id'},
                status=403
            )

        serializer = serializers.VisitedLinksSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        links = serializer.validated_data.get('links')
        try:
            domains = linksParser.get_unique_domains_from_links(links)
        except Exception as err:
            logger.error('Error while getting domains; links: %s; Error: %s', links, err)
            return Response({'message': 'Internal error', 'code': 'internal_error'}, status=500)

        now_timestamp_seconds = int((timezone.now() - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds())
        add_data_in_database.delay(
            user_id,
            domains,
            now_timestamp_seconds
        )

        return Response({'status': 'Ok'})

    @staticmethod
    def _generate_user_history_rows(user_id: str, domains: typing.List[str], now: int):
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

            UserDomainsHistory.objects.create(**serializer_row_database.validated_data)


class DomainsView(APIView):
    def get(self, request: Request):
        user_id = request.META.get('HTTP_X_USER_ID')
        if not user_id:
            return Response(
                {'message': 'Request has not X-User-Id'},
                status=403
            )

        serializer = serializers.ViewPeriodSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        start_period = serializer.validated_data.get('start')
        finish_period = serializer.validated_data.get('finish')
        try:
            user_domains_in_range = self._get_user_domains_in_range(
                user_id=user_id,
                start_period=start_period,
                finish_period=finish_period
            )
        except Exception as exc:
            logger.error(
                'Error while get history data; user_id: %s; '
                'start_period: %s; finish_period: %s; Error: %s',
                user_id,
                start_period,
                finish_period,
                exc
            )
            return Response({'message': 'Internal error', 'code': 'internal_error'}, status=500)

        return Response(user_domains_in_range)

    @staticmethod
    def _get_user_domains_in_range(user_id: str, start_period: int, finish_period: int) -> dict:
        user_domains_in_range = UserDomainsHistory.objects.filter(
            user_id=user_id, created_at__gte=start_period, created_at__lt=finish_period
        )

        user_history = DomainsHistorySerializer(user_domains_in_range, many=True)

        user_domains_in_range = {'domains': set(), 'status': 'Ok'}
        for el in list(user_history.data):
            user_domains_in_range['domains'].add(el.get('domain'))

        return user_domains_in_range
