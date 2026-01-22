"""
Comprehensive test suite for Student Registration System

This test suite covers the complete flow of the application:
1. Encryption/Decryption functionality
2. Form validation (email, mobile, duplicates)
3. Complete registration flow
4. Duplicate prevention using hash-based comparison
5. Database operations
6. Email sending functionality

Run tests with: python manage.py test students
"""

from django.test import TestCase, Client, TransactionTestCase
from django.contrib.messages import get_messages
from django.db import connection
from django.core import mail
from django.urls import reverse
from unittest.mock import patch, MagicMock

from .models import Student
from .forms import StudentRegistrationForm
from .encryption import encrypt_data, decrypt_data, hash_for_comparison


def create_student_table():
    """Helper function to create student table in test database"""
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARBINARY(255) NOT NULL,
                mobile VARBINARY(255) NOT NULL,
                student_class VARCHAR(100),
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)


class EncryptionTestCase(TestCase):
    """
    Test Case 1: Encryption and Decryption Functionality
    
    Tests the core encryption/decryption functions that secure
    email and mobile data in the database.
    """
    
    def setUp(self):
        """Set up test data"""
        self.test_email = "test@example.com"
        self.test_mobile = "1234567890"
    
    def test_encrypt_decrypt_email(self):
        """
        Test that email encryption and decryption work correctly.
        Flow: Plain email -> Encrypt -> Decrypt -> Original email
        """
        # Encrypt the email
        encrypted = encrypt_data(self.test_email)
        
        # Verify encryption produces bytes
        self.assertIsInstance(encrypted, bytes)
        self.assertNotEqual(encrypted, self.test_email.encode())
        
        # Decrypt the email
        decrypted = decrypt_data(encrypted)
        
        # Verify decryption returns original value
        self.assertEqual(decrypted, self.test_email)
    
    def test_encrypt_decrypt_mobile(self):
        """
        Test that mobile encryption and decryption work correctly.
        Flow: Plain mobile -> Encrypt -> Decrypt -> Original mobile
        """
        # Encrypt the mobile
        encrypted = encrypt_data(self.test_mobile)
        
        # Verify encryption produces bytes
        self.assertIsInstance(encrypted, bytes)
        
        # Decrypt the mobile
        decrypted = decrypt_data(encrypted)
        
        # Verify decryption returns original value
        self.assertEqual(decrypted, self.test_mobile)
    
    def test_hash_for_comparison(self):
        """
        Test hash-based comparison for duplicate detection.
        Same input should produce same hash, different inputs produce different hashes.
        """
        email1 = "test@example.com"
        email2 = "TEST@EXAMPLE.COM"  # Different case, should produce same hash
        email3 = "different@example.com"  # Different email
        
        hash1 = hash_for_comparison(email1)
        hash2 = hash_for_comparison(email2)
        hash3 = hash_for_comparison(email3)
        
        # Same email (different case) should produce same hash
        self.assertEqual(hash1, hash2)
        
        # Different emails should produce different hashes
        self.assertNotEqual(hash1, hash3)
        
        # Hash should be consistent (deterministic)
        self.assertEqual(hash_for_comparison(email1), hash1)


class FormValidationTestCase(TransactionTestCase):
    """
    Test Case 2: Form Validation
    
    Tests form validation including:
    - Required fields
    - Email format validation
    - Mobile number format validation
    - Duplicate detection
    """
    
    def setUp(self):
        """Set up test data and create a test student"""
        # Create student table
        create_student_table()
        # Create a test student in the database
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO student (name, email, mobile, student_class, created, modified)
                VALUES (%s, %s, %s, %s, NOW(), NOW())
                """,
                ['Existing Student', encrypt_data('existing@test.com'), encrypt_data('9876543210'), 'Grade 10']
            )
    
    def test_valid_form(self):
        """
        Test that a valid form passes validation.
        Flow: Valid data -> Form validation -> Form is valid
        """
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'mobile': '1234567890',
            'student_class': 'Grade 10'
        }
        form = StudentRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_required_fields(self):
        """
        Test that required fields are enforced.
        Flow: Missing required field -> Form validation -> Form is invalid
        """
        # Test missing name
        form = StudentRegistrationForm(data={
            'email': 'test@example.com',
            'mobile': '1234567890'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        
        # Test missing email
        form = StudentRegistrationForm(data={
            'name': 'John Doe',
            'mobile': '1234567890'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        
        # Test missing mobile
        form = StudentRegistrationForm(data={
            'name': 'John Doe',
            'email': 'test@example.com'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('mobile', form.errors)
    
    def test_email_format_validation(self):
        """
        Test email format validation.
        Flow: Invalid email -> Form validation -> Error message
        """
        form = StudentRegistrationForm(data={
            'name': 'John Doe',
            'email': 'invalid-email',
            'mobile': '1234567890'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_mobile_format_validation(self):
        """
        Test mobile number format validation.
        Flow: Invalid mobile (too short) -> Form validation -> Error message
        """
        form = StudentRegistrationForm(data={
            'name': 'John Doe',
            'email': 'test@example.com',
            'mobile': '123'  # Too short
        })
        self.assertFalse(form.is_valid())
        self.assertIn('mobile', form.errors)
    
    def test_duplicate_email_prevention(self):
        """
        Test duplicate email prevention using hash-based comparison.
        Flow: Duplicate email -> Form validation -> Error message
        """
        form = StudentRegistrationForm(data={
            'name': 'New Student',
            'email': 'existing@test.com',  # Same as existing student
            'mobile': '1111111111',
            'student_class': 'Grade 11'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('already registered', str(form.errors['email']))
    
    def test_duplicate_mobile_prevention(self):
        """
        Test duplicate mobile prevention using hash-based comparison.
        Flow: Duplicate mobile -> Form validation -> Error message
        """
        form = StudentRegistrationForm(data={
            'name': 'New Student',
            'email': 'new@test.com',
            'mobile': '9876543210',  # Same as existing student
            'student_class': 'Grade 11'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('mobile', form.errors)
        self.assertIn('already registered', str(form.errors['mobile']))
    
    def test_email_case_insensitive(self):
        """
        Test that email duplicate detection is case-insensitive.
        Flow: Same email (different case) -> Form validation -> Error message
        """
        form = StudentRegistrationForm(data={
            'name': 'New Student',
            'email': 'EXISTING@TEST.COM',  # Different case
            'mobile': '1111111111',
            'student_class': 'Grade 11'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_mobile_format_normalization(self):
        """
        Test that mobile numbers are normalized (digits only) for comparison.
        Flow: Same mobile (different format) -> Form validation -> Error message
        """
        form = StudentRegistrationForm(data={
            'name': 'New Student',
            'email': 'new@test.com',
            'mobile': '(987) 654-3210',  # Different format, same digits
            'student_class': 'Grade 11'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('mobile', form.errors)


class RegistrationFlowTestCase(TransactionTestCase):
    """
    Test Case 3: Complete Registration Flow
    
    Tests the end-to-end registration process:
    1. GET request shows registration form
    2. POST request with valid data creates student
    3. Data is encrypted in database
    4. Session data is stored
    5. Redirect to success page
    6. Email is sent
    """
    
    def setUp(self):
        """Set up test client and create table"""
        create_student_table()
        self.client = Client()
        self.registration_url = reverse('students:register_student')
        self.success_url = reverse('students:registration_success')
    
    def test_get_registration_page(self):
        """
        Test that GET request displays registration form.
        Flow: GET /register/ -> Form is displayed
        """
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student Registration')
        self.assertContains(response, 'form')
    
    @patch('students.views.send_mail')
    def test_complete_registration_flow(self, mock_send_mail):
        """
        Complete registration flow test.
        
        Flow:
        1. User submits valid registration form
        2. Data is validated
        3. Email and mobile are encrypted
        4. Student record is created in database
        5. Session data is stored
        6. User is redirected to success page
        7. Confirmation email is sent
        
        This test demonstrates the complete application flow.
        """
        # Mock email sending
        mock_send_mail.return_value = True
        
        # Step 1: Submit registration form
        form_data = {
            'name': 'Test Student',
            'email': 'teststudent@example.com',
            'mobile': '1234567890',
            'student_class': 'Grade 10'
        }
        
        response = self.client.post(self.registration_url, data=form_data, follow=True)
        
        # Step 2: Verify redirect to success page
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Registration Successful')
        
        # Step 3: Verify student was created in database
        students = Student.objects.all()
        self.assertEqual(students.count(), 1)
        
        student = students.first()
        self.assertEqual(student.name, 'Test Student')
        
        # Step 4: Verify data is encrypted in database
        self.assertIsInstance(student.email, bytes)
        self.assertIsInstance(student.mobile, bytes)
        
        # Step 5: Verify decryption works
        decrypted_email = decrypt_data(student.email)
        decrypted_mobile = decrypt_data(student.mobile)
        self.assertEqual(decrypted_email, 'teststudent@example.com')
        self.assertEqual(decrypted_mobile, '1234567890')
        
        # Step 6: Verify email was sent
        mock_send_mail.assert_called_once()
        call_args = mock_send_mail.call_args
        self.assertIn('teststudent@example.com', call_args[1]['recipient_list'])
        
        # Step 7: Verify success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Registration successful' in str(m) for m in messages))
    
    def test_registration_with_invalid_data(self):
        """
        Test registration with invalid data.
        Flow: Invalid form data -> Form validation fails -> Error message displayed
        """
        form_data = {
            'name': '',  # Missing required field
            'email': 'invalid-email',
            'mobile': '123'  # Too short
        }
        
        response = self.client.post(self.registration_url, data=form_data)
        
        # Should not redirect, form should be re-displayed with errors
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        
        # Verify no student was created
        self.assertEqual(Student.objects.count(), 0)
    
    def test_duplicate_registration_prevention(self):
        """
        Test that duplicate registrations are prevented.
        Flow: 
        1. Register first student
        2. Try to register with same email/mobile
        3. Second registration is rejected
        """
        # Create first student
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO student (name, email, mobile, student_class, created, modified)
                VALUES (%s, %s, %s, %s, NOW(), NOW())
                """,
                ['First Student', encrypt_data('duplicate@test.com'), encrypt_data('9999999999'), 'Grade 10']
            )
        
        # Try to register duplicate
        form_data = {
            'name': 'Second Student',
            'email': 'duplicate@test.com',  # Same email
            'mobile': '8888888888',
            'student_class': 'Grade 11'
        }
        
        response = self.client.post(self.registration_url, data=form_data)
        
        # Should show error, not create duplicate
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already registered')
        
        # Verify only one student exists
        students = Student.objects.all()
        self.assertEqual(students.count(), 1)


class DatabaseOperationsTestCase(TransactionTestCase):
    """
    Test Case 4: Database Operations
    
    Tests database operations including:
    - Creating student records
    - Encrypted data storage
    - Retrieving and decrypting data
    """
    
    def setUp(self):
        """Create student table"""
        create_student_table()
    
    def test_create_student_with_encryption(self):
        """
        Test creating a student record with encrypted data.
        Flow: Create student -> Data is encrypted -> Can be decrypted
        """
        name = 'Database Test Student'
        email = 'dbtest@example.com'
        mobile = '5555555555'
        student_class = 'Grade 12'
        
        # Create student using raw SQL (matching view logic)
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO student (name, email, mobile, student_class, created, modified)
                VALUES (%s, %s, %s, %s, NOW(), NOW())
                """,
                [name, encrypt_data(email), encrypt_data(mobile), student_class]
            )
            student_id = cursor.lastrowid
        
        # Retrieve student
        student = Student.objects.get(id=student_id)
        
        # Verify data
        self.assertEqual(student.name, name)
        self.assertEqual(student.student_class, student_class)
        
        # Verify encryption
        self.assertIsInstance(student.email, bytes)
        self.assertIsInstance(student.mobile, bytes)
        
        # Verify decryption
        self.assertEqual(decrypt_data(student.email), email)
        self.assertEqual(decrypt_data(student.mobile), mobile)
    
    def test_multiple_students_storage(self):
        """
        Test storing multiple students with different encrypted data.
        Flow: Create multiple students -> Each has unique encrypted data -> All can be decrypted
        """
        students_data = [
            ('Student 1', 'student1@test.com', '1111111111'),
            ('Student 2', 'student2@test.com', '2222222222'),
            ('Student 3', 'student3@test.com', '3333333333'),
        ]
        
        # Create students
        for name, email, mobile in students_data:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO student (name, email, mobile, student_class, created, modified)
                    VALUES (%s, %s, %s, %s, NOW(), NOW())
                    """,
                    [name, encrypt_data(email), encrypt_data(mobile), 'Grade 10']
                )
        
        # Verify all students exist
        self.assertEqual(Student.objects.count(), 3)
        
        # Verify each student's data can be decrypted correctly
        for i, (name, email, mobile) in enumerate(students_data, 1):
            student = Student.objects.get(id=i)
            self.assertEqual(student.name, name)
            self.assertEqual(decrypt_data(student.email), email)
            self.assertEqual(decrypt_data(student.mobile), mobile)


class IntegrationTestCase(TransactionTestCase):
    """
    Test Case 5: Integration Test - Complete Application Flow
    
    This is the main integration test that demonstrates the complete
    flow of the student registration application from start to finish.
    
    Flow:
    1. User visits registration page
    2. Fills out registration form
    3. Form validates data (including duplicate check)
    4. Data is encrypted
    5. Student record is saved to database
    6. Session data is stored
    7. User is redirected to success page
    8. Confirmation email is sent
    9. User can view their registration details
    """
    
    def setUp(self):
        """Set up test client, URLs, and create table"""
        create_student_table()
        self.client = Client()
        self.register_url = reverse('students:register_student')
        self.success_url = reverse('students:registration_success')
    
    @patch('students.views.send_mail')
    def test_complete_application_flow(self, mock_send_mail):
        """
        Complete end-to-end test of the student registration application.
        
        This test demonstrates the entire application flow and should be
        used as documentation for how the system works.
        """
        # Configure mock email
        mock_send_mail.return_value = True
        
        # ============================================
        # STEP 1: User visits registration page
        # ============================================
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student Registration')
        self.assertContains(response, 'Complete your registration')
        
        # ============================================
        # STEP 2: User fills out and submits form
        # ============================================
        registration_data = {
            'name': 'Integration Test Student',
            'email': 'integration@test.com',
            'mobile': '9876543210',
            'student_class': 'Grade 11'
        }
        
        # ============================================
        # STEP 3: Form validation (including duplicate check)
        # ============================================
        # The form will validate:
        # - Required fields are present
        # - Email format is valid
        # - Mobile has at least 10 digits
        # - Email/mobile are not duplicates (hash-based comparison)
        
        # ============================================
        # STEP 4: Submit registration
        # ============================================
        response = self.client.post(self.register_url, data=registration_data, follow=True)
        
        # ============================================
        # STEP 5: Verify redirect to success page
        # ============================================
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Registration Successful')
        self.assertContains(response, 'Integration Test Student')
        self.assertContains(response, 'integration@test.com')
        
        # ============================================
        # STEP 6: Verify student record in database
        # ============================================
        students = Student.objects.all()
        self.assertEqual(students.count(), 1)
        
        student = students.first()
        self.assertEqual(student.name, 'Integration Test Student')
        self.assertEqual(student.student_class, 'Grade 11')
        
        # ============================================
        # STEP 7: Verify data encryption
        # ============================================
        # Data should be encrypted in database
        self.assertIsInstance(student.email, bytes)
        self.assertIsInstance(student.mobile, bytes)
        
        # Verify encrypted data is different from plain text
        self.assertNotEqual(student.email, 'integration@test.com'.encode())
        self.assertNotEqual(student.mobile, '9876543210'.encode())
        
        # ============================================
        # STEP 8: Verify decryption works
        # ============================================
        decrypted_email = decrypt_data(student.email)
        decrypted_mobile = decrypt_data(student.mobile)
        
        self.assertEqual(decrypted_email, 'integration@test.com')
        self.assertEqual(decrypted_mobile, '9876543210')
        
        # ============================================
        # STEP 9: Verify email was sent
        # ============================================
        mock_send_mail.assert_called_once()
        call_args = mock_send_mail.call_args
        
        # Verify email recipient
        self.assertIn('integration@test.com', call_args[1]['recipient_list'])
        
        # Verify email subject contains registration ID
        self.assertIn(str(student.id), call_args[1]['subject'])
        
        # ============================================
        # STEP 10: Verify success message
        # ============================================
        messages = list(get_messages(response.wsgi_request))
        success_messages = [str(m) for m in messages if 'success' in str(m).lower()]
        self.assertTrue(len(success_messages) > 0)
        
        # ============================================
        # STEP 11: Test duplicate prevention
        # ============================================
        # Try to register again with same email
        duplicate_response = self.client.post(self.register_url, data=registration_data)
        
        # Should show error, not create duplicate
        self.assertEqual(duplicate_response.status_code, 200)
        self.assertContains(duplicate_response, 'already registered')
        
        # Verify only one student exists
        self.assertEqual(Student.objects.count(), 1)
        
        print("\n" + "="*60)
        print("INTEGRATION TEST COMPLETE")
        print("="*60)
        print("✓ Registration page loads correctly")
        print("✓ Form validation works")
        print("✓ Data encryption works")
        print("✓ Student record created in database")
        print("✓ Data decryption works")
        print("✓ Email sending works")
        print("✓ Duplicate prevention works")
        print("="*60)
