from django.urls import reverse

from main.views import (Applicant, Employer, Vacancy,)

import pytest


@pytest.mark.django_db
def test_view_applicant(client):
    url = reverse('applicant')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_applicant_detail(client):

    def create_candidate():
        Applicant(first_name='John', last_name='Doe',
                  birth_date='1984-02-19', gender='m').save()
        return Applicant.objects.get(last_name='Doe')

    a = create_candidate()
    url = reverse('applicant-detail', kwargs={'pk': a.id})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_vacancy(client):
    url = reverse('vacancy')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_vacancy_detail(client):

    def create_vacancy():
        Employer(company_name='Apple').save()
        e = Employer.objects.get(company_name='Apple')
        Vacancy(company_name=e, vacancy_name='Python').save()
        return Vacancy.objects.get(vacancy_name='Python')

    v = create_vacancy()
    url = reverse('vacancy-detail', kwargs={'pk': v.id})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_technology(client):
    url = reverse('technology')
    response = client.get(url)
    assert response.status_code == 200
