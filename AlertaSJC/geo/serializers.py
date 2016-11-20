# -*- coding: utf-8 -*-

from AlertaSJC.geo.models import Cota
from rest_framework_gis.serializers import GeoFeatureModelSerializer

class CotaSerializer(GeoFeatureModelSerializer):
    '''
    Serializer da Classe CurvaNivel
    '''

    class Meta:
        model = Cota
        geo_field = 'geom'
        fields = ('cheia',)
