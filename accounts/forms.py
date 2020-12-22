from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'))


class PatientRegistrationForm(UserCreationForm):
  

    def __init__(self, *args, **kwargs):
        super(PatientRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['gender'].required = True
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['email'].label = "Email"
        self.fields['phone_number'].label = "Phone Number"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

        # self.fields['gender'].widget = forms.CheckboxInput()

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['phone_number'].widget.attrs.update(
            {
                'placeholder': 'Enter Phone Number',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )

    class Meta:
        model = User

        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2', 'gender' ]
        error_messages = {
            'first_name': {
                'required': 'First name is required',
                'max_length': 'Name is too long'
            },
            'last_name': {
                'required': 'Last name is required',
                'max_length': 'Last Name is too long'
            },
            'gender': {
                'required': 'Gender is required'
            }
        }

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.role = "patient"
        if commit:
            user.save()
        return user


