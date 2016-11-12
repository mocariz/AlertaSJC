# -*- coding: utf-8 -*-

import os
import shapefile
from django.conf import settings
from django.contrib.gis.geos import LineString
from django.core.management.base import BaseCommand
from TrajetoSecoSJC.geo.models import CurvaNivel


class Command(BaseCommand):
    '''
    Comando para carregar as curvas de nivel
    '''

    def handle(self, *args, **options):

        # obtem a base do diretorio
        file_path = os.path.join(settings.BASE_DIR,
                                 "TrajetoSecoSJC/geo/shape/altitude2.shp")

        # abre o shapefile
        arquivo = shapefile.Reader(file_path)

        # processa todos os pontos do shapefile e cria um lograadouro
        for linha in arquivo.iterShapeRecords():
            shape = linha.shape
            dados = linha.record
            print dados

            # converter os points em lista
            points = map(lambda y: list(y), shape.points)
            curva, created = CurvaNivel.objects.update_or_create(
                geom=LineString(points),
                id=dados[0],
                altitude=dados[1])

            if created:
                curva.save()
