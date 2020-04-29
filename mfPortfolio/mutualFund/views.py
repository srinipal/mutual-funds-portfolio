from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render

# Create your views here.
from mutualFund.forms import MutualFundForm
from django.views.generic import DetailView, ListView

from mutualFund.models import MutualFund, MutualFundEquityAllocation, MutualFundAssetAllocation, MutualFundScrapeLog
from mutualFund.fundParse import money_control_scrape
from .utils.common_enums import AssetClass

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


def mf_scrape(request, template_name='mutualFund/scrape_response.html'):
    mf_id = request.GET['mf_id']
    mutual_fund = get_object_or_404(MutualFund, pk=mf_id)
    stocks_data = money_control_scrape.get_stocks_data(str(mutual_fund.pk), mutual_fund.holdings_url)

    # Delete all equity allocations
    MutualFundEquityAllocation.objects.all().filter(mutual_fund=mutual_fund).delete()

    # Delete all asset class allocations
    MutualFundAssetAllocation.objects.all().filter(mutual_fund=mutual_fund).delete()

    stock_data_list = stocks_data['stock_data_list']
    if len(stock_data_list) > 0:
        for stock_data in stock_data_list:
            mutual_fund_equity_allocation = MutualFundEquityAllocation()
            mutual_fund_equity_allocation.mutual_fund = mutual_fund

            # name, sector, sector_total, value, holdings_percent, prev_month_change_percent, past_year_highest_percent,
            # past_year_lowest_percent, quantity, prev_month_change_qty, m_cap, group_name
            mutual_fund_equity_allocation.stock_name = stock_data[0]
            mutual_fund_equity_allocation.sector = stock_data[1]
            mutual_fund_equity_allocation.sector_total = stock_data[2]
            mutual_fund_equity_allocation.holdings_value = stock_data[3]
            mutual_fund_equity_allocation.holdings_percent = stock_data[4]
            mutual_fund_equity_allocation.prev_month_change_percent = stock_data[5]
            mutual_fund_equity_allocation.past_year_highest_percent = stock_data[6]
            mutual_fund_equity_allocation.past_year_lowest_percent = stock_data[7]
            mutual_fund_equity_allocation.quantity = stock_data[8]
            mutual_fund_equity_allocation.prev_month_change_qty = stock_data[9]
            mutual_fund_equity_allocation.category = stock_data[10]
            mutual_fund_equity_allocation.group_name = stock_data[11]
            mutual_fund_equity_allocation.save()

    portfolio_percentages = stocks_data['portfolio_percentages']

    if AssetClass.EQUITY in portfolio_percentages:
        MutualFundAssetAllocation(mutual_fund=mutual_fund, asset_class=AssetClass.EQUITY.value,
                                  percentage=portfolio_percentages[AssetClass.EQUITY]).save()
    if AssetClass.DEBT in portfolio_percentages:
        MutualFundAssetAllocation(mutual_fund=mutual_fund, asset_class=AssetClass.DEBT.value,
                                  percentage=portfolio_percentages[AssetClass.DEBT]).save()
    if AssetClass.OTHERS in portfolio_percentages:
        MutualFundAssetAllocation(mutual_fund=mutual_fund, asset_class=AssetClass.OTHERS.value,
                                  percentage=portfolio_percentages[AssetClass.OTHERS]).save()

    MutualFundScrapeLog(mutual_fund=mutual_fund).save()

    return render(request, template_name)

