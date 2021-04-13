from django.urls import path
from django.contrib.flatpages import views as flat_views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', flat_views.flatpage, {'url': '/about/'}, name='about'),
    path('contact/', flat_views.flatpage,
         {'url': '/contact/'}, name='contact'),

    path('applicant/', views.ApplicantListView.as_view(), name='applicant'),
    path('applicant/<int:pk>', views.ApplicantDetailView.as_view(),
         name='applicant-detail'),

    path('vacancy/', views.VacancyListView.as_view(), name='vacancy'),
    path('vacancy/<int:pk>', views.VacancyDetailView.as_view(),
         name='vacancy-detail'),
    path('vacancy/add', views.VacancyAddView.as_view(), name='create_vacancy'),
    path('vacancy/<int:pk>/edit',
         views.VacancyUpdateView.as_view(), name='update_vacancy'),

    path('technology/', views.TechnologyListView.as_view(), name='technology'),


    path('profile/<int:pk>', views.UserProfileUpdate.as_view(), name='profile'),
    path('accounts/register', views.RegisterUser.as_view(), name='register'),
    path('accounts/login', views.LoginUser.as_view(), name='login'),
]
