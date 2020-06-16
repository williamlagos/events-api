import facebook
from datetime import datetime
from pytz import timezone
from dateutil import parser
from crowley.models import Tag
from backend.models import Event, Owner


FACEBOOK_EVENT_FIELDS = 'id,name,start_time,end_time,place,description,' \
    'owner{id,name,location{city,state}},is_page_owned,attending_count,' \
    'interested_count,cover'


def is_event_allowed(fb_event_data):
    """Verifica se um evento pode ser processado.

    Checa se ainda não ocorreu e se está livre de palavras rejeitadas.
    """
    # Computa a hora atual de Brasilia
    br_tz = timezone('America/Sao_Paulo')
    now = datetime.now(br_tz)

    # Calcula a diferença entre as datas e verifica se o evento é passado
    start_time = parser.parse(fb_event_data['start_time'])
    end_time = start_time
    if 'end_time' in fb_event_data:
        end_time = parser.parse(fb_event_data['end_time'])
    datetime_diff = end_time - now
    if datetime_diff.total_seconds() < 0:
        return False

    # Verifica se o corpo do evento possui palavras rejeitadas
    event_body = fb_event_data['name']
    if 'description' in fb_event_data:
        event_body += fb_event_data['description']
    event_body = event_body.lower()

    denied_tags = Tag.objects.filter(active=True, action=Tag.TAG_DENY)
    for tag in denied_tags:
        content = tag.content.lower()
        if content in event_body:
            return False

    return True


def find_or_create_owner(fb_event_data, data_origin):
    """Localiza ou insere um Owner com os dados de evento do Facebook."""
    owner_type = Owner.OWNER_TYPE_USER
    if 'is_page_owned' in fb_event_data:
        if fb_event_data['is_page_owned']:
            owner_type = Owner.OWNER_TYPE_PAGE
        else:
            owner_type = Owner.OWNER_TYPE_USER

    try:
        location_city = fb_event_data['owner']['location']['city']
    except:
        location_city = None

    try:
        location_state = fb_event_data['owner']['location']['state']
    except:
        location_state = None

    owner_data = {
        'owner_type': owner_type,
        'name': fb_event_data['owner']['name'],
        'origin': data_origin,
        'location_city': location_city,
        'location_state': location_state,
        'active': True
    }

    owner, created = Owner.objects.get_or_create(
        external_id=fb_event_data['owner']['id'],
        defaults=owner_data
    )

    if created:
        print('Created Owner ', owner.id, owner.name)
    else:
        # Atualiza os dados do owner, mas mantém os campos de origem e ativo
        # de acordo com o que já foi moderado.
        owner_data['origin'] = owner.origin
        owner_data['active'] = owner.active
        for key, value in owner_data.items():
            setattr(owner, key, value)
        owner.save()
        print('Updated owner', owner.id)

    return owner


def upsert_event(fb_event_data, data_origin):
    """Insere ou atualiza um Event com dados de evento do Facebook."""
    owner = find_or_create_owner(fb_event_data, data_origin)

    start_time = parser.parse(fb_event_data['start_time'])
    end_time = None
    if 'end_time' in fb_event_data:
        end_time = parser.parse(fb_event_data['end_time'])

    description = None
    if 'description' in fb_event_data:
        description = fb_event_data['description']

    try:
        place_latitude = fb_event_data['place']['location']['latitude']
    except:
        place_latitude = None

    try:
        place_longitude = fb_event_data['place']['location']['longitude']
    except:
        place_longitude = None

    try:
        place_city = fb_event_data['place']['location']['city']
    except:
        place_city = None

    try:
        place_state = fb_event_data['place']['location']['state']
    except:
        place_state = None

    try:
        place_country = fb_event_data['place']['location']['country']
    except:
        place_country = None

    try:
        place_name = fb_event_data['place']['name']
    except:
        place_name = None

    try:
        place_address = fb_event_data['place']['location']['street']
    except:
        place_address = None

    try:
        cover_image_url = fb_event_data['cover']['source']
    except:
        cover_image_url = None

    event_data = {
        'owner': owner,
        'external_id': fb_event_data['id'],
        'name': fb_event_data['name'],
        'description': description,
        'start_time': start_time,
        'end_time': end_time,
        'place_latitude': place_latitude,
        'place_longitude': place_longitude,
        'place_city': place_city,
        'place_state': place_state,
        'place_country': place_country,
        'place_name': place_name,
        'place_address': place_address,
        'status': Event.STATUS_PENDING,
        'origin': data_origin,
        'is_page_owned': fb_event_data['is_page_owned'],
        'attending_count': fb_event_data['attending_count'],
        'interested_count': fb_event_data['interested_count'],
        'cover_image_url': cover_image_url,
        'active': True
    }

    # Localiza ou cria o evento
    event, created = Event.objects.get_or_create(
        external_id=fb_event_data['id'],
        defaults=event_data
    )

    if created:
        print('Created event', event.id)
    else:
        # Atualiza os dados do evento, mas mantém os campos de status e ativo
        # de acordo com o que já foi moderado.
        event_data['status'] = event.status
        event_data['origin'] = event.origin
        event_data['active'] = event.active
        for key, value in event_data.items():
            setattr(event, key, value)
        event.save()
        print('Updated event', event.id)

    return event


def process_fb_event_list(fb_event_list, data_origin):
    """Processa uma lista de eventos do Facebook.

    Faz a triagem de cada evento da lista através das palavras recusadas e
    insere ou atualiza os eventos e seus organizadores.
    """
    for event in fb_event_list:
        if (is_event_allowed(event)):
            upsert_event(event, data_origin)


def scrape_fb_page(fb_page_id, fb_access_token):
    """Busca os eventos de uma página do Facebook.

    Faz a triagem por palavras recusadas e insere ou atualiza os eventos e
    organizadores no backend.
    """
    print('Crawling on page', fb_page_id)

    try:
        graph = facebook.GraphAPI(access_token=fb_access_token, version='2.7')
        page_events = graph.get_connections(
            id=fb_page_id,
            connection_name='events',
            fields=FACEBOOK_EVENT_FIELDS
        )
    except facebook.GraphAPIError as graph_error:
        print('Error while crawling on page', fb_page_id,
              ':', graph_error.message)
        return

    process_fb_event_list(page_events['data'], Event.ORIGIN_MR_CROWLEY)

    print('Done with page', fb_page_id)
