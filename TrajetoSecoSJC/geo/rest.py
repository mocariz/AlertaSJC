# -*- coding: utf-8 -*-

from rest_framework import viewsets
from TrajetoSecoSJC.geo.models import CurvaNivel, Cota
from TrajetoSecoSJC.geo.serializers import CurvaNivelSerializer, CotaSerializer


class CurvaNivelRestView(viewsets.ReadOnlyModelViewSet):
    serializer_class = CurvaNivelSerializer
    queryset = CurvaNivel.objects.all()


class CotaRestView(viewsets.ReadOnlyModelViewSet):
    serializer_class = CotaSerializer
    queryset = Cota.objects.all()
