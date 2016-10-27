# -*- coding: utf-8 -*-
'''
@author: monica
'''

from django.contrib.gis import admin
from TrajetoSecoSJC.geo.models import Logradouro, Cota

admin.site.register(Logradouro)
admin.site.register(Cota)
