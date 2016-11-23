# -*- coding: utf-8 -*-
'''
@author: Monica Mota
'''

from django.db import models


class LeituraSensor(models.Model):
    leitura = models.ForeignKey('dados.Leitura')
    sensor = models.ForeignKey('estacoes.Sensor')
    valor = models.FloatField()

    def __unicode__(self):
        return u"{0}: {1}".format(self.leitura, self.sensor)

    class Meta:
        unique_together = ("leitura", "sensor")
        get_latest_by = 'leitura__horaLeitura'
        ordering = ('-leitura__horaLeitura',)
