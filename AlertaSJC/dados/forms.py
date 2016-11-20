# -*- coding: UTF-8 -*-

import datetime
from django import forms
from django.utils import timezone
from django.utils.encoding import force_str


class DateTimeInput(forms.DateTimeInput):
    '''
    Widget do DateTimeInput com as configurações do datetimepicker
    '''
    def __init__(self):
        date_format = '%d/%m/%Y %H:%M'
        attrs = {'class': 'datetimepicker',
                 'data-datetimepicker': 'datetime',
                 'data-date-format': 'DD/MM/YYYY HH:mm'}
        super(DateTimeInput, self).__init__(attrs=attrs, format=date_format)


class DateTimeField(forms.DateTimeField):
    '''
    DateTimeField com o widget padrão com as configurações do datetimepicker
    '''
    widget = DateTimeInput
    input_formats = ['%d/%m/%Y %H:%M']

    def strptime(self, value, format):
        local_tz = timezone.get_current_timezone()
        result = datetime.datetime.strptime(force_str(value), format)
        return result


class PeriodoForm(forms.Form):
    inicio = DateTimeField()
    fim = DateTimeField()

    def clean(self):
        data = super(PeriodoForm, self).clean()

        if data.get('inicio') > data.get('fim'):
            raise forms.ValidationError(
                "A data inicial deve menor que a data final"
            )
