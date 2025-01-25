#  Copyright (c) 2023 TaggLabs Pvt. Ltd.
#  salary_app/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from salary_app.views import EmployeeViewSet, SalarySlipView, generate_salary_slip_pdf, SalarySlipListView
from django.conf import settings
from django.conf.urls.static import static

# Initialize the router
router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

# Define the URL patterns
urlpatterns = [
    path('salary_slip/', SalarySlipView.as_view(), name='salary_slip'), # Path for rendering the salary slip page
    path('employees/', include(router.urls)),  # API for employees
    path('download_salary_slip_pdf/<int:slip_id>/', generate_salary_slip_pdf.as_view(), name='download_pdf'),
    path('salary_slip_list/', SalarySlipListView.as_view(), name='salary_slip_list'), # Path for listing salary slips
]
# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)