# -*- coding: UTF-8 -*-

from django.conf.urls import url
from AlertaSJC.dados.views import Leituras, Historico, NivelView, MapaView

app_name = 'dados'

urlpatterns = [
    url(r'^$', Leituras.as_view(), name='chuva'),
    url(r'^historico/(?P<estacao_id>\d+)/$', Historico.as_view(),
        name="historico"),
    url(r'^nivel_rio$', NivelView.as_view(), name='nivel'),
    url(r'^mapa$', MapaView.as_view(), name='mapa-estacoes'),
]
