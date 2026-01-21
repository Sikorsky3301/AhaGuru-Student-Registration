from django import forms
from .models import Student


class StudentRegistrationForm(forms.Form):
    """
    Form for student registration with validation.
    """
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name'
        }),
        label='Full Name'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        }),
        label='Email Address'
    )
    
    mobile = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your mobile number'
        }),
        label='Mobile Number'
    )
    
    student_class = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your class (e.g., Grade 10, Class A)'
        }),
        label='Class'
    )
    
    def clean_mobile(self):
        """
        Validate mobile number format.
        """
        mobile = self.cleaned_data.get('mobile')
        if mobile:
            # Remove any non-digit characters for validation
            digits_only = ''.join(filter(str.isdigit, mobile))
            if len(digits_only) < 10:
                raise forms.ValidationError("Mobile number must contain at least 10 digits.")
        return mobile
    
    def clean_email(self):
        """
        Validate email and check for duplicates.
        """
        email = self.cleaned_data.get('email')
        if email:
            # Check if email already exists (decrypt and compare)
            from .encryption import encrypt_data
            encrypted_email = encrypt_data(email.lower())
            
            # Check if this encrypted email exists in database
            if Student.objects.filter(email=encrypted_email).exists():
                raise forms.ValidationError("This email is already registered.")
        
        return email.lower() if email else email

