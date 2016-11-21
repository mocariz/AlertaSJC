# -*- coding: utf-8 -*-

from AlertaSJC.geo.models import Cota, Logradouro
from AlertaSJC.dados.models.leituraSensor import LeituraSensor
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class LogradouroSerializer(GeoFeatureModelSerializer):
    css = serializers.SerializerMethodField()

    def get_css(self, obj):
        '''
        Define o css do nivel de alerta para o nivel do rio
        '''
        css = ''
        leitura = LeituraSensor.objects.filter(
            sensor__pk=2,
            leitura__estacao__id=11
        ).latest()

        try:
            cota = Cota.objects.get(logradouro=obj).cheia
            diferenca = float(cota) - leitura.valor

            if diferenca > 3.0:
                css = "vigilancia"
            elif diferenca >= 2.0 :
                css = "atencao"
            elif diferenca >= 1:
                css = "alerta"
            elif leitura.valor > cota:
                css = "prontidao"
        except Cota.DoesNotExist:
            pass
        return css

    class Meta:
        model = Logradouro
        geo_field = 'geom'
        fields = ('id', 'css',)
