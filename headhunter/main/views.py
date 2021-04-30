from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,)
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView,)

from .forms import (CreateNewUser, ProfileForm, ProfileFormSet,
                    UserForm, VacancyAddForm, VacancyUpdateForm,)
from .models import Applicant, Profile, Technology, Vacancy


# Create your views here.


def index(request: HttpRequest) -> HttpResponse:
    context = {
        'turn_on_block': True,
    }
    return render(request, 'index.html', context=context)


class ApplicantListView(ListView):
    model = Applicant
    paginate_by = 10

    context_object_name = 'applicant_list'
    queryset = Applicant.objects.all()

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        tag = self.request.GET.get('tag')
        context['tag'] = tag
        if tag is not None:
            context['tag_url'] = f'tag={tag}'
        else:
            context['tag_url'] = ''
        return context

    def get_queryset(self) -> 'QuerySet[Applicant]':
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

        return render(request,
                      'main/applicant_detail.html',
                      context={'applicant': applicant})


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


class VacancyDetailView(DetailView):
    model = Vacancy
    paginate_by = 10

    def vacancy_detail_view(request, primary_key):
        vacancy = get_object_or_404(Vacancy, pk=primary_key)

        return render(request,
                      'main/vacancy_detail.html',
                      context={'vacancy': vacancy})

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        pk = context['vacancy']
        num_visits = cache.get(pk, 0)
        num_visits += 1
        cache.set(pk, num_visits)

        context['num_visits'] = num_visits

        return context


class ProfileCreate(LoginRequiredMixin, CreateView):
    """Создание профиля пользователя"""
    model = Profile
    form_class = ProfileForm
    # success_url = 'account/profile/'

    def get_initial(self) -> dict:
        # этод метод я оставил только при создании
        # так как связку User-Profile надо устанавливать
        # только при создании профиля, при редактировании профиля
        # она уже будет и заново устанавливать не надо
        initial = super(ProfileCreate, self).get_initial()
        initial['user'] = self.request.user.id
        return initial


class UserProfileUpdate(LoginRequiredMixin, UpdateView):
    """Редактирование данных пользователя и профиля."""

    model = User
    form_class = UserForm
    template_name = 'account/profile/profile_form.html'
    login_url = reverse_lazy('index')

    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        return reverse('profile', kwargs={'pk': pk})

    def get_object(self, request):
        """Получение пользователя из request."""
        return request.user

    def get_context_data(self, **kwargs) -> dict:
        """Добавление в контекст дополнительной формы"""
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileFormSet(
            instance=self.get_object(kwargs['request']))
        return context

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Метод обрабатывающий GET запрос.
        Переопределяется только из-за self.get_object(request)
        """
        self.object = self.get_object(request)
        return self.render_to_response(self.get_context_data(request=request))

    def form_valid_formset(self, form, formset) -> HttpResponse:
        """Валидация вложенной формы и сохранение обеих форм."""
        if formset.is_valid():
            formset.save(commit=False)
            formset.save()
        else:
            return HttpResponseRedirect(self.get_success_url())
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """
        Метод обрабатывающий POST запрос.
        Здесь происходит валидация основной формы и
        создание инстанса формы данным POST запроса
        """
        self.object = self.get_object(request)
        form = self.get_form()
        profile_form = ProfileFormSet(
            self.request.POST, self.request.FILES, instance=self.object)
        if form.is_valid():
            return self.form_valid_formset(form, profile_form)
        else:
            return self.form_invalid(form)


class VacancyAddView(PermissionRequiredMixin, CreateView):

    def has_permission(self) -> bool:
        return self.request.user.groups.filter(name='sellers').exists()

    model = Vacancy
    form_class = VacancyAddForm
    success_url = reverse_lazy('vacancy')


class VacancyUpdateView(PermissionRequiredMixin, UpdateView):

    def has_permission(self) -> bool:
        return self.request.user.groups.filter(name='sellers').exists()

    model = Vacancy
    form_class = VacancyUpdateForm
    template_name_suffix = '_form_update'
    success_url = reverse_lazy('vacancy')


class RegisterUser(CreateView):
    form_class = CreateNewUser
    template_name = 'main/register.html'

    def form_valid(self, form) -> HttpResponse:
        user = form.save()
        login(self.request,
              user,
              backend='django.contrib.auth.backends.ModelBackend')
        return redirect('index')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'main/login.html'
