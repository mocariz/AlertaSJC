# -*- coding: utf-8 -*-

from rest_framework import viewsets
from TrajetoSecoSJC.geo.models import CurvaNivel
from TrajetoSecoSJC.geo.serializers import CurvaNivelSerializer


class CurvaNivelRestView(viewsets.ReadOnlyModelViewSet):
    serializer_class = CurvaNivelSerializer
    queryset = CurvaNivel.objects.all()
