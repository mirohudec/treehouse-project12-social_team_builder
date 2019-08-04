from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView

from project import models
from project.models import Applicant


class HomeView(ListView):
    template_name = 'social_team_builder/index.html'
    model = models.Positions

    def get_queryset(self):
        # user is searching
        if 'search' in self.request.GET:
            search = self.request.GET['search']
            pos_name = Q(name__icontains=search)
            pos_desc = Q(description__icontains=search)
            project_name = Q(project__name__icontains=search)
            project_desc = Q(project__description__icontains=search)
            accepted = Q(accepted=False)
            return self.model.objects.filter(
                (pos_name |
                 pos_desc |
                 project_name |
                 project_desc) &
                accepted
            ).all()
        # user is using filter for my skills
        elif 'position' in self.request.GET:
            position = self.request.GET['position']
            if position == 'all':
                return self.model.objects.filter(accepted=False).all()
            if position == 'myskills':
                if self.request.user.is_authenticated:
                    skills = list(models.Skill.objects.filter(
                        user=self.request.user).all().values_list('name'))
                    pos_queryset = self.model.objects.filter(
                        accepted=False).all().values_list('name')
                    positions = list(pos_queryset)
                    # find the common value between skills and position 
                    # to offer position based on user skills
                    intersection = []
                    for skill in skills:
                        for position in positions:
                            if skill[0].lower() in position[0].lower():
                                intersection.append(position[0])
                    return self.model.objects.filter(
                        name__in=intersection).all()
            # user is using filter in home page
            else:
                return self.model.objects.filter(name=position).all()
        else:
            # basic home page with all open positions
            return self.model.objects.filter(accepted=False).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['applications'] = Applicant.objects.filter(
            position__accepted=False).all()
        if 'search' in self.request.GET:
            data['search'] = self.request.GET['search']
        if 'position' in self.request.GET:
            data['position'] = self.request.GET['position']
        else:
            data['position'] = 'all'
        data['positions'] = self.model.objects.filter(accepted=False).all()
        return data
