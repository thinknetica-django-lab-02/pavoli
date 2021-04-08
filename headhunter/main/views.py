from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import (ListView, DetailView, UpdateView, FormView)
from django.shortcuts import render, get_object_or_404
from .forms import (UserForm, ProfileFormset)
from .models import Applicant, Employer, Technology, Vacancy, Profile, User

# Create your views here.


def index(request):
    context = {
        'turn_on_block': True,
    }
    return render(request, 'index.html', context=context)


class ApplicantListView(ListView):
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


class ApplicantDetailView(DetailView):
    model = Applicant
    paginate_by = 10

    def applicant_detail_view(request, primary_key):
        applicant = get_object_or_404(Applicant, pk=primary_key)

        return render(request, 'main/applicant_detail.html', context={'applicant': applicant})


class TechnologyListView(ListView):
    model = Technology
    paginate_by = 10

    context_object_name = 'technology_list'
    queryset = Technology.objects.all().order_by('name')


class VacancyListView(ListView):
    model = Vacancy
    paginate_by = 10

    context_object_name = 'vacancy_list'
    queryset = Vacancy.objects.all()


class ProfileUpdate(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'accounts/profile/profile_update_form.html'

    def get_success_url(self):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
        else:
            pk = 'demo'
        return reverse('profile', kwargs={'pk': pk})

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs['pk'])


'''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileFormset(
            instance=self.get_object(kwargs['request']))
        return context

    def get_object(self, request):
        return request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileFormset(
            instance=self.get_object(kwargs['request']))
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(request)
        return self.render_to_response(self.get_context_data(request=request))

    def form_valid_formset(self, form, formset):
        if formset.is_valid():
            formset.save(commit=False)
            formset.save()
        else:
            return HttpResponseRedirect(self.get_success_url())
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(request)
        form = self.get_form()
        profile_form = ProfileFormset(
            self.request.POST, self.request.FILES, instance=self.object)
        if form.is_valid():
            return self.form_valid_formset(form, profile_form)
        else:
            return self.form_invalid(form)
'''
