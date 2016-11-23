# -*- coding: utf-8 -*-
'''
@author: monica
'''

from django.contrib.gis import admin
from AlertaSJC.estacoes.models import EstacaoSensor, Estacao, Sensor, Fonte


class EstacaoSensorInLine(admin.TabularInline):
    model = EstacaoSensor
    extra = 0


class EstacaoAdmin(admin.OSMGeoAdmin):
    list_display = ('nome', 'codigo', 'fonte')
    list_filter = ('fonte',)
    inlines = (EstacaoSensorInLine,)
    save_as = True


admin.site.register(Estacao, EstacaoAdmin)
admin.site.register(Sensor)
admin.site.register(Fonte)
