# -*- coding: utf-8 -*-

from rest_framework import viewsets
from AlertaSJC.geo.models import Logradouro
from AlertaSJC.geo.serializers import LogradouroSerializer


class LogradouroRestView(viewsets.ReadOnlyModelViewSet):
    serializer_class = LogradouroSerializer
    queryset = Logradouro.objects.all()
