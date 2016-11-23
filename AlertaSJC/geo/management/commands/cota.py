# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from AlertaSJC.geo.models import Logradouro, Cota
from django.conf import settings
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

        for logradouro in Logradouro.objects.all():
            coords = logradouro.get_center()
            coordenadas = u'{0}, {1}'.format(coords[1], coords[0])

            try:
                Cota.objects.get(logradouro=logradouro)
            except Cota.DoesNotExist:
                path = url.format(coordenadas, key)
                response = requests.get(path, timeout=240, headers={
                    'User-Agent': settings.USER_AGENT})

                data = json.loads(response.text)['results'][0]

                cota = Cota.objects.create(
                    logradouro=logradouro,
                    altitude=data['elevation']
                )
                cota.save()
