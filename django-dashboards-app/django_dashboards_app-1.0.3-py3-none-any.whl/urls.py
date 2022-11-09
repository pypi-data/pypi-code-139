
from django.urls import path
from django.views.generic import RedirectView
from django.conf import settings

from django_dashboards_app import views


urlpatterns = [
    
    path('', RedirectView.as_view(url=settings.DASHBOARD_REDIRECT)),
    path('apps/', views.apps, name='apps'),
]