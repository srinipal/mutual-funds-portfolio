from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.db.models import Sum
from django.forms.formsets import BaseFormSet
from django.forms.formsets import formset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from .forms import SIPRebalanceForm
from .models import MutualFundSIP, SIPRebalance, PortfolioRebalance
from . import analytics_helper
from mutualFund import mf_scrape_service


@login_required
def re_balance(request):
    sip_rebalance_activities = analytics_helper.get_sip_rebalance_activities(request.user.id)

    if request.method == 'GET':
        mf_scrape_service.scrape_all()

    context = {
        're_balance_activities': sip_rebalance_activities
    }
    return render(request, 'portfolio/portfolio_rebalance.html', context)


@login_required
def re_balance_activity_create(request, template_name='portfolio/new_rebalance_activity.html'):

    SIPFormSet = formset_factory(SIPRebalanceForm, BaseFormSet)
    if request.method == 'GET':
        mf_scrape_service.scrape_all()
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
                return redirect('portfolioRebalance')
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
    return render(request, template_name, context)


class SIPRebalanceView(LoginRequiredMixin, DetailView):
    template_name = 'portfolio/rebalance_activity.html'
    model = PortfolioRebalance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context