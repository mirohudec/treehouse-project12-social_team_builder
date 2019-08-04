from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from django.forms import widgets
from django_summernote.widgets import SummernoteWidget
from django import forms
from . import models


class ProjectForm(forms.ModelForm):
    description = forms.CharField(
        widget=SummernoteWidget(), required=False)
    timeline = forms.CharField(widget=widgets.Textarea)
    requirements = forms.CharField(widget=widgets.Textarea)

    class Meta:
        model = models.Project
        fields = ('name', 'description', 'requirements', 'timeline')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = ""
        self.fields['name'].widget.attrs['placeholder'] = "Full Name"
        self.fields['name'].widget.attrs['class'] = 'circle--input--h1'
        self.fields['description'].label = ""
        self.fields['description'].widget.attrs['placeholder'] = "Tell us about yourself..."
        self.fields['description'].widget.attrs['class'] = 'circle--article--body'
        self.fields['requirements'].label = ""
        self.fields['requirements'].widget.attrs['placeholder'] = "Project description..."
        self.fields['requirements'].widget.attrs['class'] = 'circle--textarea--input'
        self.fields['timeline'].label = ""
        self.fields['timeline'].widget.attrs['placeholder'] = "Time estimate"
        self.fields['timeline'].widget.attrs['class'] = 'circle--textarea--input'


class PositionForm(forms.ModelForm):
    description = forms.CharField(
        widget=SummernoteWidget(
            attrs={'summernote': {'width': '100%', 'height': '200px'}}
        ), required=False)

    class Meta:
        model = models.Positions
        fields = ('name', 'description', 'time')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].label = ""
        self.fields['description'].widget.attrs['placeholder'] = "Position description..."
        self.fields['name'].label = ""
        self.fields['name'].widget.attrs['placeholder'] = "Position Title"
        self.fields['name'].widget.attrs['class'] = 'circle--input--h3'
        self.fields['time'].label = ""
        self.fields['time'].widget.attrs['placeholder'] = "Position time involvement..."
        self.fields['time'].widget.attrs['class'] = 'circle--input--h3'


PositionFormSet = inlineformset_factory(
    models.Project, models.Positions, form=PositionForm, extra=1)


class StatusForm(forms.Form):
    status = forms.ChoiceField(
        choices=(
            ('all', 'All Applicants'), ('new', 'New Applications'),
            ('accepted', 'Accepted'), ('rejected', 'Rejected')
        ), widget=forms.Select(
            attrs={'onchange': 'this.form.submit()'}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].label = ''


class MyProjectForm(forms.Form):
    projects = forms.ChoiceField(widget=forms.Select(
        attrs={'onchange': 'this.form.submit();'}), required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['projects'].label = ''
        self.fields['projects'].choices = [('all', 'All Projects')] + [(
            project.name, project.name) for project in models.Project.objects.filter(created_by=user).all()]


class NeedForm(forms.Form):
    needs = forms.ChoiceField(widget=forms.Select(
        attrs={'onchange': 'this.form.submit();'}), required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        project = kwargs.pop('project')
        super().__init__(*args, **kwargs)
        self.fields['needs'].label = ""
        self.fields['needs'].choices = [('all', 'All Needs')] + [(
            project.name, project.name) for project in models.Positions.objects.filter(user=user, project__name=project).all()]
