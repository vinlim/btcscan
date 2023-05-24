"""
URL configuration for exporer app.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.index, name='explorer_index'),
    path('tx/<str:tx_hash>/', views.view, name='explorer_view'),
    path('tx_search/', views.search, name='explorer_search'),
    path('api/estimate', api.estimate, name='api_estimator')
]
