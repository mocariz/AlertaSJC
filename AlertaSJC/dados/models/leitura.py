# -*- coding: utf-8 -*-
'''
@author: Monica Mota
'''

from django.db import models
from django.utils import timezone


class Leitura(models.Model):
    horaLeitura = models.DateTimeField(db_index=True)
    horaRecebida = models.DateTimeField(blank=True, null=True)
    horaEnviada = models.DateTimeField(blank=True, null=True)
    estacao = models.ForeignKey('estacoes.Estacao')

    def __unicode__(self):
        horaLeitura = timezone.localtime(self.horaLeitura)
        return u'{0} - {1}'.format(self.estacao, horaLeitura)

    def create_leituraChuva(self):
        '''
        cria a leitura chuva
        '''
        from AlertaSJC.dados.models.leituraChuva import LeituraChuva
        from AlertaSJC.estacoes.models import Sensor

        try:
            try:
                # pega a leitura chuva ligada a leitura
                lc = self.leiturachuva
            except LeituraChuva.DoesNotExist:
                # cria uma leitura chuva
                lc = LeituraChuva(leitura=self)
            lc.createValoresChuva()
            lc.save()
        except Sensor.DoesNotExist as e:
            pass

    def createLeituraSensor(self, sensor, valor=None):
        '''
        cria uma leitura sensor para a leitura
        '''
        from AlertaSJC.estacoes.models import EstacaoSensor
        from AlertaSJC.dados.models.leituraSensor import LeituraSensor

        try:
            try:
                # pega a leitura sensor ligada a leitura
                ls = LeituraSensor.objects.get(leitura=self, sensor=sensor)
            except LeituraSensor.DoesNotExist:
                # cria uma nova leitura
                ls = LeituraSensor(leitura=self, sensor=sensor)

            ls.valor = valor
            ls.save()
        except EstacaoSensor.DoesNotExist:
            pass

    @property
    def css_nivel(self):
        '''
            Define o css do nivel de alerta para o nivel do rio
        '''
        css = ''
        leitura = self.leiturasensor_set.filter(sensor__nome='Nivel')[0]

        if leitura.valor > 1.0 and leitura.valor < 4.0:
            css = "ch-fraca"
        elif leitura.valor >= 4.0 and leitura.valor < 6.0:
            css = "ch-moderada"
        elif leitura.valor >= 6.0 and leitura.valor < 8.0:
            css = "ch-forte"
        elif leitura.valor > 8.0:
            css = "ch-muito-forte"
        return css

    class Meta:
        ordering = ['-horaLeitura']
        get_latest_by = 'horaLeitura'
        unique_together = ("horaLeitura", "estacao")
        index_together = [["horaLeitura", "estacao"]]
