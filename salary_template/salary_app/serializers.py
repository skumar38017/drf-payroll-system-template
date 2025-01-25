# salary_app/serializers.py


from rest_framework import serializers
from salary.models import SalarySlip, User


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalarySlip
        fields = '__all__'
