from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from accounts.models import User
from django.views.generic import CreateView,ListView,DeleteView

from .forms import CreateAppointmentForm,TakeAppointmentForm
from .models import Appointment,TakeAppointment
from accounts.decorators import  user_is_doctor,user_is_doctor

def app(request):
    return render(request,'b1.html')


class AppointmentCreateView(CreateView):
    template_name = 'appointment/appointment_create.html'
    form_class = CreateAppointmentForm
    extra_context = {
        'title': 'Post New Appointment'
    }
    success_url = reverse_lazy('doctor-appointment')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('login')
        if self.request.user.is_authenticated and self.request.user.role != 'doctor':
            return reverse_lazy('login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AppointmentCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)    

class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointment/appointment.html'
    context_object_name = 'appointment'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    @method_decorator(user_is_doctor)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id).order_by('-id')            


class DoctorPageView(ListView):
    paginate_by = 9
    model = Appointment
    context_object_name = 'doctor'
    template_name = "doctor.html"

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')
class TakeAppointmentView(CreateView):
    template_name = 'appointment/take_appointment.html'
    form_class = TakeAppointmentForm
    extra_context = {
        'title': 'Take Appointment'
    }
    success_url = reverse_lazy('home')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('login')
        if self.request.user.is_authenticated and self.request.user.role != 'patient':
            return reverse_lazy('login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TakeAppointmentView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class PatientListView(ListView):
    model = TakeAppointment
    context_object_name = 'patients'
    template_name = "appointment/patient_list.html"

    def get_queryset(self):
        return self.model.objects.filter(appointment__user_id=self.request.user.id).order_by('-id')            


class PatientDeleteView(DeleteView):
    model = TakeAppointment
    success_url = reverse_lazy('patient-list')   
    template_name = "appointment/patient_delete.html"     

class AppointmentDeleteView(DeleteView):
  
    model = Appointment
    success_url = reverse_lazy('doctor-appointment')
    template_name = "appointment/appointment_delete.html" 
