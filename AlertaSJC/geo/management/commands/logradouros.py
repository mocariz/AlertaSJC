# -*- coding: utf-8 -*-

import os
import shapefile
from django.conf import settings
from django.contrib.gis.geos import LineString
from django.core.management.base import BaseCommand
from AlertaSJC.geo.models import Logradouro


class Command(BaseCommand):
    '''
    Comando para carregar os logradouros de são jose dos campos
    '''

    args = u'<modulo>'
    help = u'caminho do shapefile ex: modulo/pasta/arquivo'

    def handle(self, *args, **options):

        # obtem a base do diretorio
        file_path = os.path.join(settings.BASE_DIR,
                                 "AlertaSJC/geo/shape/roads.shp")

        # abre o shapefile
        arquivo = shapefile.Reader(file_path)

        # processa todos os pontos do shapefile e cria um lograadouro
        for linha in arquivo.iterShapeRecords():
            shape = linha.shape
            dados = linha.record

            # converter os points em lista
            points = map(lambda y: list(y), shape.points)
            logradouro, created = Logradouro.objects.update_or_create(
                geom=LineString(points),
                id=dados[0],
                codigo=dados[1],
                nome=dados[3])

            if created:
                logradouro.save()
