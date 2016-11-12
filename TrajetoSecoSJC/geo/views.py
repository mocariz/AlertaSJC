# -*- coding: UTF-8 -*-

from django.views.generic.base import View
from django.shortcuts import render


class CurvaNivelView(View):
    template = 'geo/curva_mapa.html'

    def get(self, request):
        return render(request, self.template)
