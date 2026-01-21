from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'students'

urlpatterns = [
    path('', RedirectView.as_view(url='register/', permanent=False), name='home'),
    path('register/', views.register_student, name='register_student'),
    path('success/', views.registration_success, name='registration_success'),
]

