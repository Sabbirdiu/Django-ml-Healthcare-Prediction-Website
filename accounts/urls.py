from django.urls import path
from .views import *


urlpatterns = [
    path('patient/register', RegisterPatientView.as_view(), name='patient-register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('doctor/register', RegisterDoctorView.as_view(), name='doctor-register'),
    
    
]