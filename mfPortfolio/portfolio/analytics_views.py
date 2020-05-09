from mutualFund import mf_scrape_service
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from . import analytics_helper
from django.http import JsonResponse


@login_required
def portfolio_analysis(request, template_name='portfolio/portfolio_analysis.html'):
    mf_scrape_service.scrape_all_user(request.user)
    return render(request, template_name)


@login_required
def sip_analysis(request, template_name='portfolio/sip_analysis.html'):
    mf_scrape_service.scrape_all_user(request.user)
    return render(request, template_name)


@login_required
def get_sector_distribution_data(request):
    sector_shares = []
    analysis_type = request.GET['type']
    if 'sip' == analysis_type:
        sector_shares = analytics_helper.get_sip_sector_shares(request.user.id)
    elif 'sipRebalance' == analysis_type:
        rebalance_id = request.GET['rebalance-id']
        sector_shares = analytics_helper.get_sip_rebalance_sector_shares(rebalance_id)
    else:
        sector_shares = analytics_helper.get_portfolio_sector_shares(request.user.id)

    sector_distribution_pie_data = analytics_helper.to_2d_chart_data(sector_shares, max_categories=20)

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Sector-wise Distribution'},
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
            'name': 'Sector-wise Distribution',
            'data': sector_distribution_pie_data
        }]
    }
    return JsonResponse(chart)


@login_required
def get_stock_distribution_data(request):
    stock_shares = []
    analysis_type = request.GET['type']
    if 'sip' == analysis_type:
        stock_shares = analytics_helper.get_sip_stock_shares(request.user.id)
    elif 'sipRebalance' == analysis_type:
        rebalance_id = request.GET['rebalance-id']
        stock_shares = analytics_helper.get_sip_rebalance_stock_shares(rebalance_id)
    else:
        stock_shares = analytics_helper.get_portfolio_stock_shares(request.user.id)

    stock_shares_distribution_data = analytics_helper.to_2d_chart_data(stock_shares, max_categories=20)

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Stock-wise Distribution'},
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
            'name': 'Stock-wise Distribution',
            'data': stock_shares_distribution_data
        }]
    }

    return JsonResponse(chart)


@login_required
def get_popular_stocks(request):
    popular_stocks = []
    analysis_type = request.GET['type']
    if 'sip' == analysis_type:
        popular_stocks = analytics_helper.get_sip_popular_stocks(request.user.id)
    else:
        popular_stocks = analytics_helper.get_portfolio_popular_stocks(request.user.id)

    popular_stocks_data = analytics_helper.to_2d_chart_data(popular_stocks)

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Popular Stocks'},
        'xAxis': {
            'type': 'category'
        },
        'yAxis': {
            'title': {
                'text': 'Popularity Score'
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
            'name': 'Popular Stocks',
            'data': popular_stocks_data
        }]
    }

    return JsonResponse(chart)
