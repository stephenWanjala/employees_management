# Create your views here.
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from employees.models import Employee
from employees.serializers.Serializers import EmployeeSerializer


# @api_view(['GET'])
# def api_root(request):
#     return Response(
#     )


class EmployeeList(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
