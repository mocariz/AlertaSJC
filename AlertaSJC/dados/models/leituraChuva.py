# -*- coding: utf-8 -*-
'''
@author: Monica Mota
'''


from datetime import timedelta
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from AlertaSJC.estacoes.models import Sensor
from AlertaSJC.dados.models.leitura import Leitura
from AlertaSJC.dados.models.leituraSensor import LeituraSensor


class LeituraChuva(models.Model):
    leitura = models.OneToOneField(Leitura)
    h01 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="01 hora")
    h02 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="02 horas")
    h03 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="03 horas")
    h04 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="04 horas")
    h06 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="06 horas")
    h12 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="12 horas")
    h24 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="24 horas")
    h96 = models.FloatField(db_index=True, null=True, blank=True,
                            verbose_name="96 horas")
    mes = models.FloatField()

    @property
    def horaLeitura(self):
        '''
        utilizado no admin para exibir a horaLeitura no painel de administracao
        '''
        return self.leitura.horaLeitura

    class Meta:
        ordering = ('-leitura__horaLeitura',)
        get_latest_by = 'leitura__horaLeitura'

    def calculoValorChuva(self, tempo):
        inicio = self.leitura.horaLeitura - timedelta(minutes=tempo)
        fim = self.leitura.horaLeitura
        query = Leitura.objects.filter(
            estacao=self.leitura.estacao,
            horaLeitura__range=(inicio, fim)
        ).order_by("horaLeitura")

        first = query.first()
        last = query.last()
        minutos = timedelta(minutes=tempo)
        if abs(last.horaLeitura - first.horaLeitura) == minutos:
            sensor = Sensor.objects.get(tipo="vrnce")

            return LeituraSensor.objects.filter(
                leitura__estacao=self.leitura.estacao,
                sensor=sensor,
                leitura__horaLeitura__gt=inicio,
                leitura__horaLeitura__lte=fim
            ).aggregate(sum=Sum('valor'))['sum']
        else:
            return None

    def calculo_Mes(self):
        horaLeitura = timezone.localtime(self.leitura.horaLeitura)
        month = horaLeitura.month
        year = horaLeitura.year
        # obtem o sensor de variance da estacao
        variance = Sensor.objects.get(tipo="vrnce")
        queryMes = LeituraSensor.objects.filter(
            leitura__estacao=self.leitura.estacao,
            sensor=variance,
            leitura__horaLeitura__month=month,
            leitura__horaLeitura__year=year,
            leitura__horaLeitura__lte=self.leitura.horaLeitura)

        if queryMes.exists():
            return queryMes.aggregate(sum=Sum('valor'))['sum']
        else:
            return 0

    def createValoresChuva(self):
        campos = ['h01', 'h02', 'h03', 'h04', 'h06', 'h12', 'h24', 'h96']
        # calcula o valor da chuva para cada campo
        for campo in campos:
            minutos = LeituraChuva.convert_to_minutes(campo)
            setattr(self, campo, self.calculoValorChuva(minutos))
        # calcula o valor do mes
        self.mes = self.calculo_Mes()

    @staticmethod
    def convert_to_minutes(attr):
        '''
        recebe o valor do campo da leitura chuva e retorna a quatindade de
        minutos correspondente ao mesmo

        ex: h01 = 60, h02 = 120
        '''
        if attr.startswith('m'):
            return int(attr[1:])
        else:
            return int(attr[1:]) * 60

    @property
    def css_chuva(self):
        '''
        retorna o css correspondente ao nivel de alerta
        '''
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
