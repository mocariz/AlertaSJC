# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework import routers
from TrajetoSecoSJC.geo.rest import CurvaNivelRestView
from TrajetoSecoSJC.geo.views import CurvaNivelView

router = routers.DefaultRouter()
router.register(r'curvas', CurvaNivelRestView, base_name='curvas')

app_name = 'geo'

urlpatterns = [

    # API do rest com geojson
    url(r'^rest/', include(router.urls, namespace='rest')),

    url(r'^$', CurvaNivelView.as_view(), name='curva'),
]
