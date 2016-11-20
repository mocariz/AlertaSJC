# -*- coding: utf-8 -*-

from AlertaSJC.geo.models import Cota
from AlertaSJC.dados.models.leituraSensor import LeituraSensor
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

class CotaSerializer(GeoFeatureModelSerializer):
    '''
    Serializer da Classe CurvaNivel
    '''

    geom = serializers.SerializerMethodField()
    css = serializers.SerializerMethodField()

    def get_geom(self, obj):
        return obj.logradouro.geom

    def get_css(self, obj):
        '''
        Define o css do nivel de alerta para o nivel do rio
        '''

        leitura = LeituraSensor.objects.filter(
            sensor__pk=2,
            leitura__estacao__id=11
        ).latest()
        return leitura.leitura.css_nivel


    class Meta:
        model = Cota
        geo_field = 'geom'
        fields = ('cheia', 'css',)
