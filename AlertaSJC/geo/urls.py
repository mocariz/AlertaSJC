# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework import routers
from AlertaSJC.geo.rest import CotaRestView
from AlertaSJC.geo.views import MapaView

router = routers.DefaultRouter()
router.register(r'cotas', CotaRestView, base_name='cotas')

app_name = 'geo'

urlpatterns = [

    # API do rest com geojson
    url(r'^rest/', include(router.urls, namespace='rest')),

    url(r'^$', MapaView.as_view(), name='mapa'),
]
