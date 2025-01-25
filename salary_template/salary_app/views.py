#  Copyright (c) 2023 TaggLabs Pvt. Ltd.
#  salary_app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django.views import View
from num2words import num2words  # Ensure you have this installed
from .serializers import EmployeeSerializer
from salary.models import SalarySlip, User
from django.http import Http404


from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import DatabaseError


# API View for managing Employee Salary Slips
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = SalarySlip.objects.all()
    serializer_class = EmployeeSerializer

# View for rendering the salary_slip.html template
class UserSalarySlipView(LoginRequiredMixin, View):
    login_url = '/login/'  # Redirect URL for unauthenticated users

    def get(self, request, slip_id):
        # Get the salary slip for the current user and matching slip_id
        try:
            salary_slip = SalarySlip.objects.get(slip_id=slip_id, user=request.user)
        except SalarySlip.DoesNotExist:
            raise Http404("No SalarySlip matches the given query or you do not have access.")


        # Prepare the context to pass to the template
        context = {
            'WATERMARK': salary_slip.watermark.url if salary_slip.watermark else None,
            'COMPANY_LOGO': salary_slip.company_logo.url if salary_slip.company_logo else None,
            'COMPANY_NAME': salary_slip.company_name,
            'PAYSLIP': salary_slip.payslip_month,
            'COMPANY_PHONE': salary_slip.company_phone,
            'COMPANY_EMAIL': salary_slip.company_email,
            'COMPANY_WEBSITE': salary_slip.company_website,
            'COMPANY_ADDRESS': salary_slip.company_address,
            'EMPLOYEE_NO': salary_slip.employee_no,
            'EMPLOYEE_NAME': salary_slip.employee_name,
            'DOJ': salary_slip.doj,
            'BANK_NAME': salary_slip.bank_name,
            'BANK_ACCOUNT': salary_slip.bank_account,
            'BANK_IFSC': salary_slip.bank_ifsc,
            'UAN_NO': salary_slip.uan_no,
            'PAN_NO': salary_slip.pan_no,
            'BRANCH': salary_slip.branch,
            'DEPARTMENT': salary_slip.department,
            'DESIGNATION': salary_slip.designation,
            'TOTAL_DAYS': salary_slip.total_days,
            'LOP': salary_slip.lop,
            'WORK_DAYS': salary_slip.work_days,
            'EFFECTIVE_WORK_DAYS': salary_slip.effective_work_days,
            'BASIC_SALARY': salary_slip.basic_salary,
            'HRA': salary_slip.hra,
            'SPECIAL_ALLOWANCE': salary_slip.special_allowance,
            'ACCOMMODATION_ALLOWANCE': salary_slip.accommodation_allowance,
            'EPF_EMPLOYEE': salary_slip.epf_employee,
            'GROUP_MEDICAL_INSURANCE': salary_slip.gmi,
            'PROFESSIONAL_TAX': salary_slip.professional_tax,
            'TOTAL_GROSS': salary_slip.total_gross,
            'TOTAL_DEDUCTION': salary_slip.total_deduction,
            'TOTAL_FBP': salary_slip.total_fbp,
            'NET_PAY': salary_slip.net_pay,
            'NET_PAY_WORDS': num2words(salary_slip.net_pay, to='currency', lang='en'),  # Converts net pay to words
        }

        # Render the template with the context
        return render(request, 'salary_slip.html', context)
    

# View for listing salary slips with pagination
class SalarySlipListView(LoginRequiredMixin, View):
    login_url = '/login/'  # Redirect for unauthenticated users

    def get(self, request):
        # Fetch salary slips for the logged-in user
        salary_slips = SalarySlip.objects.filter(user=request.user).order_by('-generated_at')

        if not salary_slips.exists():
            # If no slips exist for the user, return an error message
            return render(request, 'salary_slip_list.html', {
                'salary_slips': None,
                'title': 'Salary Slips List',
                'error': "No salary slips found for this user."
            })

        # Paginate salary slips (10 per page)
        paginator = Paginator(salary_slips, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'salary_slip_list.html', {
            'salary_slips': page_obj,
            'title': 'Salary Slips List',
            'error': None
        })


# generate for downloading the salary slip
class generate_salary_slip_pdf(LoginRequiredMixin, View):
    login_url = '/login/'  # Redirect URL for unauthenticated users

    def get(self, request, slip_id):
        # Get the salary slip for the provided slip_id
        slip = get_object_or_404(SalarySlip, slip_id=slip_id, user=request.user)

        # Create a response for the PDF download
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="SalarySlip_{slip.payslip_number}.pdf"'

        # Create the PDF document using ReportLab (or WeasyPrint)
        p = canvas.Canvas(response)
        p.drawString(100, 800, f"Salary Slip for {slip.employee_name}")
        p.drawString(100, 780, f"Net Pay: {slip.net_pay}")
        p.showPage()
        p.save()
        
        return response