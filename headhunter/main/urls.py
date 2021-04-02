from django.urls import path
from django.contrib.flatpages import views as flat_views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', flat_views.flatpage, {'url': '/about/'}, name='about'),
    path('contact/', flat_views.flatpage,
         {'url': '/contact/'}, name='contact'),
]

urlpatterns += [
    path('applicant/', views.ApplicantListView.as_view(), name='applicant'),
    path('applicant/<int:pk>', views.ApplicantDetailView.as_view(),
         name='applicant-detail'),
    path('vacancy/', views.VacancyListView.as_view(), name='vacancy'),
    path('technology/', views.TechnologyListView.as_view(), name='technology'),
]

urlpatterns += [
    path('profile/<int:pk>', views.ProfileForm.as_view(), name='profile'),
]
