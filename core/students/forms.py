from django import forms
from .models import Student
from .encryption import hash_for_comparison, decrypt_data


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
        Validate mobile number format and check for duplicates using hash comparison.
        """
        mobile = self.cleaned_data.get('mobile')
        if mobile:
            # Normalize mobile: remove non-digit characters for comparison
            digits_only = ''.join(filter(str.isdigit, mobile))
            if len(digits_only) < 10:
                raise forms.ValidationError("Mobile number must contain at least 10 digits.")
            
            # Check for duplicate using hash-based comparison
            mobile_hash = hash_for_comparison(digits_only)
            
            # Check all existing students by decrypting and comparing hashes
            existing_students = Student.objects.all()
            for student in existing_students:
                try:
                    existing_mobile = decrypt_data(student.mobile)
                    existing_digits = ''.join(filter(str.isdigit, existing_mobile))
                    existing_hash = hash_for_comparison(existing_digits)
                    
                    if existing_hash == mobile_hash:
                        raise forms.ValidationError(
                            "This mobile number is already registered. Please use a different mobile number."
                        )
                except forms.ValidationError:
                    # Re-raise ValidationError (don't catch it)
                    raise
                except (ValueError, Exception) as e:
                    # Only skip if decryption fails (not ValidationError)
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f"Error decrypting mobile for student {student.id}: {str(e)}")
                    continue
        
        return mobile
    
    def clean_email(self):
        """
        Validate email and check for duplicates using hash-based comparison.
        """
        email = self.cleaned_data.get('email')
        if email:
            # Normalize email: lowercase and strip
            normalized_email = email.lower().strip()
            
            # Check for duplicate using hash-based comparison
            email_hash = hash_for_comparison(normalized_email)
            
            # Check all existing students by decrypting and comparing hashes
            existing_students = Student.objects.all()
            for student in existing_students:
                try:
                    existing_email = decrypt_data(student.email)
                    existing_normalized = existing_email.lower().strip()
                    existing_hash = hash_for_comparison(existing_normalized)
                    
                    if existing_hash == email_hash:
                        raise forms.ValidationError(
                            "This email address is already registered. Please use a different email address or contact support if you believe this is an error."
                        )
                except forms.ValidationError:
                    # Re-raise ValidationError (don't catch it)
                    raise
                except (ValueError, Exception) as e:
                    # Only skip if decryption fails (not ValidationError)
                    # Log the error for debugging
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f"Error decrypting email for student {student.id}: {str(e)}")
                    continue
        
        return email.lower().strip() if email else email
    
    def clean(self):
        """
        Cross-field validation: ensure email and mobile are not both duplicates of the same record.
        """
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        mobile = cleaned_data.get('mobile')
        
        if email and mobile:
            # Additional check: if both email and mobile match the same student
            email_hash = hash_for_comparison(email.lower().strip())
            mobile_digits = ''.join(filter(str.isdigit, mobile))
            mobile_hash = hash_for_comparison(mobile_digits)
            
            existing_students = Student.objects.all()
            for student in existing_students:
                try:
                    existing_email = decrypt_data(student.email)
                    existing_mobile = decrypt_data(student.mobile)
                    
                    existing_email_hash = hash_for_comparison(existing_email.lower().strip())
                    existing_mobile_digits = ''.join(filter(str.isdigit, existing_mobile))
                    existing_mobile_hash = hash_for_comparison(existing_mobile_digits)
                    
                    # If both email and mobile match the same student
                    if existing_email_hash == email_hash and existing_mobile_hash == mobile_hash:
                        raise forms.ValidationError(
                            "A registration with this email and mobile number combination already exists. "
                            "Please use different contact information or contact support."
                        )
                except forms.ValidationError:
                    # Re-raise ValidationError (don't catch it)
                    raise
                except (ValueError, Exception) as e:
                    # Only skip if decryption fails (not ValidationError)
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f"Error decrypting data for student {student.id}: {str(e)}")
                    continue
        
        return cleaned_data

