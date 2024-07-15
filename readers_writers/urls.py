from django.urls import path
from . import views

urlpatterns = [
    path('', views.readers_writers, name='readers_writers'),
    path('start/', views.start_simulation, name='start_simulation'),
    path('stop/', views.stop_simulation, name='stop_simulation'),
    path('log/', views.get_event_log, name='get_event_log'),
]

"""
URL patterns for the readers_writers app.

This module defines the URL patterns for the readers_writers app in the Django project.

- The empty path ('') maps to the readers_writers view.
- The 'start/' path maps to the start_simulation view.
- The 'stop/' path maps to the stop_simulation view.
- The 'log/' path maps to the get_event_log view.

These URL patterns are used to route incoming requests to the appropriate views.
"""
