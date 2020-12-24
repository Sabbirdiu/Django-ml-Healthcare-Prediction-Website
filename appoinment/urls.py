from django.urls import path
from .views import *


urlpatterns = [
    path('',app),
    path('doctor/appointment/create', AppointmentCreateView.as_view(), name='doctor-appointment-create'),
    path('doctor/appointment/', AppointmentListView.as_view(), name='doctor-appointment'),
    path('Doctor/', DoctorPageView.as_view(), name='doctor'),
]