# -*- coding: utf-8 -*-

import os
from django.conf import settings
from django.core.management.base import BaseCommand
from TrajetoSecoSJC.geo.models import CurvaNivel, Logradouro, Cota
from django.contrib.gis.geos import *

from django.contrib.gis.measure import D

class Command(BaseCommand):
    '''
    Comando para criar as cotas com base na nas curvas de nivel

    as curvas de nivel representam a altitude do terreno

    o ponto de referencia usado para o nivel do rio tem altitude de 550m
    em relacao ao nivel do mar
    '''

    def handle(self, *args, **options):
        rio = 550
        distance = 2000

        for rua in Logradouro.objects.all():
            point = Point(rua.get_center())

            try:
                curva = CurvaNivel.objects.filter(
                    geom__distance_lte=(point, D(m=distance)))[0]
                curva = curva.altitude
            except IndexError:
                curva = 550

            cota = curva - rio
            print cota, curva
