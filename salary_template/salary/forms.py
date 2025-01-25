#  salary/forms.py
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django import forms
from .models import User, SalarySlip  # Assuming User is your custom user model


# RegistrationForm class
class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'address', 'mobile', 'email', 'password']  # Include only fields defined in your User model
        widgets = {
            'password': forms.PasswordInput(),  # Password field as a masked input
        }
    # Custom clean method to validate the password
    def clean_password(self):
        password = self.cleaned_data.get('password')  # Retrieve the password from cleaned_data
        try:
            validate_password(password)  # Validate the password
        except ValidationError as e:
            raise forms.ValidationError(e.messages)  # Raise validation errors, if any
        return password

    # Set the placeholder attribute for the password field
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'Enter a strong password'})

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

# SalarySlipForm class
class SalarySlipForm(forms.ModelForm):
    class Meta:
        model = SalarySlip
        fields = [
            'watermark', 
            'company_logo', 
            'company_name', 
            'payslip_month', 
            'company_name_info', 
            'company_phone', 
            'company_email', 
            'company_website', 
            'company_address',
            'employee_no', 
            'employee_name', 
            'doj', 
            'bank_name', 
            'bank_account', 
            'bank_ifsc', 
            'uan_no', 
            'pan_no', 
            'branch', 
            'department', 
            'designation', 
            'total_days', 
            'lop', 
            'work_days', 
            'effective_work_days', 
            'basic_salary', 
            'hra', 
            'special_allowance', 
            'accommodation_allowance',
            'epf_employee', 
            'gmi', 
            'professional_tax', 
            'total_gross', 
            'total_deduction', 
            'total_fbp', 
            'net_pay', 
            'note'
        ]
        widgets = {
            'watermark': forms.ClearableFileInput(),
            'company_logo': forms.ClearableFileInput(),
            'doj': forms.DateInput(attrs={'type': 'date'}),
            'bank_account': forms.NumberInput(attrs={'min': 1000000000, 'max': 9999999999}),
            'epf_employee': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'gmi': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'professional_tax': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'total_gross': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'total_deduction': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'total_fbp': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'net_pay': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'note': forms.Textarea(attrs={'rows': 3, 'cols': 30}),
        }

    # Set the user attribute from the view
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # Set the user attribute from the view

    # Save the form data to the database
    def save(self, commit=True):
        salary_slip = super().save(commit=False)
        salary_slip.user = self.user  # Associate user with salary slip
        if commit:
            salary_slip.save()
        return salary_slip
