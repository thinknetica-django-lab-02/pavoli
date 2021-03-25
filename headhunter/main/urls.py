from django.urls import path
from django.contrib.flatpages import views as flat_views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', flat_views.flatpage, {'url': '/about/'}, name='about'),
    path('contact/', flat_views.flatpage, {'url': '/contact/'}, name='contact'),
]