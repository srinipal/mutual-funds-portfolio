from django.urls import path

from . import views

urlpatterns = [
    path('mutual-funds/', views.IndexView.as_view(), name='mfIndex'),
    path('mutual-funds-create/', views.mf_create, name='mfCreate'),
    path('mutual-funds-view/<int:pk>/', views.MutualFundDetailView.as_view(), name='mfDetail'),
    path('mutual-funds-edit/<int:pk>/', views.mf_edit, name='mfEdit'),
    path('mutual-funds-delete/<int:pk>/', views.mf_delete, name='mfDelete'),
    path('sips/', views.SIPIndexView.as_view(), name='sipIndex'),
    path('sips-create/', views.sip_create, name='sipCreate'),
    path('sips-edit/<int:pk>/', views.sip_edit, name='sipEdit'),
    path('sips-view/<int:pk>/', views.MutualFundSIPDetailView.as_view(), name='sipDetail'),
]