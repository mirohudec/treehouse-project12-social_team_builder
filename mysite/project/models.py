from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    timeline = models.CharField(max_length=255)
    requirements = models.CharField(max_length=255)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse_lazy('project:project_detail', kwargs={'username': self.created_by.username, 'slug': self.name})


class Positions(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    accepted = models.BooleanField(blank=True, default=False)
    time = models.CharField(max_length=255)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)


class Applicant(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    position = models.ForeignKey(Positions, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='UNDECIDED')


class Skill(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class MyProject(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
