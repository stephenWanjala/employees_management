# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from employees.models import (
    Employee, Department, Training
)
from employees.serializers.Serializers import (EmployeeSerializer, DepartmentSerializer,
                                               EmployeeSerializerExpandedDepartment, TrainingSerializer,
                                               RegisterSerializer)

# @api_view(['GET'])
# def api_root(request):
#     return Response(
#     )
User = get_user_model()


class EmployeeList(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        queryset = User.objects.filter(is_superuser=False)
        return queryset


class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


@api_view(['GET'])
def department_list(request):
    """
    List all departments.
    :param request:
    :return:
    """
    departments = Department.objects.all()
    data = [{'id': department.id, 'name': department.name} for department in departments]
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def department_employees(request, department_id):
    """
    List all employees in a department. by the department id.
    :param request:
    :param department_id:
    :return:
    """
    employees = Employee.objects.filter(department_id=department_id)
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def employees_in_department(request, department_name):
    """
    Get a list of employees in a department
    :param request:
    :param department_name:
    :return:
    """
    # find the department that matches the department_name
    department = Department.objects.filter(name__icontains=department_name).first()

    # if the department is not found, return an empty list
    if department is None:
        return Response([], status=status.HTTP_404_NOT_FOUND)

    # find the employees that belong to the department
    employees = Employee.objects.filter(department=department)

    # serialize the employees and return them
    serializer = EmployeeSerializerExpandedDepartment(employees, many=True)
    return Response(serializer.data)


class DepartmentList(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class TrainingList(generics.ListCreateAPIView):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer


class TrainingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
