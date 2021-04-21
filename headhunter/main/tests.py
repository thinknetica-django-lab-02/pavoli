from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser

from main.views import *


client = Client()


class ApplicantListViewTests(TestCase):

    def test_applicant(self):
        response = self.client.get(reverse('applicant'))
        self.assertEqual(response.status_code, 200)


class ApplicantDetailViewTests(TestCase):

    def test_candidate_detail(self):
        url = reverse('applicant-detail', args=[1, ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TechnologyListViewTests(TestCase):

    def test_skills(self):
        response = self.client.get(reverse('technology'))
        self.assertEqual(response.status_code, 200)


class VacancyListViewTests(TestCase):

    def test_vacancy(self):
        response = self.client.get(reverse('vacancy'))
        self.assertEqual(response.status_code, 200)


class VacancyDetailViewTests(TestCase):

    def test_vacancy_detail(self):
        url = reverse('vacancy-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
