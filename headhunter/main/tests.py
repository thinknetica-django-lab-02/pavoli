from django.test import TestCase, Client
from django.urls import reverse

from main.views import (Applicant, Vacancy, Employer)


# client = Client()


class ApplicantListViewTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_applicant(self):
        response = self.client.get(reverse('applicant'))
        self.assertEqual(response.status_code, 200)


class ApplicantDetailViewTests(TestCase):

    def setUp(self):
        self.client = Client()

    def create_candidate(self):
        Applicant(first_name='John', last_name='Doe',
                  birth_date='1984-02-19', gender='m').save()
        return Applicant.objects.get(last_name='Doe')

    def test_candidate_detail(self):
        a = self.create_candidate()
        url = reverse('applicant-detail', kwargs={'pk': a.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TechnologyListViewTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_skills(self):
        response = self.client.get(reverse('technology'))
        self.assertEqual(response.status_code, 200)


class VacancyListViewTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_vacancy(self):
        response = self.client.get(reverse('vacancy'))
        self.assertEqual(response.status_code, 200)


class VacancyDetailViewTests(TestCase):

    def setUp(self):
        self.client = Client()

    def create_vacancy(self):
        Employer(company_name='Apple').save()
        e = Employer.objects.get(company_name='Apple')
        Vacancy(company_name=e, vacancy_name='Python').save()
        return Vacancy.objects.get(vacancy_name='Python').id

    def test_vacancy_detail(self):
        pk = self.create_vacancy()
        url = reverse('vacancy-detail', kwargs={'pk': pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
