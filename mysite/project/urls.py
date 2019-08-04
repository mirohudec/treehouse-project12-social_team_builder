from django.urls import path

from . import views

app_name = 'project'

urlpatterns = [
    path('applications/', views.ApplicationsListView.as_view(),
         name='applications'),
    path('applications/apply/<int:id>', views.application_apply,
         name='applications_apply'),
    path('applications/accept/<int:id>/', views.application_accept,
         name='applications_accept'),
    path('applications/reject/<int:id>/', views.application_reject,
         name='applications_reject'),
    path('<username>/create/', views.ProjectCreateView.as_view(),
         name='project_create'),
    path('<username>/<slug>/', views.ProjectDetailView.as_view(),
         name='project_detail'),
    path('<username>/<slug>/edit/', views.ProjectEditView.as_view(),
         name='project_edit'),
    path('<username>/<slug>/delete/', views.ProjectDeleteView.as_view(),
         name='project_delete'),
]
