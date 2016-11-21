# -*- coding: utf-8 -*-

from rest_framework import viewsets
from AlertaSJC.geo.models import Cota
from AlertaSJC.geo.serializers import LogradouroSerializer


class LogradouroRestView(viewsets.ReadOnlyModelViewSet):
    serializer_class = LogradouroSerializer

    def get_queryset(self):
        '''
        retorna somente os logradouros que possuem algum nivel de atencao
        '''
        lista = []
        for cota in Cota.objects.all():
            if cota.css_cota() != '':
                lista.append(cota.logradouro)

        return lista
