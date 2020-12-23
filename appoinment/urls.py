from django.urls import path
from .views import *


urlpatterns = [
    path('',app),
    path('doctor/appointment/create', AppointmentCreateView.as_view(), name='doctor-appointment-create'),
]