from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile_home'),
    path('profile/edit', views.EditProfileView.as_view(),
         name='profile_edit'),
    path('profile/view/<username>', views.ViewProfileView.as_view(),
         name='profile_view'),
]
