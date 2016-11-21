# -*- coding: utf-8 -*-
'''
@author: Monica Mota
'''

from datetime import timedelta
import logging
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)

TIME_DELAY = timedelta(minutes=18)


class Leitura(models.Model):
    """
    Classe para fazer a persistência das leituras enviada pela estações
    """

    horaLeitura = models.DateTimeField(db_index=True)
    horaRecebida = models.DateTimeField(blank=True, null=True)
    horaEnviada = models.DateTimeField(blank=True, null=True)
    estacao = models.ForeignKey('estacoes.Estacao')

    def __unicode__(self):
        horaLeitura = timezone.localtime(self.horaLeitura) \
                              .strftime('%d/%m/%Y %H:%M:%S')
        return u'{0} - {1}'.format(self.estacao, horaLeitura)

    def atualiza_or_create_leituraChuva(self):
        from AlertaSJC.dados.models.leituraChuva import LeituraChuva
        from AlertaSJC.estacoes.models import Sensor

        try:
            try:
                lc = self.leiturachuva
            except LeituraChuva.DoesNotExist:
                lc = LeituraChuva(leitura=self)
            lc.createValoresChuva()
            lc.save()
        except Sensor.DoesNotExist as e:
            logger.error(u"{0} - {1}".format(self, e))

    def createLeituraSensor(self, sensor, valor=None):
        '''
        :param sensor: Instancia do Sensor a ser gravado
        :type sensor: Sensor
        :param valor: Valor Bruto do sensor
        :type valor: float
        :return: Instancia do Sensor criado
        :rtype: LeituraSensor
        '''
        from AlertaSJC.estacoes.models import EstacaoSensor
        from AlertaSJC.dados.models.leituraSensor import LeituraSensor

        try:
            try:
                ls = LeituraSensor.objects.get(
                    leitura=self, sensor=sensor)
                logger.debug("%s - Atualizado" % ls)
            except LeituraSensor.DoesNotExist:
                ls = LeituraSensor(
                    leitura=self, sensor=sensor)
                logger.debug("%s - Criado" % ls)

            ls.valor = valor
            ls.save()
            return ls
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
