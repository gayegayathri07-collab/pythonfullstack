from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('list/', views.StudentListView.as_view(), name='index'),
    path('location/', TemplateView.as_view(template_name='students/location.html'), name='location'),
    path('add-contact/', views.add_contact, name='add_contact'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('add/', views.StudentCreateView.as_view(), name='add_student'),
    path('<int:pk>/edit/', views.StudentUpdateView.as_view(), name='edit_student'),
    path('<int:pk>/delete/', views.StudentDeleteView.as_view(), name='delete_student'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='detail'),
]
