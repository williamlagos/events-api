from django.db import models


class Owner(models.Model):
    """Uma entidade responsável por eventos.

    Os owners podem ter sido importado de uma fonte externa, como uma página
    do Facebook.

    Atributos
    ===========
    external_id: O identificador único externo (do Facebook)
    name: O nome da página ou usuário
    owner_type: Tipo de Owner
        - U: Usuário
        - P: Página
    origin: A origem dos dados
        - L: Robô PHP legado
        - C: Mr. Crowley
        - U: Usuário
    location_city: Cidade
    location_state: Estado
    notes: Observações sobre este Owner
    active: Define se o Owner está ativo
    created: Data de criação da instância
    last_modified: Data da última modificação da instância
    """

    OWNER_TYPE_USER = 'U'
    OWNER_TYPE_PAGE = 'P'
    OWNER_TYPE_FIELD_CHOICES = (
        (OWNER_TYPE_USER, 'Usuário'),
        (OWNER_TYPE_PAGE, 'Página'),
    )

    ORIGIN_LEGACY = 'L'
    ORIGIN_MR_CROWLEY = 'C'
    ORIGIN_USER = 'U'
    ORIGIN_FIELD_CHOICES = (
        (ORIGIN_LEGACY, 'Robô PHP legado'),
        (ORIGIN_MR_CROWLEY, 'Mr. Crowley'),
        (ORIGIN_USER, 'Usuário'),
    )

    external_id = models.CharField(
        'ID Externo',
        unique=True,
        max_length=50
    )
    name = models.CharField('Nome', max_length=255)
    owner_type = models.CharField(
        'Tipo',
        max_length=1,
        choices=OWNER_TYPE_FIELD_CHOICES,
        default=OWNER_TYPE_USER
    )
    origin = models.CharField(
        'Origem de dados',
        max_length=1,
        choices=ORIGIN_FIELD_CHOICES,
        default=ORIGIN_LEGACY
    )
    location_city = models.CharField(
        'Cidade',
        blank=True,
        null=True,
        max_length=50)
    location_state = models.CharField(
        'Estado',
        blank=True,
        null=True,
        max_length=20)
    notes = models.CharField(
        'Notas',
        blank=True,
        null=True,
        max_length=50)
    active = models.BooleanField('Ativo', default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Owner object with id {}>'.format(self.id)


class Event(models.Model):
    """Classe que representa um evento, como um baile.

    Este evento pode ter sido importado de uma fonte externa, como um evento do
    Facebook.

    Atributos
    ===========
    owner: O responsável por este evento
    external_id: O identificador único externo (do Facebook)
    name: Nome
    description: Descrição detalhada
    start_time: Data/hora de início
    end_time: Data/hora do término
    place_latitude: A latitude do local
    place_longitude: A longitude do local
    place_city: A cidade do local
    place_state: O estado do local
    place_country: O estado do local
    place_name: Nome do local
    place_address: O endereço do local
    status: O estado de moderação
        - P: Pendente
        - A: Aprovado
        - D: Rejeitado
    origin: A origem dos dados
        - L: Robô PHP legado
        - C: Mr. Crowley
        - U: Usuário
    is_page_owned: Indica se o evento é organizado por uma página
    attending_count: Número de pessoas que confirmaram presença
    interested_count: Quantidade de pessoas que se interessaram
    cover_image_url: URL da imagem de capa do evento
    active: Define se a instância está ativa
    created: Data de criação da instância
    last_modified: Data da última modificação da instância
    """

    STATUS_PENDING = 'P'
    STATUS_APPROVED = 'A'
    STATUS_DENIED = 'D'
    STATUS_FIELD_CHOICES = (
        (STATUS_PENDING, 'Moderação pendente'),
        (STATUS_APPROVED, 'Aprovado'),
        (STATUS_DENIED, 'Rejeitado'),
    )

    ORIGIN_LEGACY = 'L'
    ORIGIN_MR_CROWLEY = 'C'
    ORIGIN_USER = 'U'
    ORIGIN_FIELD_CHOICES = (
        (ORIGIN_LEGACY, 'Robô PHP legado'),
        (ORIGIN_MR_CROWLEY, 'Mr. Crowley'),
        (ORIGIN_USER, 'Usuário'),
    )

    owner = models.ForeignKey(
        'Owner',
        on_delete=models.PROTECT,
    )

    external_id = models.CharField('ID Externo', unique=True, max_length=50)
    name = models.CharField('Nome', max_length=255)
    description = models.TextField('Descrição', blank=True, null=True,
                                   default='')
    start_time = models.DateTimeField('Início')
    end_time = models.DateTimeField('Término', blank=True, null=True,
                                    default=None)

    place_latitude = models.DecimalField('Latitude', blank=True, null=True,
                                         default=None, max_digits=17,
                                         decimal_places=15)
    place_longitude = models.DecimalField('Longitude', blank=True, null=True,
                                          default=None, max_digits=17,
                                          decimal_places=15)
    place_city = models.CharField('Cidade', blank=True, null=True,
                                  max_length=50, default='')
    place_state = models.CharField('Estado', blank=True, null=True,
                                   max_length=20, default='')
    place_country = models.CharField('País', blank=True, null=True,
                                     max_length=50, default='')
    place_name = models.CharField('Local', blank=True, null=True,
                                  max_length=50, default='')
    place_address = models.CharField('Endereço', blank=True, null=True,
                                     max_length=50, default='')

    status = models.CharField('Moderação',
                              max_length=1,
                              choices=STATUS_FIELD_CHOICES,
                              default=STATUS_PENDING)
    origin = models.CharField('Origem de dados',
                              max_length=1,
                              choices=ORIGIN_FIELD_CHOICES,
                              default=ORIGIN_LEGACY)
    # TODO: Este campo é redundante com Owner.owner_type e será removido
    is_page_owned = models.BooleanField('Criado por Página', default=False)
    attending_count = models.IntegerField('Confirmados', blank=True, null=True,
                                          default=None)
    interested_count = models.IntegerField('Interessados', blank=True,
                                           null=True, default=None)
    cover_image_url = models.URLField('URL da imagem de capa', max_length=1024,
                                      blank=True, null=True, default='')
    active = models.BooleanField('Ativo', default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Event object with id {}>'.format(self.id)

    class Meta:
        ordering = ['start_time', 'name']
