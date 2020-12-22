from django.urls import path
from .views import *


urlpatterns = [
    path('patient/register', RegisterPatientView.as_view(), name='patient-register'),
    
    
]