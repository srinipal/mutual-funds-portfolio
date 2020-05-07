from django.contrib.auth.decorators import login_required
from django.forms.formsets import BaseFormSet
from django.forms.formsets import formset_factory
from django.shortcuts import render

from .forms import SIPRebalanceForm
from .models import MutualFundSIP


@login_required
def re_balance(request):
    SIPFormSet = formset_factory(SIPRebalanceForm, BaseFormSet)

    initial_mf_sips = []
    if request.method == 'POST':
        None
    else:
        mutual_fund_sips = MutualFundSIP.objects.all().filter(active=True, created_by=request.user)
        initial_mf_sips = [{'mutual_fund_global': l.mutual_fund.mutual_fund_global, 'amount': l.amount}
                           for l in mutual_fund_sips]

    sip_formset = SIPFormSet(initial=initial_mf_sips)
    context = {
        'sip_formset': sip_formset
    }
    return render(request, 'portfolio/portfolio_rebalance.html', context)
