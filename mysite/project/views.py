from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import (
    UpdateView, DetailView, DeleteView, CreateView, ListView)

from . import forms
from . import models
from project.models import Applicant, Positions
from django.contrib import messages


class ProjectDetailView(DetailView):
    template_name = 'project/home.html'
    model = models.Project

    def get_object(self):
        return self.model.objects.filter(
            created_by__username=self.kwargs.get('username'),
            name=self.kwargs.get('slug')).first()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['positions'] = models.Positions.objects.filter(
            project=self.object).all()
        return data


class ProjectEditView(UpdateView):
    template_name = 'project/edit.html'
    form_class = forms.ProjectForm
    model = models.Project

    def get_success_url(self):
        return reverse_lazy('project:project_detail',
                            kwargs={'username': self.request.user.username,
                                    'slug': self.object.name})

    def get_object(self):
        return self.model.objects.filter(created_by=self.request.user,
                                         name=self.kwargs.get('slug')).first()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['positions'] = forms.PositionFormSet(
                self.request.POST, instance=self.object)
        else:
            data['positions'] = forms.PositionFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        positions = context['positions']
        if positions.is_valid():
            positions.instance = self.object
            for position in positions:
                pos = position.save(commit=False)
                pos.user = self.request.user
            positions.save()
        return super().form_valid(form)


class ProjectCreateView(CreateView):
    template_name = 'project/edit.html'
    form_class = forms.ProjectForm
    model = models.Project

    def get_success_url(self):
        return reverse_lazy('project:project_detail',
                            kwargs={'username': self.request.user.username,
                                    'slug': self.object.name})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['positions'] = forms.PositionFormSet(
                self.request.POST, instance=self.object)
        else:
            data['positions'] = forms.PositionFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        positions = context['positions']
        form = context['form']
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.created_by = self.request.user
            self.object.save()
        if positions.is_valid():
            positions.instance = self.object
            for position in positions:
                pos = position.save(commit=False)
                pos.user = self.request.user
                pos.project = self.object
            positions.save()
        return redirect(self.get_success_url())


class ProjectDeleteView(DeleteView):
    model = models.Project
    template_name = 'project/project_confirm_delete.html'
    success_url = reverse_lazy('social_team_builder:home')

    def get_object(self):
        return self.model.objects.filter(created_by=self.request.user,
                                         name=self.kwargs.get('slug')).first()


class ApplicationsListView(ListView):
    template_name = 'project/applications.html'

    def get_queryset(self):
        model = Applicant
        if not model.objects.filter(
            position__project__created_by=self.request.user):
            return model.objects.none()
        if 'status' in self.request.GET:
            status = self.request.GET['status']
        else:
            status = 'all'
        if 'projects' in self.request.GET:
            project = self.request.GET['projects']
        else:
            project = 'all'
        if 'needs' in self.request.GET:
            needs = self.request.GET['needs']
        else:
            needs = 'all'
        if status == 'all':
            status_q = Q()
        elif status == 'new':
            status_q = Q(status='UNDECIDED')
        elif status == 'accepted':
            status_q = Q(status='ACCEPTED')
        elif status == 'rejected':
            status_q = Q(status='REJECTED')
        if project == 'all':
            project_q = Q()
        else:
            project_q = Q(position__project__name__iexact=project)

        positions = [pos.name for pos in models.Positions.objects.filter(
            project__name=project).all()]
        if needs == 'all':
            needs_q = Q()
        elif project == 'all':
            needs_q = Q()
        elif needs in positions:
            needs_q = Q(position__name__iexact=needs)
        else:
            needs_q = Q()

        return model.objects.filter(
            status_q & project_q & needs_q & Q(
                position__project__created_by=self.request.user)).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['status'] = forms.StatusForm(self.request.GET)
        data['project'] = forms.MyProjectForm(
            self.request.GET, user=self.request.user)
        if 'projects' in data['project'].data:
            data['needs'] = forms.NeedForm(
                self.request.GET,
                user=self.request.user,
                project=data['project'].data['projects'])
        else:
            data['needs'] = forms.NeedForm(
                self.request.GET,
                user=self.request.user,
                project='')
        return data


def application_accept(request, id):
    application = Applicant.objects.get(id=id)
    if request.user == application.position.project.created_by:
        application.status = 'ACCEPTED'
        application.save()
        position = models.Positions.objects.get(id=application.position.id)
        position.accepted = True
        position.user = application.user
        position.save()
        send_mail(
            'Application approved',
            f'You were accepted for position: {position.name}. ' +
            f'Contact {position.user.email} for more information.',
            'stb.project12@gmailcom',
            [f'{application.user.email}'],
            fail_silently=False
        )
        messages.success(request,
                         f'Email sent to accepted applicant: ' + 
                         f'{application.user.username}')
    else:
        raise PermissionDenied()
    return redirect(request.META.get('HTTP_REFERER'))


def application_reject(request, id):
    application = Applicant.objects.get(id=id)
    if request.user == application.position.project.created_by:
        application.status = 'REJECTED'
        application.save()
        send_mail(
            'Application rejected',
            f'You were rejected for position: {application.position.name}.' +
            f'Thanks for applying.',
            'stb.project12@gmailcom',
            [f'{application.user.email}'],
            fail_silently=False
        )
        messages.success(request,
                         f'Email sent to rejected applicant: ' + 
                         f'{application.user.username}')
    else:
        raise PermissionDenied()
    return redirect(request.META.get('HTTP_REFERER'))


def application_apply(request, id):
    position = Positions.objects.get(id=id)
    if position.accepted:
        raise Http404()
    try:
        Applicant.objects.get(
            user=request.user, position=position)
        messages.warning(request, f'You already applied to this position')
    except Applicant.DoesNotExist:
        Applicant.objects.create(
            status='UNDECIDED',
            user=request.user,
            position=position
        )
        messages.success(
            request, f'Successfully applied to the position of ' + 
            f'{position.name}')
    return redirect(request.META.get('HTTP_REFERER'))
