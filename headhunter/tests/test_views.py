import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_view_applicant(client):
    url = reverse('applicant')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_applicant_detail(client):
    url = reverse('applicant-detail', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_vacancy(client):
    url = reverse('vacancy')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_vacancy_detail(client):
    url = reverse('vacancy-detail', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_technology(client):
    url = reverse('technology')
    response = client.get(url)
    assert response.status_code == 200
