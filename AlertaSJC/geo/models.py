# -*- coding: utf-8 -*-
'''
@author: Monica Mota
'''
from django.contrib.gis.db import models
from AlertaSJC.dados.models.leituraSensor import LeituraSensor

TIPO = (
    ('mt', 'motorway'),
    ('tk', 'trunk'),
    ('pm', 'primary'),
    ('sc', 'secondary'),
    ('tt', 'tertiary'),
    ('rd', 'residential'),
    ('sv', 'service'),
    ('ft', 'footway'),
    ('tr', 'track'),
    ('pd', 'pedestrian'),
    ('ph', 'path'),
    ('mtl', 'motorway_link'),
    ('pml', 'primary_link'),
    ('ttl', 'tertiary_link'),
    ('tkl', 'trunk_link'),
    ('scl', 'secondary_link'),
    ('ls', 'living_street'),
    ('cy', 'cycleway'),
    ('sp', 'steps'),
    ('ri', 'rail'),
    ('pi', 'pier'),
    ('un', 'unclassified'),
)


class Logradouro(models.Model):
    """
        Classe de persistência das estações
    """

    # Informação
    nome = models.CharField(max_length=150, db_index=True)
    codigo = models.IntegerField(db_index=True)

    # Características
    tipo = models.CharField(max_length=4, choices=TIPO)
    maounica = models.BooleanField(db_index=True)
    sentido = models.CharField(max_length=2, null=True)

    # Localização
    geom = models.LineStringField(spatial_index=True)  # WGS84
    referencia = models.CharField(max_length=50, db_index=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return u"{0}".format(self.nome)

    def get_center(self):
        center = self.geom.centroid
        return center.coords

    class Meta:
        ordering = ['nome']
        verbose_name = u"Logradouro"
        verbose_name_plural = u"Logradouros"
        unique_together = ("codigo", "nome",)

class Cota(models.Model):
    """
    Cota de cheia das ruas.
    """

    logradouro = models.ForeignKey(Logradouro, db_index=True)
    altitude = models.DecimalField(max_digits=5, decimal_places=2, db_index=True)
    observacao = models.CharField(max_length=254, null=True)
    cota = models.DecimalField(max_digits=5, decimal_places=2, db_index=True,
                               null=True)

    class Meta:
        ordering = ['cota']
        verbose_name = u'Cota'
        verbose_name_plural = u'Cotas'

    def __unicode__(self):
        return u'{0}, {1} - Cota: {2}'.format(self.logradouro,
                                              self.logradouro.nome,
                                              self.cota)


    def css_cota(self):
        css = ''
        leitura = LeituraSensor.objects.filter(
            sensor__pk=2,
            leitura__estacao__id=11
        ).latest()
        diferenca = float(self.cota) - leitura.valor


        if diferenca > 3.0 and diferenca < 5.0:
            css = "vigilancia"
        elif diferenca >= 2.0 and diferenca < 3.0:
            css = "atencao"
        elif diferenca >= 1 and diferenca < 2.0:
            css = "alerta"
        elif leitura.valor > self.cota:
            css = "prontidao"

        print css, diferenca

        return css
