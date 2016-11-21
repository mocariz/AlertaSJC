# -*- coding: utf-8 -*-

from AlertaSJC.geo.models import Cota, Logradouro
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class LogradouroSerializer(GeoFeatureModelSerializer):
    css = serializers.SerializerMethodField()

    def get_css(self, obj):
        '''
        Define o css do nivel de alerta para o nivel do rio
        '''
        css = ''
        try:
            cota = Cota.objects.get(logradouro=obj)
            css = cota.css_cota()
        except Cota.DoesNotExist:
            pass
        return css

    class Meta:
        model = Logradouro
        geo_field = 'geom'
        fields = ('id', 'css',)
