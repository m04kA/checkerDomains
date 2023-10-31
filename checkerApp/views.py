from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from checkerApp.src import linksParser
from checkerApp import serializers


# Create your views here.
class DomainsView(APIView):
    def post(self, request: Request):
        serializer = serializers.VisitedLinksSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={
                'message': f'Serialize request error; Error: {serializer.errors};',
                'code': 'wrong_request'},
                status=400
            )
        links = serializer.validated_data.get('links')
        try:
            domains = linksParser.get_unique_domains_from_links(links)
        except Exception as err:
            print('Error while getting domains; links: {}; Error: {}'.format(links, err))
            return Response({'message': 'Internal error', 'code': 'internal_error'}, status=500)
        return Response(domains)
