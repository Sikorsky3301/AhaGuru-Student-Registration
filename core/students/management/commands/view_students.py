from django.core.management.base import BaseCommand
from students.models import Student
from students.encryption import decrypt_data


class Command(BaseCommand):
    help = 'Display all students with decrypted email and mobile data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--id',
            type=int,
            help='View a specific student by ID',
        )

    def handle(self, *args, **options):
        student_id = options.get('id')
        
        if student_id:
            try:
                student = Student.objects.get(id=student_id)
                self.display_student(student)
            except Student.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Student with ID {student_id} not found.'))
        else:
            students = Student.objects.all().order_by('-created')
            
            if not students.exists():
                self.stdout.write(self.style.WARNING('No students found in database.'))
                return
            
            self.stdout.write(self.style.SUCCESS(f'\nTotal Students: {students.count()}\n'))
            self.stdout.write('=' * 70)
            
            for student in students:
                self.display_student(student)
                self.stdout.write('-' * 70)
    
    def display_student(self, student):
        """Display a single student's information."""
        try:
            email = decrypt_data(student.email) if student.email else 'N/A'
            mobile = decrypt_data(student.mobile) if student.mobile else 'N/A'
        except Exception as e:
            email = f'Decryption Error: {str(e)}'
            mobile = f'Decryption Error: {str(e)}'
        
        self.stdout.write(f'\nID: {student.id}')
        self.stdout.write(f'Name: {student.name}')
        self.stdout.write(f'Email: {email}')
        self.stdout.write(f'Mobile: {mobile}')
        self.stdout.write(f'Class: {student.student_class or "Not specified"}')
        self.stdout.write(f'Created: {student.created}')
        self.stdout.write(f'Modified: {student.modified}')
