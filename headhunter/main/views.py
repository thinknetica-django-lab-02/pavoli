from django.contrib.auth.models import User
from django.contrib import messages
from django.http.response import (
    HttpResponseRedirect,
)
from django.shortcuts import redirect, render, reverse
from django.views.generic import (
    ListView, DetailView, UpdateView, CreateView,
)
from .forms import *
from .models import *


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


class ProfileCreate(CreateView):
    """Создание профиля пользователя"""
    model = Profile
    form_class = ProfileForm
    # success_url = 'accounts/profile/'

    def get_initial(self):
        # этод метод я оставил только при создании так как связку User-Profile надо устанавливать
        # только при создании профиля, при редактировании профиля она уже будет и заново устанавливать не надо
        initial = super(ProfileCreate, self).get_initial()
        initial['user'] = self.request.user.id
        return initial


class UserProfileUpdate(UpdateView):
    """Редактирование данных пользователя и профиля."""

    model = User
    form_class = UserForm
    template_name = 'accounts/profile/profile_form.html'
    # success_url = 'accounts/profile/'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('profile', kwargs={'pk': pk})

    def get_object(self, request):
        """Получение пользователя из request."""
        return request.user

    def get_context_data(self, **kwargs):
        """Добавление в контекст дополнительной формы"""
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileFormSet(
            instance=self.get_object(kwargs['request']))
        return context

    def get(self, request, *args, **kwargs):
        """Метод обрабатывающий GET запрос.
        Переопределяется только из-за self.get_object(request)
        """
        self.object = self.get_object(request)
        return self.render_to_response(self.get_context_data(request=request))

    def form_valid_formset(self, form, formset):
        """Валидация вложенной формы и сохранение обеих форм."""
        if formset.is_valid():
            formset.save(commit=False)
            formset.save()
        else:
            return HttpResponseRedirect(self.get_success_url())
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        """Метод обрабатывающий POST запрос.
        Здесь происходит валидация основной формы и создание инстанса формы данным POST запроса
        """
        self.object = self.get_object(request)
        form = self.get_form()
        profile_form = ProfileFormSet(
            self.request.POST, self.request.FILES, instance=self.object)
        if form.is_valid():
            return self.form_valid_formset(form, profile_form)
        else:
            return self.form_invalid(form)


def create_vacancy(request, employer_id):
    employer = Employer.objects.get(id=employer_id)
    formset = vacancy_formset(
        queryset=Vacancy.objects.none(), instance=employer)

    if request.method == 'POST':
        formset = vacancy_formset(request.POST, instance=employer)

        if formset.is_valid():
            formset.save()

            return redirect('/')

    context = {'formset': formset, }
    return render(request, 'accounts/vacancy_form.html', context)


def update_vacancy(request, id):
    vacancy = Vacancy.objects.get(id=id)
    form = VacancyForm(instance=vacancy)

    if request.method == 'POST':
        form = VacancyForm(request.POST, instance=vacancy)

        if form.is_valid():
            form.save()
            return redirect('.')

    context = {'formset': form}
    return render(request, 'accounts/vacancy_form.html', context)
