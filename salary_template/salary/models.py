# salary/models.py
from django.db import models
from django.contrib.auth.models import User  # Add this line
import uuid
import os
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now 

# Custom User model inheriting AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import os
from django.core.exceptions import ValidationError

# Validator for file extensions
def validate_file_extension(value):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']
    ext = os.path.splitext(value.name)[1].lower()  # Get the file extension from the file name
    if ext not in valid_extensions:
        raise ValidationError(f"Invalid file extension. Allowed: {', '.join(valid_extensions)}.")


# Custom User model inheriting AbstractUser
class User(AbstractUser):
    # Using UUID as the primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Custom fields
    name = models.CharField(max_length=100)  # Custom name field
    address = models.TextField()  # Address field
    mobile = models.CharField(max_length=15)  # Mobile number field
    email = models.EmailField(unique=True)  # Email field with uniqueness constraint
    role = models.CharField(
        max_length=20,
        choices=[('user', 'User'), ('admin', 'Admin')],
        default='user'
    )  # Role field with default value 'user'
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set when the object is updated

    # Set email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'address', 'mobile', 'role']

    def save(self, *args, **kwargs):
        # Assign the role 'admin' to superusers
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.role}"

# salary class
class SalarySlip(models.Model):
    slip_id = models.CharField(
        primary_key=True,
        max_length=50,
        unique=True,
        default=uuid.uuid4,
        editable=False
    )  

    # Linking the user to the SalarySlip model using a ForeignKey
    user = models.ForeignKey(
        'User',  # Refers to the custom User model
        on_delete=models.CASCADE,
        related_name='salary_slips',
        null=True,
        blank=True
    )
    
    # Use the custom User model

    # File fields
    watermark = models.ImageField(
        upload_to='watermarks/',
        validators=[validate_file_extension],
        null=True,
        blank=True
    )
    company_logo = models.ImageField(
        upload_to='company_logos/',
        validators=[validate_file_extension],
        null=True,
        blank=True
    )

    # Company Details
    company_name = models.CharField(max_length=255, blank=True, null=True)
    payslip_month = models.CharField(max_length=50, blank=True)
    company_name_info = models.CharField(max_length=100, blank=True)
    company_phone = models.CharField(max_length=15, blank=True)
    company_email = models.EmailField(blank=True)  # Optional email
    company_website = models.URLField(blank=True)  # Optional website
    company_address = models.TextField(blank=True)

    # Employee Details
    employee_no = models.CharField(max_length=50, blank=True)
    employee_name = models.CharField(max_length=100, blank=True)
    doj = models.DateField(null=True, blank=True)  # Optional Date of Joining
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account = models.CharField(max_length=20, blank=True)
    bank_ifsc = models.CharField(max_length=20, blank=True)
    uan_no = models.CharField(max_length=20, blank=True)
    pan_no = models.CharField(max_length=20, blank=True)

    # Work Details
    branch = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    total_days = models.IntegerField(default=0)  # Total working days
    lop = models.IntegerField(default=0)  # Loss of Pay
    work_days = models.IntegerField(default=0)
    effective_work_days = models.IntegerField(default=0)

    # Salary Details
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    hra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    special_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    accommodation_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    epf_employee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Employee Provident Fund
    gmi = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Group Medical Insurance
    professional_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_gross = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_fbp = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Fixed Benefit Plan
    net_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    generated_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set when the object is updated
    # Additional Information
    note = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slip_id:
            # Create a unique slip ID before saving the object
            self.slip_id = f"SLIP-{uuid.uuid4().hex[:8]}"  # Generate a unique slip ID
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Salary Slip for {self.user.email} - {self.slip_id} ({self.payslip_month or 'No Payslip month'})\n"
            f"Company: {self.company_name}\n"
            f"Employee: {self.employee_name} (Employee No: {self.employee_no})\n"
            f"Designation: {self.designation}\n"
            f"DOJ: {self.doj}\n"
            f"Bank: {self.bank_name} (Account No: {self.bank_account}, IFSC: {self.bank_ifsc})\n"
            f"Salary Details: Basic: {self.basic_salary}, HRA: {self.hra}, Special Allowance: {self.special_allowance}, "
            f"Accommodation Allowance: {self.accommodation_allowance}, EPF: {self.epf_employee}, GMI: {self.gmi}\n"
            f"Gross: {self.total_gross}, Deductions: {self.total_deduction}, Net Pay: {self.net_pay}\n"
            f"Generated At: {self.generated_at}, Last Updated: {self.updated_at}\n"
            f"Note: {self.note or 'No Additional Notes'}"
        )