# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from AlertaSJC.geo.models import Logradouro, Cota
import requests
import json


class Command(BaseCommand):
    '''
    Comando para criar as cotas com base na elevação obtida pela api do google:
    Google Elevation API
    '''

    def handle(self, *args, **options):
        # parametros do Google Elevation API
        url = "https://maps.googleapis.com/maps/api/elevation/json?locations" \
              "={0}&key={1}"
        key = 'AIzaSyAja4jfU-mjd3IjUqTk03zAc1R8sRGAuqY'

        USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) ' \
                     'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/28.0.1500.71 Safari/537.36'

        for logradouro in Logradouro.objects.all():
            coords = logradouro.get_center()
            coordenadas = u'{0}, {1}'.format(coords[1], coords[0])

            try:
                Cota.objects.get(logradouro=logradouro)
                print 'Cota já existe'
            except Cota.DoesNotExist:
                path = url.format(coordenadas, key)
                response = requests.get(path, timeout=240, headers={
                    'User-Agent': USER_AGENT})

                data = json.loads(response.text)['results'][0]

                cota = Cota.objects.create(
                    logradouro=logradouro,
                    cheia=data['elevation']
                )
                cota.save()
                print 'Criada nova cota para' + logradouro.nome
