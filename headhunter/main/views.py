from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import UpdateView


from .models import Applicant, Employer, Technology, Vacancy, Profile

# Create your views here.


def index(request):
    context = {
        'turn_on_block': True,
    }
    return render(request, 'index.html', context=context)


class ApplicantListView(generic.ListView):
    model = Applicant
    paginate_by = 10

    context_object_name = 'applicant_list'
    queryset = Applicant.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.request.GET.get('tag')
        context['tag'] = tag
        if tag is not None:
            context['tag_url'] = f'tag={tag}'
        else:
            context['tag_url'] = ''
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag = self.request.GET.get('tag')

        if tag:
            return queryset.filter(skill=tag)
        return queryset


class ApplicantDetailView(generic.DetailView):
    model = Applicant
    paginate_by = 10

    def applicant_detail_view(request, primary_key):
        applicant = get_object_or_404(Applicant, pk=primary_key)

        return render(request, 'main/applicant_detail.html', context={'applicant': applicant})


class TechnologyListView(generic.ListView):
    model = Technology
    paginate_by = 10

    context_object_name = 'technology_list'
    queryset = Technology.objects.all().order_by('name')


class VacancyListView(generic.ListView):
    model = Vacancy
    paginate_by = 10

    context_object_name = 'vacancy_list'
    queryset = Vacancy.objects.all()


class ProfileForm(UpdateView):
    model = Profile
    template_name_suffix = '_update_form'
