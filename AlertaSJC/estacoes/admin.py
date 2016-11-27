# -*- coding: utf-8 -*-
'''
@author: monica
'''

from django.contrib.gis import admin
from AlertaSJC.estacoes.models import Estacao, Sensor, Fonte


class EstacaoAdmin(admin.OSMGeoAdmin):
    list_display = ('nome', 'codigo', 'fonte')
    list_filter = ('fonte',)
    save_as = True


admin.site.register(Estacao, EstacaoAdmin)
admin.site.register(Sensor)
admin.site.register(Fonte)
