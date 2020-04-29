from django.urls import path

from . import views

urlpatterns = [
        path('mutual-funds-create/', views.mf_create, name='mfCreate'),
        path('mutual-funds-view/<int:pk>/', views.MutualFundDetailView.as_view(), name='mfDetail')
    ]