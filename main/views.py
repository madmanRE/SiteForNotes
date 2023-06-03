from django.shortcuts import render
from .forms import *
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.urls import reverse
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from .serializers import NoteSerializer
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'importance']
    basename = 'Note'


def index(request):
    context = {}
    context['themes'] = Theme.objects.all()
    return render(request, 'main/index.html', context=context)


class RegisterView(View):
    def get(self, request):
        form = RegisterForm
        return render(request, 'main/register.html', {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = User.objects.create_user(username=username)
                user.set_password(password)
                user.save()
                login(request, user)
                profile = Profile.objects.create(
                    user=user,
                    username=username,
                )
                profile.save()
                return redirect("/")
            except IntegrityError:
                form.add_error("login", "Пользователь с таким логином уже существует")

        return render(request, "main/register.html", {"form": form})


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "main/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.request.user.profile.pk)
        context['button_value'] = "Обновить профиль"
        context['themes'] = Theme.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy("main:index")


class ListNotes(ListView):
    template_name = 'main/list-notes.html'
    context_object_name = 'notes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['themes'] = Theme.objects.all()
        return context

    def get_queryset(self):
        theme_params = self.request.GET.get('theme')
        if theme_params:
            return Note.objects.filter(author=self.request.user.profile, is_active=True, theme__title=theme_params)
        else:
            return Note.objects.filter(author=self.request.user.profile, is_active=True)


class CreateNote(CreateView):
    template_name = 'main/create-note.html'
    form_class = NoteForm

    def get_success_url(self):
        return reverse('main:list_notes', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_value'] = "Создать"
        context['themes'] = Theme.objects.all()
        return context

    def form_valid(self, form):
        note = form.save(commit=False)
        note.author = self.request.user.profile
        note.save()
        return super().form_valid(form)


class UpdateNote(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "main/create-note.html"

    def get_success_url(self):
        return reverse('main:list_notes', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_value'] = "Обновить"
        context['themes'] = Theme.objects.all()
        return context


class DeleteNote(DeleteView):
    model = Note
    template_name = "main/create-note.html"

    def get_success_url(self):
        return reverse('main:list_notes', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_value'] = "Удалить"
        context['themes'] = Theme.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())
