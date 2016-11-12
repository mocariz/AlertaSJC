# -*- coding: utf-8 -*-
'''
@author: Monica Mota
'''

import logging
from datetime import timedelta
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from TrajetoSecoSJC.dados.models.leitura import Leitura
from TrajetoSecoSJC.dados.models.leituraSensor import LeituraSensor

logger = logging.getLogger(__name__)


class LeituraChuva(models.Model):
    """
    Classe para fazer a persistência e o calculo da chuva
    """

    leitura = models.OneToOneField(Leitura)
    m15 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="Em 15 min")
    m30 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="Em 30 min")
    h01 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="Em 01 hora")
    h02 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="Em 02 horas")
    h03 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="Em 03 horas")
    h04 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="Em 04 horas")
    h06 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="Em 06 horas")
    h12 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="Em 12 horas")
    h24 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="EM 24 horas")
    h36 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="Em 36 horas")
    h48 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="Em 42 horas")
    h72 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="Em 72 horas")
    h96 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="Em 96 horas")
    h168 = models.FloatField(db_index=True, null=True, blank=True,
                             verbose_name="Em 168 horas")
    mes = models.FloatField()

    @property
    def estacao(self):
        return self.leitura.estacao.pk

    @property
    def horaLeitura(self):
        return self.leitura.horaLeitura

    def __getitem__(self, periodo):
        return getattr(self, periodo)

    class Meta:
        ordering = ('-leitura__horaLeitura',)
        get_latest_by = 'leitura__horaLeitura'

    def calculoValorChuva(self, tempo):
        inicio = self.leitura.horaLeitura \
            - timedelta(minutes=tempo)
        fim = self.leitura.horaLeitura
        query = Leitura.objects \
            .filter(estacao=self.leitura.estacao,
                    horaLeitura__range=(inicio, fim)) \
            .order_by("horaLeitura")
        first = query[0]
        last = query.reverse()[0]
        if abs(last.horaLeitura - first.horaLeitura) == \
                timedelta(minutes=tempo):
            variance = self.leitura.estacao.sensores.get(tipo="vrnce")
            return LeituraSensor.objects \
                .filter(leitura__estacao=self.leitura.estacao,
                        sensor=variance,
                        leitura__horaLeitura__gt=inicio,
                        leitura__horaLeitura__lte=fim).aggregate(
                            sum=Sum('valor'))['sum']
        else:
            return None

    def calculo_Mes(self):
        horaLeitura = timezone.localtime(self.leitura.horaLeitura)
        month = horaLeitura.month
        year = horaLeitura.year
        # obtem o sensor de variance da estacao
        variance = self.leitura.estacao.sensores.get(tipo="vrnce")
        try:
            firstOfMes = LeituraSensor.objects \
                .filter(leitura__estacao=self.leitura.estacao,
                        sensor=variance,
                        leitura__horaLeitura__month=month,
                        leitura__horaLeitura__year=year) \
                .earliest()
            queryMes = LeituraSensor.objects \
                .filter(leitura__estacao=self.leitura.estacao,
                        sensor=variance,
                        leitura__horaLeitura__month=month,
                        leitura__horaLeitura__year=year,
                        leitura__horaLeitura__lte=self.leitura.horaLeitura,
                        leitura__horaLeitura__gt=firstOfMes.leitura
                        .horaLeitura)

            if queryMes.exists():
                return queryMes.aggregate(sum=Sum('valor'))['sum']
            else:
                return 0

        except LeituraSensor.DoesNotExist:
            return 0

    def createValoresChuva(self):
        attrs = filter(lambda k: k != 'mes' and
                       k.startswith('m') or
                       k.startswith('h') and
                       len(k) < 5, dir(self))
        for attr in attrs:
            tempo = LeituraChuva.get_minutes_for_attr(attr)
            setattr(self, attr, self.calculoValorChuva(tempo))
        self.mes = self.calculo_Mes()

    @staticmethod
    def get_minutes_for_attr(attr):
        if attr.startswith('m'):
            return int(attr[1:])
        else:
            return int(attr[1:]) * 60

    @property
    def css_chuva(self):
        css = ''
        if self.h24 < 10.0 and self.h24 > 0.4:
            css = "ch-fraca"
        elif self.h24 >= 10.0 and self.h24 < 30.0:
            css = "ch-moderada"
        elif self.h24 >= 30.0 and self.h24 < 70.0:
            css = "ch-forte"
        elif self.h24 > 70.0:
            css = "ch-muito-forte"
        return css

    def json_leiturachuva(self):
        return {
            "estacao_id": self.leitura.estacao.id,
            "nome": self.leitura.estacao.nome,
            "horaLeitura": self.leitura.horaLeitura,
            "m15": self.m15,
            "m30": self.m30,
            "h01": self.h01,
            "h02": self.h02,
            "h03": self.h03,
            "h04": self.h04,
            "h06": self.h06,
            "h12": self.h12,
            "h24": self.h24,
            "h36": self.h36,
            "h48": self.h48,
            "h72": self.h72,
            "h96": self.h96,
            "h168": self.h168,
            "mes": self.mes,
            "classe": self.css_chuva,
        }
