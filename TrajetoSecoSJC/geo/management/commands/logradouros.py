# -*- coding: utf-8 -*-

import os
import shapefile
from django.conf import settings
from django.contrib.gis.geos import LineString
from django.core.management.base import BaseCommand
from TrajetoSecoSJC.geo.models import Logradouro, TIPO


class Command(BaseCommand):
    '''
    Comando para carregar os logradouros de são jose dos campos
    '''

    args = u'<modulo>'
    help = u'caminho do shapefile ex: modulo/pasta/arquivo'

    def handle(self, *args, **options):

        # obtem a base do diretorio
        file_path = os.path.join(settings.BASE_DIR,
                                 "TrajetoSecoSJC/geo/shape/roads.shp")

        # abre o shapefile
        arquivo = shapefile.Reader(file_path)

        # processa todos os pontos do shapefile e cria um lograadouro
        for linha in arquivo.iterShapeRecords():
            shape = linha.shape
            dados = linha.record
            lTipo = 'un'

            # define o tipo do logradouro com base nos tipos da lista
            for tipo in TIPO:
                if tipo[1] == dados[2]:
                    lTipo = tipo[0]

            if dados[6] == 1:
                sentido = True
            else:
                sentido = False

            # converter os points em lista
            points = map(lambda y: list(y), shape.points)
            logradouro, created = Logradouro.objects.update_or_create(
                geom=LineString(points),
                id=dados[0],
                codigo=dados[1],
                nome=dados[3],
                tipo=lTipo,
                maounica=sentido,
                referencia=dados[7])

            if created:
                logradouro.save()
