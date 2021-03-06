import threading

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from mutualFund import mf_scrape_service
# Create your views here.
from mutualFund.forms import MutualFundForm
from mutualFund.models import MutualFund
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def mf_create(request):
    if request.method == 'POST':
        form = MutualFundForm(request.POST)
        if form.is_valid():
            form.save()
            mutual_fund = form.instance
            scraping_th = threading.Thread(target=mf_scrape_service.scrape, args=[mutual_fund, ])
            scraping_th.start()
            return redirect('mfDetail', mutual_fund.pk)
    form = MutualFundForm()
    return render(request, 'portfolio/create.html', {'form': form})


@login_required
def mf_edit(request, pk, template_name='portfolio/edit.html'):
    mutual_fund = get_object_or_404(MutualFund, pk=pk)
    form = MutualFundForm(request.POST or None, instance=mutual_fund)
    if form.is_valid():
        form.save()
        return redirect('mfDetail', pk)
    return render(request, template_name, {'form': form})


class MutualFundDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = MutualFund
    template_name = 'mutualFund/mf_detail.html'


class IndexView(LoginRequiredMixin, ListView):
    login_url = '/login'
    template_name = 'mutualFund/index.html'
    context_object_name = 'mf_list'

    def get_queryset(self):
        return MutualFund.objects.all().order_by('mf_name')


@login_required
def mf_scrape(request, pk, template_name='mutualFund/scrape_response.html'):
    mutual_fund = get_object_or_404(MutualFund, pk=pk)
    scraping_th = threading.Thread(target=mf_scrape_service.scrape, args=[mutual_fund,])
    scraping_th.start()
    return render(request, template_name)


@login_required
def mf_scrape_all_user(request, template_name='mutualFund/scrape_response.html'):
    mf_scrape_service.scrape_all_user(request.user)
    return render(request, template_name)


@login_required
def mf_scrape_all(request, template_name='mutualFund/scrape_response.html'):
    mf_scrape_service.scrape_all()
    return render(request, template_name)
