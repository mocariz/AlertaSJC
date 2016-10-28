# -*- coding: UTF-8 -*-

from datetime import timedelta
from django.views.generic.base import View
from django.shortcuts import render, get_object_or_404

from TrajetoSecoSJC.estacoes.models import Estacao
from TrajetoSecoSJC.dados.forms import PeriodoForm
from TrajetoSecoSJC.dados.models.leituraChuva import LeituraChuva


class Leituras(View):
    template = 'dados/leitura.html'

    def get(self, request):
        estacoes = Estacao.objects.filter(tipo='plv')
        lc = LeituraChuva.objects.filter(leitura__estacao__in=estacoes) \
            .order_by('leitura__estacao__id', '-leitura__horaLeitura') \
            .distinct('leitura__estacao__id')

        return render(request, self.template, {
            'dados': lc,
        })


class Historico(View):
    template = 'dados/historico.html'
    form = PeriodoForm

    def leituras(self, estacao, inicio, fim):
        return LeituraChuva.objects.select_related('leitura').filter(
            leitura__estacao=estacao,
            leitura__horaLeitura__range=(inicio, fim)
        ).order_by('-leitura__horaLeitura')

    def get(self, request, estacao_id):
        estacao = get_object_or_404(Estacao, pk=estacao_id)
        try:
            chuva = LeituraChuva.objects.select_related('leitura').filter(
                leitura__estacao=estacao).latest("leitura__horaLeitura")

            fim = chuva.leitura.horaLeitura
            inicio = fim - timedelta(hours=24)
            data = {'inicio': inicio, 'fim': fim}

            form = self.form(initial=data)
            leituras = self.leituras(estacao, inicio, fim)
        except LeituraChuva.DoesNotExist:
            form = self.form()
            leituras = []

        return render(request, self.template, {
            'lista': leituras,
            'form': form,
            'estacao': estacao.nome,
            'pk': estacao.pk,
        })

    def post(self, request, estacao_id):
        estacao = get_object_or_404(Estacao, pk=estacao_id)
        form = self.form(request.POST)
        if form.is_valid():
            inicio = form.cleaned_data['inicio']
            fim = form.cleaned_data['fim']
            leituras = self.leituras(estacao, inicio, fim)
        else:
            leituras = []

        return render(request, self.template, {
            'lista': leituras,
            'form': form,
            'estacao': estacao.nome,
            'pk': estacao.pk,
        })
