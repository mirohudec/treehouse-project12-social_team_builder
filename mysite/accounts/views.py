from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import (
    TemplateView, FormView, UpdateView, DetailView)

from . import forms
from . import models
from project.models import Positions, Skill, MyProject


class ProfileView(DetailView):
    template_name = 'accounts/profile.html'
    model = models.User

    def get_object(self, queryset=None):
        return self.model.objects.get(email=self.request.user.email)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['positions'] = Positions.objects.all().filter(
            user=self.object, accepted=True)
        data['skills'] = Skill.objects.all().filter(
            user=self.object)
        data['my_projects'] = MyProject.objects.all().filter(
            user=self.object)
        return data


class ViewProfileView(DetailView):
    template_name = 'accounts/profile.html'
    model = models.User

    def get_object(self, queryset=None):
        # get slug from path
        path = self.request.path
        username = path.replace('/profile/view/', '')
        return self.model.objects.get(username=username)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['positions'] = Positions.objects.all().filter(
            user=self.object, accepted=True)
        data['skills'] = Skill.objects.all().filter(
            user=self.object)
        data['my_projects'] = MyProject.objects.all().filter(
            user=self.object)
        return data


class EditProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/edit_profile.html'
    form_class = forms.ProfileForm
    model = models.User

    def get_object(self, queryset=None):
        return self.model.objects.get(email=self.request.user.email)

    def get_success_url(self):
        return reverse_lazy('social_team_builder:home')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['user'] = self.request.user
        if self.request.POST:
            data['skills'] = forms.SkillFormSet(
                self.request.POST, instance=self.object)
            data['my_projects'] = forms.MyProjectFormSet(
                self.request.POST, instance=self.object)
        else:
            data['skills'] = forms.SkillFormSet(
                instance=self.object)
            data['my_projects'] = forms.MyProjectFormSet(
                instance=self.object)
        data['positions'] = Positions.objects.all().filter(
            user=self.request.user, accepted=True)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        skills = context['skills']
        my_projects = context['my_projects']
        if skills.is_valid():
            skills.instance = self.object
            skills.save()
        if my_projects.is_valid():
            my_projects.instance = self.object
            my_projects.save()
        return super().form_valid(form)
