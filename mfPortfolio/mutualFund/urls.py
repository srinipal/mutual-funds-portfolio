from django.urls import path

from . import views

urlpatterns = [
        path('mutual-funds-create/', views.mf_create, name='mfCreate'),
        path('mutual-funds-edit/<int:pk>/', views.mf_edit, name='mfEdit'),
        path('mutual-funds-view/<int:pk>/', views.MutualFundDetailView.as_view(), name='mfDetail'),
        path('mutual-funds/', views.IndexView.as_view(), name='mfIndex'),
        path('scrape/', views.mf_scrape, name='mfScrape')
    ]
