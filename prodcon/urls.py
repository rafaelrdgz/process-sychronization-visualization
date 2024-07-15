from django.urls import path
from . import views

urlpatterns = [
    path('', views.prodcon, name='prodcon'),
    path('start/', views.start_prodcon, name='start_prodcon'),
    path('stop/', views.stop_prodcon, name='stop_prodcon'),
    path('log/', views.get_and_clear_list, name='get_and_clear_list'),
    path('animated_version/', views.animated_version, name='animated_version'),
]

"""
URL patterns for the prodcon app.

This module defines the URL patterns for the prodcon app. It includes the following patterns:
- '' (empty string): Maps to the prodcon view.
- 'start/': Maps to the start_prodcon view.
- 'stop/': Maps to the stop_prodcon view.
- 'log/': Maps to the get_and_clear_list view.
- 'animated_version/': Maps to the animated_version view.
"""
