# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from employees.models import Employee, Department
from employees.serializers.Serializers import EmployeeSerializer


@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API.
    :param request:
    :param format:
    :return:
    """
    sample_employee_id = 1  # replace with a valid employee_id
    sample_department_name = "computing"  # replace with a valid departmentName
    sample_department_id = 1  # replace with a valid department_id
    return Response({
        'employees': reverse('employees', request=request, format=format),
        'employee': reverse('employee', args=[sample_employee_id], request=request, format=format),
        'employees_in_department': reverse('employees_in_department', args=[sample_department_name], request=request,
                                           format=format),
        'employees_in_department_by_id': reverse('employees_in_department_by_id', args=[sample_department_id],
                                                 request=request, format=format),
    })


@api_view(['GET', 'POST'])
def employee_list(request):
    """
    List all employees, or create a new employee.
    :param request:
    :return:
    """
    if request.method == 'GET':
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def employee_detail(request, employee_id):
    """
    Retrieve, update or delete a employee instance.

    :param request:
    :param employee_id:
    :return:
    """
    try:
        employee = Employee.objects.get(pk=int(employee_id))
    except Employee.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = EmployeeSerializer(employee, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmployeeSerializer(employee, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        employee.delete()
        return Response(status=204)


@api_view(['GET'])
def department_list(request):
    """
    List all departments.
    :param request:
    :return:
    """
    departments = Department.objects.all()
    data = [{'id': department.id, 'name': department.name} for department in departments]
    return Response(data)


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


# @api_view(['GET'])
# def employees_in_department(request):
#     # Filter by department
#     """
#     List all employees in a department. by the department name.
#     :param request:
#     :return:
#     """
#     department = request.query_params.get('department', None)
#     if department is not None:
#         employees = Employee.objects.filter(department__name__icontains=department)
#     else:
#         employees = Employee.objects.all()
#
#     serializer = EmployeeSerializer(employees, many=True)
#     return Response(serializer.data)

@api_view(['GET'])
def employees_in_department(request, department_name):
    """
    Retrieve a list of employees in a given department by the department name.
    """
    department = get_object_or_404(Department, name=department_name)
    employees = Employee.objects.filter(department=department)
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)
