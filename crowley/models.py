#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

class Crawler(models.Model):
    """Uma instância do robô que irá utilizar dados de usuário do Facebook
    para rastrear páginas ou executar buscas por eventos.

    :param name: O Nome
    :param token: O Token de usuário fornecido pelo Facebook
    :param active: Define se o Crawler está ativo
    :param created: Data de criação da instância
    :param last_modified: Data da última modificação da instância
    """

    name = models.CharField('Nome', max_length=255)
    token = models.CharField('Token', max_length=255)
    active = models.BooleanField('Ativo', default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    __repr__ = __str__


class Tag(models.Model):
    """Uma tag controla o processamento de eventos, permitindo ou negando o
    processamento de um evento de acordo com o conteúdo da tag.

    :param content: O conteúdo que deve ser observado no texto de um evento
    :param action: Ação a ser tomada: permitir ou negar a inclusão do evento
    :param active: Define se a tag está ativa
    :param created: Data de criação da instância
    :param last_modified: Data da última modificação da instância
    """
    TAG_ALLOW = 'A'
    TAG_DENY = 'D'
    ACTION_CHOICES = (
            (TAG_ALLOW, 'Permitir'),
            (TAG_DENY, 'Proibir'),
        )

    content = models.CharField('Conteúdo', max_length=255)
    action = models.CharField(
                'Ação',
                max_length=1,
                choices=ACTION_CHOICES,
                default=TAG_ALLOW
            )
    active = models.BooleanField('Ativa', default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    __repr__ = __str__
