"""
URL configuration for exporer app.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='explorer.index'),
    path('tx/<str:tx_hash>/', views.view, name='explorer.view')
]
