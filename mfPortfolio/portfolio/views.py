from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView


from .forms import MutualFundForm, MutualFundSIPForm
from .models import MutualFund, MutualFundSIP


@login_required
def portfolio(request, template_name='portfolio/portfolio.html'):
    return render(request, template_name)


@login_required
def mf_chart_data(request):
    mutual_funds = MutualFund.objects.all().filter(created_by=request.user).order_by('-amount')

    mutual_funds_chart_data = list(map(lambda mutual_fund: {'name': mutual_fund.mutual_fund_global.mf_name, 'y': int(mutual_fund.amount)}, mutual_funds))
    if not mutual_funds_chart_data:
        raise Http404('No mutual funds found for this user')

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Mutual Fund Distribution'},
        'tooltip': {
            'pointFormat': '<b>{point.y}({point.percentage:.1f}%)</b>'
        },
        'plotOptions': {
            'series': {
                'dataLabels': {
                    'enabled': True
                },
                'showInLegend': False
            }
        },
        'series': [{
            'name': 'Mutual Fund Distribution',
            'data': mutual_funds_chart_data
        }]
    }
    return JsonResponse(chart)


@login_required
def sip_chart_data(request):
    sips = MutualFundSIP.objects.all().filter(active=True, created_by=request.user)\
        .values('mutual_fund__mutual_fund_global__mf_name')\
        .annotate(total_sip=Sum('amount'))\
        .order_by('-total_sip')
    sips_chart_data = list(map(lambda sip: {'name': sip['mutual_fund__mutual_fund_global__mf_name'], 'y': int(sip['total_sip'])}, sips))

    if not sips_chart_data:
        raise Http404('No active SIPs found for this user')

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Active SIPs'},
        'xAxis': {
            'type': 'category'
        },
        'yAxis': {
            'title': {
                'text': 'Amount'
            }
        },
        'tooltip': {
            'pointFormat': '<b>{point.y}</b>'
        },
        'plotOptions': {
            'series': {
                'dataLabels': {
                    'enabled': True
                }
            }
        },
        'series': [{
            'name': 'Active SIPs',
            'data': sips_chart_data
        }]
    }
    return JsonResponse(chart)


class MFIndexView(LoginRequiredMixin, ListView):
    login_url = '/login'
    template_name = 'portfolio/index.html'
    context_object_name = 'mf_list'

    def get_queryset(self):
        return MutualFund.objects.all().filter(created_by=self.request.user).order_by('-last_transaction_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_sum'] = context[self.context_object_name].aggregate(Sum('amount'))['amount__sum']
        return context


class SIPIndexView(LoginRequiredMixin, ListView):
    login_url = '/login'
    template_name = 'portfolio/sip_index.html'
    context_object_name = 'sip_list'

    def get_queryset(self):
        return MutualFundSIP.objects.all().filter(active=True, created_by=self.request.user).order_by('-last_transaction_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_sum'] = context[self.context_object_name].aggregate(Sum('amount'))['amount__sum']
        return context


class MutualFundDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = MutualFund
    template_name = 'portfolio/detail.html'


class MutualFundSIPDetailView(LoginRequiredMixin, DetailView):
    model = MutualFundSIP
    template_name = 'portfolio/sip_detail.html'


@login_required
def mf_create(request):
    if request.method == 'POST':
        form = MutualFundForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('portfolioMFDetail', form.instance.pk)
        else:
            return render(request, 'portfolio/create.html', {'form': form})
    form = MutualFundForm()

    return render(request, 'portfolio/create.html', {'form': form})


@login_required
def mf_edit(request, pk, template_name='portfolio/edit.html'):
    mutual_fund = get_object_or_404(MutualFund, pk=pk)
    form = MutualFundForm(request.POST or None, instance=mutual_fund, initial={
        'fields_to_disable': ['mutual_fund_global']})
    if form.is_valid():
        form.save()
        return redirect('portfolioMFDetail', pk)
    return render(request, template_name, {'form': form})


@login_required
def mf_delete(request, pk, template_name='portfolio/delete.html'):
    mutual_fund = get_object_or_404(MutualFund, pk=pk)
    if request.method == 'POST':
        mutual_fund.delete()
        return redirect('portfolioMFIndex')
    return render(request, template_name, {'object': mutual_fund})


@login_required
def sip_create(request):
    if request.method == 'POST':
        form = MutualFundSIPForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('sipDetail', form.instance.pk)
        else:
            return render(request, 'portfolio/sip_create.html', {'form': form})
    form = MutualFundSIPForm(user=request.user)
    return render(request, 'portfolio/sip_create.html', {'form': form})


@login_required
def sip_edit(request, pk, template_name='portfolio/edit.html'):
    mutual_fund_sip = get_object_or_404(MutualFundSIP, pk=pk)
    form = MutualFundSIPForm(request.POST or None, user=request.user, instance=mutual_fund_sip, initial={
        'fields_to_disable': ['amount', 'mutual_fund', 'start_date', 'frequency']})
    if form.is_valid():
        form.save()
        return redirect('sipDetail', pk)

    return render(request, template_name, {'form': form})



