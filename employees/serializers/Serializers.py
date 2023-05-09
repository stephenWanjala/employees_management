from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from employees.models import Training, JobTitle, Department, PerformanceReview, Employee


class JobTitleSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = JobTitle
        fields = '__all__'


class EmployeeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'department', 'job_title', 'hire_date',
                  'performance_goals', 'manager']
        depth = 1
        expandable_fields = {
            'manager': ('employees.EmployeeSerializer', {'source': 'manager'}),
            'job_title': (JobTitleSerializer, {'source': 'job_title'}),
            'department': ('employees.DepartmentSerializer', {'source': 'department'}),
            'performance_reviews': ('employees.PerformanceReviewSerializer', {'many': True}),
            'trainings_completed': ('employees.TrainingSerializer', {'many': True}),
        }


class EmployeeSerializerExpandedDepartment(FlexFieldsModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'job_title', 'hire_date',
                  'performance_goals', 'manager']
        depth = 1
        expandable_fields = {
            'manager': ('employees.EmployeeSerializer', {'source': 'manager'}),
            'job_title': (JobTitleSerializer, {'source': 'job_title'}),
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


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password],
                                     style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'job_title', 'department', 'password',
                  'password2', 'hire_date',)
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = get_user_model().objects.create(
            last_name=validated_data['last_name'],
            first_name=validated_data['first_name'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            department=validated_data['department'],
            job_title=validated_data['job_title'],
            hire_date=validated_data['hire_date']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if get_user_model().objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if get_user_model().objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return instance
