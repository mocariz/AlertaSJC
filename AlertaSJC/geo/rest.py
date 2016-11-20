# -*- coding: utf-8 -*-

from rest_framework import viewsets
from AlertaSJC.geo.models import Cota
from AlertaSJC.geo.serializers import CotaSerializer


class CotaRestView(viewsets.ReadOnlyModelViewSet):
    serializer_class = CotaSerializer
    queryset = Cota.objects.all()
