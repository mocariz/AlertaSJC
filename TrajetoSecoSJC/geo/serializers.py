# -*- coding: utf-8 -*-

from TrajetoSecoSJC.geo.models import CurvaNivel
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class CurvaNivelSerializer(GeoFeatureModelSerializer):
    '''
    Serializer da Classe CurvaNivel
    '''

    class Meta:
        model = CurvaNivel
        geo_field = 'geom'
        fields = ('altitude',)


class CotaSerializer(GeoFeatureModelSerializer):
    '''
    Serializer da Classe CurvaNivel
    '''

    class Meta:
        model = CurvaNivel
        geo_field = 'geom'
        fields = ('altitude',)
