from django.contrib import admin
from django.utils.html import format_html
from .models import Student
from .encryption import decrypt_data


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Admin interface for Student model with decrypted email and mobile display.
    """
    list_display = ('id', 'name', 'decrypted_email', 'decrypted_mobile', 'student_class', 'created', 'modified')
    list_filter = ('student_class', 'created')
    search_fields = ('name', 'student_class')
    readonly_fields = ('id', 'created', 'modified', 'decrypted_email', 'decrypted_mobile', 'encrypted_email_display', 'encrypted_mobile_display')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'student_class')
        }),
        ('Contact Information (Decrypted)', {
            'fields': ('decrypted_email', 'decrypted_mobile'),
            'description': 'These are the decrypted values for viewing purposes.'
        }),
        ('Encrypted Data (Database Storage)', {
            'fields': ('encrypted_email_display', 'encrypted_mobile_display'),
            'description': 'This is how the data is stored in the database (encrypted).'
        }),
        ('Timestamps', {
            'fields': ('created', 'modified')
        }),
    )
    
    def decrypted_email(self, obj):
        """Display decrypted email address."""
        try:
            return decrypt_data(obj.email) if obj.email else '-'
        except Exception as e:
            return f'Error: {str(e)}'
    decrypted_email.short_description = 'Email (Decrypted)'
    
    def decrypted_mobile(self, obj):
        """Display decrypted mobile number."""
        try:
            return decrypt_data(obj.mobile) if obj.mobile else '-'
        except Exception as e:
            return f'Error: {str(e)}'
    decrypted_mobile.short_description = 'Mobile (Decrypted)'
    
    def encrypted_email_display(self, obj):
        """Display encrypted email as hex for reference."""
        if obj.email:
            hex_data = obj.email.hex()[:50] + '...' if len(obj.email.hex()) > 50 else obj.email.hex()
            return format_html('<code>{}</code>', hex_data)
        return '-'
    encrypted_email_display.short_description = 'Email (Encrypted - Hex)'
    
    def encrypted_mobile_display(self, obj):
        """Display encrypted mobile as hex for reference."""
        if obj.mobile:
            hex_data = obj.mobile.hex()[:50] + '...' if len(obj.mobile.hex()) > 50 else obj.mobile.hex()
            return format_html('<code>{}</code>', hex_data)
        return '-'
    encrypted_mobile_display.short_description = 'Mobile (Encrypted - Hex)'
    
    def has_add_permission(self, request):
        """Disable adding students through admin (use registration form instead)."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Allow deletion if needed."""
        return True
