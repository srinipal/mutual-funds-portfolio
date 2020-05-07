from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.forms.formsets import BaseFormSet
from django.forms.formsets import formset_factory
from django.shortcuts import render, redirect

from .forms import SIPRebalanceForm
from .models import MutualFundSIP, SIPRebalance, PortfolioRebalance


@login_required
def re_balance(request):
    SIPFormSet = formset_factory(SIPRebalanceForm, BaseFormSet)

    if request.method == 'POST':
        sip_formset = SIPFormSet(request.POST)
        if sip_formset.is_valid():
            try:
                with transaction.atomic():
                    portfolio_rebalance = PortfolioRebalance(created_by=request.user)
                    portfolio_rebalance.save()
                    new_sips = []
                    for sip_form in sip_formset:
                        mutual_fund = sip_form.cleaned_data.get('mutual_fund_global')
                        sip_amount = sip_form.cleaned_data.get('amount')
                        new_sips.append(
                            SIPRebalance(mutual_fund_global=mutual_fund, amount=sip_amount, created_by=request.user,
                                         re_balance=portfolio_rebalance))

                    SIPRebalance.objects.bulk_create(new_sips)
            except IntegrityError:  # If the transaction failed
                messages.error(request, 'There was an error saving your profile.')

    else:
        mutual_fund_sips = MutualFundSIP.objects.all().filter(active=True, created_by=request.user)
        initial_mf_sips = [{'mutual_fund_global': l.mutual_fund.mutual_fund_global, 'amount': l.amount}
                           for l in mutual_fund_sips]

        sip_formset = SIPFormSet(initial=initial_mf_sips)
    context = {
        'sip_formset': sip_formset
    }
    return render(request, 'portfolio/portfolio_rebalance.html', context)
