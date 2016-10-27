# -*- coding: utf-8 -*-
'''
@author: Monica Mota
'''
from django.contrib.gis.db import models


class Logradouro(models.Model):
    """
        Classe de persistência das estações
    """

    TIPO = (
        ('mt', 'motorway'),
        ('tk', 'trunk'),
        ('pm', 'primary'),
        ('sc', 'secondary'),
        ('tt', 'tertiary'),
        ('rd', 'residential'),
        ('sv', 'service'),
        ('un', 'unclassified'),
    )
    # Informação
    nome = models.CharField(max_length=50, db_index=True)
    codigo = models.IntegerField(db_index=True)

    # Características
    tipo = models.CharField(max_length=4, choices=TIPO)
    maounica = models.BooleanField(db_index=True)
    sentido = models.CharField(max_length=2, null=True)

    # Localização
    geom = models.PolygonField(spatial_index=True)  # WGS84
    referencia = models.CharField(max_length=50, db_index=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return u"{0}".format(self.nome)

    class Meta:
        ordering = ['nome']
        verbose_name = u"Logradouro"
        verbose_name_plural = u"Logradouros"
        unique_together = ("nome", "maounica",)

class Cota(models.Model):
    """
    Cota de cheia das ruas.
    """

    logradouro = models.ForeignKey(Logradouro, db_index=True)
    cheia = models.DecimalField(max_digits=5, decimal_places=2, db_index=True)
    observacao = models.CharField(max_length=254, null=True)

    class Meta:
        ordering = ['cheia']
        verbose_name = u'Cota'
        verbose_name_plural = u'Cotas'

    def __unicode__(self):
        return u'{0}, {1} - Cota: {2}'.format(self.logradouro,
                                              self.logradouro.nome,
                                              self.cheia)
