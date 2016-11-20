# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from AlertaSJC.estacoes.models import Fonte


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        """
            Captura e salva as leituras da fontes cemaden
        """

        cemaden = Fonte.objects.get(pk=1)
        cemaden.fonte_CEMADEN()
