from django.urls import path

from . import views, analytics_views, rebalance_views

urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    path('mf-chart/', views.mf_chart_data, name='portfolioMFChart'),
    path('sip-chart/', views.sip_chart_data, name='portfolioSIPChart'),
    path('mutual-funds/', views.MFIndexView.as_view(), name='portfolioMFIndex'),
    path('mutual-funds-create/', views.mf_create, name='portfolioMFCreate'),
    path('mutual-funds-view/<int:pk>/', views.MutualFundDetailView.as_view(), name='portfolioMFDetail'),
    path('mutual-funds-edit/<int:pk>/', views.mf_edit, name='portfolioMFEdit'),
    path('mutual-funds-delete/<int:pk>/', views.mf_delete, name='portfolioMFDelete'),
    path('sips/', views.SIPIndexView.as_view(), name='sipIndex'),
    path('sips-create/', views.sip_create, name='sipCreate'),
    path('sips-edit/<int:pk>/', views.sip_edit, name='sipEdit'),
    path('sips-view/<int:pk>/', views.MutualFundSIPDetailView.as_view(), name='sipDetail'),
    path('portfolio-analysis/', analytics_views.portfolio_analysis, name='portfolioAnalysis'),
    path('sip-analysis/', analytics_views.sip_analysis, name='sipAnalysis'),
    path('sector-distribution-chart/', analytics_views.get_sector_distribution_data, name='sectorDistribution'),
    path('stock-distribution-chart/', analytics_views.get_stock_distribution_data, name='stockDistribution'),
    path('popular-stocks-chart/', analytics_views.get_popular_stocks, name='popularStocks'),
    path('portfolio-rebalance/', rebalance_views.re_balance, name='portfolioRebalance'),
    path('portfolio-rebalance-create/', rebalance_views.re_balance_activity_create, name='portfolioRebalanceCreate'),
    path('portfolio-rebalance-activity/<int:pk>/', rebalance_views.SIPRebalanceView.as_view(), name='portfolioRebalanceActivity'),
]