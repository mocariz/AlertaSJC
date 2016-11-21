# -*- coding: utf-8 -*-

from AlertaSJC.estacoes.models import Estacao
from AlertaSJC.dados.models.leitura import Leitura
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class EstacaoSerializer(GeoFeatureModelSerializer):
    css = serializers.SerializerMethodField()

    def get_css(self, obj):
        '''
        Define o css da estacao de acordo com a leitura de 24h
        '''
        leitura = obj.leitura_set.latest()
        return leitura.leiturachuva.css_chuva

    class Meta:
        model = Estacao
        geo_field = 'geom'
        fields = ('nome', 'css',)
