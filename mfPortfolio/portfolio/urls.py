from django.urls import path

from . import views

urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    path('mf-chart/', views.mf_chart_data, name='portfolioMFChart'),
    path('sip-chart/', views.sip_chart_data, name='portfolioSIPChart'),
    path('mutual-funds/', views.IndexView.as_view(), name='portfolioIndex'),
    path('mutual-funds-create/', views.mf_create, name='portfolioMFCreate'),
    path('mutual-funds-view/<int:pk>/', views.MutualFundDetailView.as_view(), name='portfolioMFDetail'),
    path('mutual-funds-edit/<int:pk>/', views.mf_edit, name='portfolioMFEdit'),
    path('mutual-funds-delete/<int:pk>/', views.mf_delete, name='portfolioMFDelete'),
    path('sips/', views.SIPIndexView.as_view(), name='sipIndex'),
    path('sips-create/', views.sip_create, name='sipCreate'),
    path('sips-edit/<int:pk>/', views.sip_edit, name='sipEdit'),
    path('sips-view/<int:pk>/', views.MutualFundSIPDetailView.as_view(), name='sipDetail'),
]