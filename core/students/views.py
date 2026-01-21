from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .forms import StudentRegistrationForm
from .encryption import encrypt_data, decrypt_data


def register_student(request):
    """
    Handle student registration with encryption for email and mobile.
    """
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Get cleaned form data
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                mobile = form.cleaned_data['mobile']
                student_class = form.cleaned_data.get('student_class', '')
                
                # Encrypt sensitive data
                encrypted_email = encrypt_data(email)
                encrypted_mobile = encrypt_data(mobile)
                
                # Insert into database using raw SQL (since managed=False)
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO student (name, email, mobile, student_class, created, modified)
                        VALUES (%s, %s, %s, %s, NOW(), NOW())
                        """,
                        [name, encrypted_email, encrypted_mobile, student_class]
                    )
                    # Get the generated ID
                    registration_id = cursor.lastrowid
                
                # Decrypt email for sending confirmation
                decrypted_email = email  # We already have it from form
                
                # Store in session for email sending
                request.session['registration_id'] = registration_id
                request.session['student_email'] = decrypted_email
                request.session['student_name'] = name
                request.session['student_class'] = student_class
                
                messages.success(request, f'Registration successful! Your Registration ID is: {registration_id}')
                return redirect('students:registration_success')
                
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
                return render(request, 'students/register.html', {'form': form})
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'students/register.html', {'form': form})


def registration_success(request):
    """
    Display success page and trigger email sending.
    """
    registration_id = request.session.get('registration_id')
    student_email = request.session.get('student_email')
    student_name = request.session.get('student_name')
    student_class = request.session.get('student_class', '')
    
    if not registration_id:
        messages.error(request, 'No registration found.')
        return redirect('students:register_student')
    
    # Send confirmation email with decrypted email and registration ID
    email_sent = False
    email_error = None
    try:
        # Render email template
        email_html = render_to_string(
            'students/emails/registration_confirmation.html',
            {
                'student_name': student_name,
                'student_email': student_email,
                'student_class': student_class,
                'registration_id': registration_id,
            }
        )
        
        # Send email
        send_mail(
            subject=f'Registration Confirmation - ID: {registration_id}',
            message=f'Dear {student_name},\n\nYour registration has been completed successfully.\n\nRegistration ID: {registration_id}\n\nThank you!',
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@edtech.com'),
            recipient_list=[student_email],
            html_message=email_html,
            fail_silently=False,
        )
        email_sent = True
        messages.info(request, 'Confirmation email has been sent! Check your console/terminal for the email output.')
    except Exception as e:
        # Log error but don't fail the registration
        email_error = str(e)
        messages.warning(request, f'Registration successful! Note: Email could not be sent. Check console for details.')
        print(f"Email Error: {email_error}")  # Print to console for debugging
    
    context = {
        'registration_id': registration_id,
        'student_email': student_email,
        'student_name': student_name,
        'email_sent': email_sent,
        'email_error': email_error,
    }
    
    # Clear session data
    request.session.pop('registration_id', None)
    request.session.pop('student_email', None)
    request.session.pop('student_name', None)
    request.session.pop('student_class', None)
    
    return render(request, 'students/success.html', context)
