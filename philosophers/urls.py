from django.urls import path
from . import views

urlpatterns = [
    path('', views.dining_philosophers, name='dining_philosophers'),
    path('start/', views.start_simulation, name='start_simulation'),
    path('stop/', views.stop_simulation, name='stop_simulation'),
    path('log/', views.get_event_log, name='get_event_log'),
    path('animated_version/', views.animated_version, name='animated_version'),
]

"""
URL patterns for the philosophers app.

This module defines the URL patterns for the philosophers app in the Django project.
Each URL pattern is associated with a specific view function.

- The empty path ('') maps to the dining_philosophers view function.
- The 'start/' path maps to the start_simulation view function.
- The 'stop/' path maps to the stop_simulation view function.
- The 'log/' path maps to the get_event_log view function.
- The 'animated_version/' path maps to the animated_version view function.
"""
