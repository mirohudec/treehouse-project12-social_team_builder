from django.urls import path

from . import views

app_name = 'social_team_builder'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home')
]
