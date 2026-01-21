from django.db import models


class Student(models.Model):
    """
    Student model matching the manually created database table.
    Since the table is created manually, managed=False prevents Django migrations.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.BinaryField(max_length=255)  # VARBINARY for encrypted storage
    mobile = models.BinaryField(max_length=255)  # VARBINARY for encrypted storage
    student_class = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student'
        managed = False  # Table is managed manually via SQL

    def __str__(self):
        return f"Student {self.id}: {self.name}"
