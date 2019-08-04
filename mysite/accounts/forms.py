from django import forms
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from django_summernote import widgets

from project import models
from .models import User


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=widgets.SummernoteWidget(), required=False)

    class Meta:
        model = get_user_model()
        fields = ('username', 'bio', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ""
        self.fields['username'].widget.attrs['placeholder'] = "Full Name"
        self.fields['username'].widget.attrs['class'] = 'circle--input--h1'
        self.fields['bio'].label = ""
        self.fields['bio'].widget.attrs['placeholder'] = "Tell us about yourself..."
        self.fields['bio'].widget.attrs['class'] = 'circle--article--body'


class SkillForm(forms.ModelForm):

    class Meta:
        model = models.Skill
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = ""
        self.fields['name'].widget.attrs['placeholder'] = "Skills"


class MyProjectForm(forms.ModelForm):

    class Meta:
        model = models.MyProject
        fields = ('name', 'url',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = ""
        self.fields['name'].widget.attrs['placeholder'] = "Project Name"
        self.fields['url'].label = ""
        self.fields['url'].widget.attrs['placeholder'] = "Project URL"


SkillFormSet = inlineformset_factory(User, models.Skill, form=SkillForm,
                                     extra=1)

MyProjectFormSet = inlineformset_factory(User, models.MyProject,
                                         form=MyProjectForm, extra=1)
