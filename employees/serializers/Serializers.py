from rest_flex_fields import FlexFieldsModelSerializer

from employees.models import Training, JobTitle, Department, PerformanceReview, Employee


class JobTitleSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = JobTitle
        fields = '__all__'


class EmployeeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        depth = 1
        expandable_fields = {
            'manager': ('employees.EmployeeSerializer', {'source': 'manager'}),
            'job_title': (JobTitleSerializer, {'source': 'job_title'}),
            'department': ('employees.DepartmentSerializer', {}),
            'performance_reviews': ('employees.PerformanceReviewSerializer', {'many': True}),
            'trainings_completed': ('employees.TrainingSerializer', {'many': True}),
        }


class PerformanceReviewSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = PerformanceReview
        fields = '__all__'
        depth = 1
        expandable_fields = {
            'employee': ('employees.EmployeeSerializer', {}),
            'reviewer': ('employees.EmployeeSerializer', {}),
        }


class DepartmentSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        expandable_fields = {
            'manager': ('employees.EmployeeSerializer', {}),
            'employees': ('employees.EmployeeSerializer', {'many': True}),

        }


class TrainingSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Training
        fields = '__all__'
        expandable_fields = {
            'employees': ('employees.EmployeeSerializer', {'many': True}),
        }
