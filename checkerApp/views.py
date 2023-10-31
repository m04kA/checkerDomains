from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from checkerApp.src import linksParser
from checkerApp import serializers
import logging

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
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=400
            )
        links = serializer.validated_data.get('links')
        try:
            domains = linksParser.get_unique_domains_from_links(links)
        except Exception as err:
            logger.error('Error while getting domains; links: %s; Error: %s', links, err)
            return Response({'message': 'Internal error', 'code': 'internal_error'}, status=500)
        return Response(domains)


class DomainsView(APIView):
    def get(self, request: Request):
        user_id = request.META.get('HTTP_X_USER_ID')
        if not user_id:
            return Response(
                {'message': 'Request has not X-User-Id'},
                status=403
            )
        serializer = serializers.ViewPeriodSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=400
            )

        return Response(serializer.data)
