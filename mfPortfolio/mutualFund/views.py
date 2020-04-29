from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render

# Create your views here.
from mutualFund.forms import MutualFundForm
from django.views.generic import DetailView, ListView

from mutualFund.models import MutualFund


def mf_create(request):
    if request.method == 'POST':
        form = MutualFundForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mfDetail', form.instance.pk)
    form = MutualFundForm()
    return render(request, 'portfolio/create.html', {'form': form})


class MutualFundDetailView(DetailView):
    model = MutualFund
    template_name = 'mutualFund/mf_detail.html'


class IndexView(ListView):
    template_name = 'mutualFund/index.html'
    context_object_name = 'mf_list'

    def get_queryset(self):
        return MutualFund.objects.all().order_by('mf_name')
