# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework import routers
from AlertaSJC.estacoes.rest import EstacoesRestView

router = routers.DefaultRouter()
router.register(r'estacoes', EstacoesRestView, base_name='estacoes')

app_name = 'estacoes'

urlpatterns = [

    # API do rest com geojson
    url(r'^rest/', include(router.urls, namespace='rest')),
]
