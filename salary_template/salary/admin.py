# salary/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import SalarySlip

# Get the custom User model
User = get_user_model()

# Define a custom UserAdmin
class UserAdmin(BaseUserAdmin):
    # Fields to display in the list view
    list_display = ('id', 'name', 'email', 'address', 'mobile', 'role', 'is_active', 'is_staff', 'password', 'is_superuser')
    
    # Fields to use in the detail form view (exclude 'id')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'address', 'mobile', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields for the add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'address', 'mobile', 'role'),
        }),
    )
    
    # Fields to use for filtering in the list view
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'groups')
    
    # Searchable fields in the admin
    search_fields = ('email', 'name', 'mobile')
    
    ordering = ('email',)

# Register the custom User model and the UserAdmin
admin.site.register(User, UserAdmin)

class SalarySlipAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = (
        'user', 
        'slip_id',
        'payslip_month', 
        'employee_name', 
        'designation', 
        'company_name', 
        'doj', 
        'bank_name',
        'bank_ifsc',
        'pan_no',
        'net_pay', 
        'total_gross', 
        'total_deduction', 
        'generated_at',  # Assuming you have a created_at field in your model
    )
    
    # Fields to filter the list by (optional)
    list_filter = (
        'company_name', 
        'employee_name', 
        'doj', 
        'designation',
    )
    
    # Searchable fields (optional)
    search_fields = (
        'payslip_number', 
        'employee_name', 
        'company_name', 
        'user__email',  # Search by user's email
    )

    # Ordering of the list (optional)
    ordering = ('-doj', 'employee_name')  # Order by Date of Joining descending and employee name ascending

# Register the model with the admin
admin.site.register(SalarySlip, SalarySlipAdmin)
