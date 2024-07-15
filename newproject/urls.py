from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="index.html")),
    path('prodcon/', include('prodcon.urls')),
    path('philosophers/', include('philosophers.urls')),
    path('readers_writers/', include('readers_writers.urls')),
]
