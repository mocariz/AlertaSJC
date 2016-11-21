# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from AlertaSJC.geo.models import Cota


class Command(BaseCommand):
    '''
    Ponto de referencia usado para o nivel do rio são as coordenadas:
    -23.153995, -45.897464, que representa o rio paraiba do sul
    '''

    def handle(self, *args, **options):
        # valor da altitude no nivel do rio obtido pela api elevation
        rio = 554.56


        for cota in Cota.objects.all():
            diferenca = float(cota.altitude) - rio
            cheia = 0

            if diferenca < 0:
                # 8 metros é o valor maximo de atenção para o nivel do rio
                cheia = 8.1
            elif diferenca < 5:
                cheia = diferenca + 5
            else:
                cheia = diferenca

            cota.cota = cheia
            cota.save()
