# -*- coding: utf-8 -*-

from django.contrib.gis import admin
from AlertaSJC.dados.models.leitura import Leitura
from AlertaSJC.dados.models.leituraChuva import LeituraChuva
from AlertaSJC.dados.models.leituraSensor import LeituraSensor


class LeituraSensorInline(admin.TabularInline):
    model = LeituraSensor
    extra = 0


class LeituraChuvaInline(admin.TabularInline):
    model = LeituraChuva
    extra = 0


class LeituraAdmin(admin.ModelAdmin):
    date_hierarchy = 'horaLeitura'
    list_filter = ('estacao',)
    inlines = (LeituraSensorInline, LeituraChuvaInline,)


class LeituraSensorAdmin(admin.ModelAdmin):
    list_display = ('leitura', 'sensor', 'valor', )
    list_filter = ('leitura__estacao', 'sensor', )


class LeituraChuvaAdmin(admin.ModelAdmin):
    list_display = ('horaLeitura', 'h01', 'h24', 'mes', )
    list_filter = ('leitura__estacao', )

admin.site.register(Leitura, LeituraAdmin)
admin.site.register(LeituraSensor, LeituraSensorAdmin)
admin.site.register(LeituraChuva, LeituraChuvaAdmin)
