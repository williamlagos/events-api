from backend.models import Owner, Event
from backend.serializers import OwnerSerializer, EventSerializer
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseBadRequest
from backend.geolocation import GeoLocation
from datetime import datetime, timedelta, time
from dateutil import parser
from pytz import timezone
from django.views.decorators.http import require_http_methods
from crowley.services import process_fb_event_list
import json


def index(request):
    return HttpResponse('<html><body><iframe width="640" height="480" '
                        'src="https://www.youtube.com/embed/FWO5Ai_a80M?'
                        'autoplay=1" frameborder="0" allowfullscreen>'
                        '</iframe></body></html>')


class OwnerList(generics.ListCreateAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    serializer_class = OwnerSerializer

    def get_queryset(self):
        queryset = Owner.objects.all()
        external_id = self.request.query_params.get('external_id', None)
        if external_id is not None:
            queryset = queryset.filter(external_id=external_id)

        return queryset


class OwnerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)

    lookup_field = 'id'
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class EventList(generics.ListCreateAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        external_id = self.request.query_params.get('external_id', None)
        if external_id is not None:
            queryset = queryset.filter(external_id=external_id)
        owner = self.request.query_params.get('owner', None)
        if owner is not None:
            queryset = queryset.filter(owner__id=owner)
        status = self.request.query_params.get('status', None)
        if status is not None:
            queryset = queryset.filter(status=status)
        city_name = self.request.query_params.get('city_name', None)
        if city_name is not None:
            queryset = queryset.filter(place_city=city_name)
        start_after = self.request.query_params.get('start_after', None)
        if start_after is not None:
            queryset = queryset.filter(start_time__gt=start_after)
        return queryset


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    lookup_field = 'id'
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class CityList(APIView):
    permission_classes = (permissions.DjangoModelPermissions,)

    # Exclui eventos inativos e com cidades nulas ou vazias
    queryset = Event.objects.exclude(active=False).\
        exclude(place_city__isnull=True).\
        exclude(place_city='')

    # Extrai os nomes de cidades distintos e ordenados
    queryset = queryset.values_list('place_city', flat=True).\
        order_by('place_city').distinct()

    def get(self, request, format=None):
        return Response(self.queryset.all())


class NearEventList(generics.ListCreateAPIView):
    """Lista de eventos próximos."""

    """Hora a ser usada na lógica de exibição de eventos anteriores."""
    GOLDEN_HOUR = 6

    """A zona horária usada ao computar as datas."""
    TIME_ZONE = timezone('America/Sao_Paulo')

    """Instância de `time` para testar a inclusão de eventos de ontem."""
    TIME_CHECK = time(hour=GOLDEN_HOUR, minute=0, tzinfo=TIME_ZONE)

    """Quantidade de tempo a ser subtraído da data de hoje."""
    TIME_SHIFT = timedelta(hours=GOLDEN_HOUR)

    permission_classes = (permissions.DjangoModelPermissions,)
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.filter(active=True).filter(status='A')

        client_datetime = self.request.query_params.get('cli_dt', None)
        if client_datetime is not None:

            # Se for antes das 6:00, retorna eventos que estariam ocorrendo
            # a partir das 18:00 de ontem. Do contrário, considera apenas os
            # eventos do dia de hoje.
            beginning = time(0, 0, tzinfo=self.TIME_ZONE)
            client_now = parser.parse(client_datetime)
            running_datetime = datetime.combine(date=client_now.date(),
                                                time=beginning)
            if client_now.time() < self.TIME_CHECK:
                running_datetime -= self.TIME_SHIFT

            # Exclui eventos com data de término anterior
            queryset = queryset.exclude(end_time__lt=running_datetime)

            # Exclui eventos sem data de término e com data de inicio anterior
            queryset = queryset.exclude(end_time__isnull=True,
                                        start_time__lt=running_datetime)

        city_name = self.request.query_params.get('city_name', None)
        if city_name is not None:
            queryset = queryset.filter(place_city__iexact=city_name)

        lat = self.request.query_params.get('latitude', None)
        lon = self.request.query_params.get('longitude', None)
        dist = self.request.query_params.get('distance', None)

        if (lat is not None and
                lon is not None and
                dist is not None):
            location = GeoLocation.from_degrees(float(lat), float(lon))
            SW_location, NE_location = location.bounding_locations(float(dist))

            longitude_limits = (SW_location.deg_lon, NE_location.deg_lon)
            latitude_limits = (SW_location.deg_lat, NE_location.deg_lat)
            queryset = queryset.filter(place_longitude__range=longitude_limits,
                                       place_latitude__range=latitude_limits)

        return queryset


@require_http_methods(["POST"])
def external_events_handler(request):
    print('handling events')

    body_unicode = request.body.decode('utf-8')
    body_unicode = body_unicode.replace('\\r', '')

    body = json.loads(body_unicode)
    data = body['data']

    try:
        process_fb_event_list(data, Event.ORIGIN_USER)
        response = HttpResponse('OK')
    except Exception as ex:
        print(ex.__class__.__name__, ':', ex.args[0])
        response = HttpResponseBadRequest('Bad request')

    return response
