# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from employees.models import Employee
from employees.serializers.Serializers import EmployeeSerializer


@api_view(['GET'])
def api_root(request, format=None):
    sample_employee_id = 1  # replace with a valid employee_id
    return Response({
        'employees': reverse('employees', request=request, format=format),
        'employee': reverse('employee', args=[sample_employee_id], request=request, format=format),
        # 'employee_reviews': reverse('employee_reviews', request=request, format=format),
        # 'employee_review': reverse('employee_review', request=request, format=format),
        # 'employee_trainings': reverse('employee_trainings', request=request, format=format),
        # 'employee_training': reverse('employee_training', request=request, format=format),
    })


@api_view(['GET', 'POST'])
def employee_list(request):
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
