# -*- coding: utf-8 -*-
'''
@author: Monica Mota
'''

import json
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from django.contrib.gis.db import models
from django.utils import timezone

from TrajetoSecoSJC.dados.models.leitura import Leitura
from TrajetoSecoSJC.dados.models.leituraChuva import LeituraChuva
from TrajetoSecoSJC.dados.models.leituraSensor import LeituraSensor

logger = logging.getLogger(__name__)
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/28.0.1500.71 Safari/537.36'

TIPO_ESTACAO = (
    ('plv', u'Pluviométrica'),    # Chuva
    ('lnm', u'Linimétrica'),      # Nivel
)

TIPODADOS = (
    ('B', 'Byte: sem Sinal'),
    ('b', 'Byte: com Sinal'),
    ('>H', 'Word: sem sinal ( 2 bytes)'),
    ('<H', 'Word: sem sinal ( 2 bytes) Big-endian'),
    ('>h', 'Word: com sinal ( 2 bytes)'),
    ('bbb', '12bits (3 bytes)'),
    ('>I', 'Inteiro: sem sinal ( 4 bytes)'),
    ('<I', 'Inteiro: sem sinal ( 4 bytes) Big-endian'),
    ('>i', 'Inteiro: com sinal ( 4 bytes)'),
    ('>f', 'Float ( 4 bytes)')
)

TIPO_SENSOR = (
    ('niv', u'Nível'),
    ('vrnce', u'Variance'),
)


class Estacao(models.Model):
    """
        Classe de persistência das estações
    """

    # Informação
    nome = models.CharField(max_length=50, db_index=True)
    codigo = models.CharField(max_length=50, db_index=True)
    descricao = models.TextField(blank=True, null=True)

    # Características
    tipo = models.CharField(max_length=4, choices=TIPO_ESTACAO)
    sensores = models.ManyToManyField('Sensor', through='EstacaoSensor')
    fonte = models.ForeignKey('Fonte')

    # Localização
    endereco = models.CharField(max_length=255, null=False, blank=False)
    numero = models.SmallIntegerField(blank=True, null=True)
    geom = models.PointField(spatial_index=True)  # WGS84

    objects = models.GeoManager()

    def __unicode__(self):
        return u"{0} - {1}".format(self.nome, self.fonte)

    @property
    def chuva(self):
        try:
            leitura = self.leitura_set.latest()
            return leitura.leiturachuva.json_leiturachuva()
        except Leitura.DoesNotExist:
            return None

    def estacaoSensor(self):
        return EstacaoSensor.objects.filter(
            estacao=self,
            ativo=True,
            sensor__leituraSensor=True
        )

    def createLeitura(self, horaLeitura, now):
        # cria a leitura
        return Leitura.objects.get_or_create(
            estacao=self,
            horaLeitura=horaLeitura,
            defaults=dict(
                fonte=self.fonte,
                horaRecebida=now,
                horaEnviada=now
            ))

    class Meta:
        ordering = ['nome']
        verbose_name = u"Estação"
        verbose_name_plural = u"Estações"
        unique_together = ("codigo", "fonte",)


class Sensor(models.Model):
    """
    Classe de persistência dos sensores
    """

    # Informação
    nome = models.CharField(max_length=50, db_index=True)
    tipo = models.CharField(max_length=5, choices=TIPO_SENSOR)

    def __unicode__(self):
        return u'{0}'.format(self.nome)

    class Meta:
        verbose_name = u"Sensor"
        verbose_name_plural = u"Sensores"
        ordering = ['nome']


class EstacaoSensor(models.Model):
    """
    Ponte Many-to-Many entre a estações e os sensores
    """

    estacao = models.ForeignKey(Estacao)
    sensor = models.ForeignKey(Sensor)

    class Meta:
        unique_together = ("estacao", "sensor")

    def __unicode__(self):
        return u"{0} - {1}".format(self.estacao, self.sensor)


class Fonte(models.Model):
    """
    Classe de persistencia das Fontes
    """

    nome = models.CharField(max_length=20, unique=True)
    site = models.CharField(max_length=254)
    url = models.CharField(max_length=254, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.nome)

    class Meta:
        ordering = ['nome']

    def fonte_CEMADEN(self):
        '''
        retorna um dict com os dados das estacões pegos no cemaden para Sjc
        '''
        now = timezone.now()
        utc_tz = timezone.utc
        resultado = {}
        for estado in self.estados():
            # cria o caminho
            path = self.url.format(estado)
            response = requests.get(path, timeout=240, headers={
                'User-Agent': USER_AGENT})

            if response.status_code == 200:
                data = json.loads(response.text)
                for d in data['cemaden']:
                    try:
                        estacao = Estacao.objects.get(
                            codigo=d['codestacao'],
                            fonte=self,
                            ativa=True,
                            source='cmden'
                        )
                        if estacao not in resultado:
                            resultado[estacao] = {}

                        try:
                            d['dataHora'] = d['dataHora'].split('.', 1)[0]
                            horaLeitura = datetime.strptime(
                                d['dataHora'], '%Y-%m-%d %H:%M:%S')
                            horaLeitura = horaLeitura.replace(tzinfo=utc_tz) \
                                                     .astimezone(utc_tz)

                            resultado[estacao][horaLeitura] = float(d['chuva'])
                        except TypeError as e:
                            logger.debug(str(e))
                    except Estacao.DoesNotExist:
                        pass

        for estacao, dados in resultado.iteritems():
            for horaLeitura, valor in dados.iteritems():
                if horaLeitura.minute in (0, 30):
                    m10 = timedelta(minutes=10)
                    valor += resultado[estacao].get(horaLeitura - m10, 0)
                    valor += resultado[estacao].get(horaLeitura - m10 - m10, 0)

                    # cria a leitura
                    leitura, created = estacao.createLeitura(horaLeitura, now)

                    if created is False:
                        continue

                    # cria leitura sensor
                    vrnce = estacao.sensores.get(tipo='vrnce')
                    leitura.createLeituraSensor(vrnce, valor)
                    # cria a leitura chuva
                    leitura.atualiza_or_create_leituraChuva()
