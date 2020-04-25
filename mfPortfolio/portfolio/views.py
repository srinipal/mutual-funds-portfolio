from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import MutualFund, MutualFundSIP
from .forms import MutualFundForm, MutualFundSIPForm
from django.views.generic import ListView, DetailView


class IndexView(ListView):
    template_name = 'portfolio/index.html'
    context_object_name = 'mf_list'

    def get_queryset(self):
        return MutualFund.objects.all()

class SIPIndexView(ListView):
    template_name = 'portfolio/sip_index.html'
    context_object_name = 'sip_list'

    def get_queryset(self):
        return MutualFundSIP.objects.all()

class MutualFundDetailView(DetailView):
    model = MutualFund
    template_name = 'portfolio/detail.html'

class MutualFundSIPDetailView(DetailView):
    model = MutualFundSIP
    template_name = 'portfolio/sip_detail.html'

def mf_edit(request, pk, template_name='portfolio/edit.html'):
    mutual_fund = get_object_or_404(MutualFund, pk=pk)
    form = MutualFundForm(request.POST or None, instance=mutual_fund)
    if form.is_valid():
        form.save()
        return redirect('mfDetail', pk)
    return render(request, template_name, {'form': form})


def mf_delete(request, pk, template_name='portfolio/delete.html'):
    mutual_fund = get_object_or_404(MutualFund, pk=pk)
    if request.method == 'POST':
        mutual_fund.delete()
        return redirect('mfIndex')
    return render(request, template_name, {'object': mutual_fund})


def mf_create(request):
    if request.method == 'POST':
        form = MutualFundForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mfIndex')
    form = MutualFundForm()

    return render(request, 'portfolio/create.html', {'form': form})


def sip_create(request):
    if request.method == 'POST':
        form = MutualFundSIPForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mfIndex')
    form = MutualFundSIPForm()
    return render(request, 'portfolio/create.html', {'form': form})

def sip_edit(request, pk, template_name='portfolio/edit.html'):
    mutual_fund_sip = get_object_or_404(MutualFundSIP, pk=pk)
    form = MutualFundSIPForm(request.POST or None, instance=mutual_fund_sip)
    if form.is_valid():
        form.save()
        return redirect('sipDetail', pk)
    return render(request, template_name, {'form': form})

