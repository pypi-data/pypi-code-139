from django.urls import path
from . import views


urlpattents = [
    path('admin/login/<uuid:token>/', views.AdminProtectView.as_view(), name="django_admin_protect_login_token"),
    path('admin/login/', views.AdminProtectView.as_view(), name="django_admin_protect_login"),
]