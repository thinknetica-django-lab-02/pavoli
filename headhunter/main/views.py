from django.shortcuts import render, get_object_or_404
from django.views import generic


from .models import Applicant, Employer, Technology, Vacancy

# Create your views here.


def index(request):
    context = {
        'turn_on_block': True,
    }
    return render(request, 'index.html', context=context)


class ApplicantListView(generic.ListView):
    model = Applicant

    context_object_name = 'applicant_list'
    queryset = Applicant.objects.all()


class ApplicantDetailView(generic.DetailView):
    model = Applicant

    def applicant_detail_view(request, primary_key):
        applicant = get_object_or_404(Applicant, pk=primary_key)

        return render(request, 'main/applicant_detail.html', context={'applicant': applicant})


class TechnologyListView(generic.ListView):
    model = Technology

    context_object_name = 'technology_list'
    queryset = Technology.objects.all()


class VacancyListView(generic.ListView):
    model = Vacancy

    context_object_name = 'vacancy_list'
    queryset = Vacancy.objects.all()
