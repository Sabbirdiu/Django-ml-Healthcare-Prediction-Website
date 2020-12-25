from django.urls import path
from .views import *


urlpatterns = [
    path('',app),
    path('doctor/appointment/create', AppointmentCreateView.as_view(), name='doctor-appointment-create'),
    path('doctor/appointment/', AppointmentListView.as_view(), name='doctor-appointment'),
    path('Doctor/', DoctorPageView.as_view(), name='doctor'),
    path('patient-take-appointment/<pk>', TakeAppointmentView.as_view(), name='take-appointment'),
    path('patient/', PatientListView.as_view(), name='patient-list'),
    path('<pk>/patient/delete', PatientDeleteView.as_view(), name='delete-patient'),
    path('<pk>/delete/', AppointmentDeleteView.as_view(), name='delete-appointment'),
]