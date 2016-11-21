# -*- coding: utf-8 -*-

from rest_framework import viewsets
from AlertaSJC.estacoes.models import Estacao
from AlertaSJC.estacoes.serializers import EstacaoSerializer


class EstacoesRestView(viewsets.ReadOnlyModelViewSet):
    serializer_class = EstacaoSerializer
    queryset = Estacao.objects.filter(tipo='plv')
