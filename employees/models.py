from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


# Create your models here.


class JobTitle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class EmployeeManager(BaseUserManager):
    def create_user(self, email, password=None, department=None, job_tittle=None, hire_date=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        if not department and not extra_fields.get('is_superuser'):
            raise ValueError('The Department field must be set')
        if not hire_date:
            raise ValueError("Hire date Required")
        if not job_tittle:
            raise ValueError("Job Tittle required")
        email = self.normalize_email(email)
        user = self.model(email=email, job_tittle=job_tittle, hire_date=hire_date ** extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('job_title'):
            extra_fields['job_title'] = JobTitle.objects.get_or_create(name='Admin')[0]

        if extra_fields.get('is_superuser'):
            extra_fields['performance_goals'] = ''
            extra_fields['manager'] = None
            extra_fields['hire_date'] = timezone.now().date()

        return self.create_user(email, password, **extra_fields)


class Employee(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20)
    job_title = models.ForeignKey(JobTitle, on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True)
    hire_date = models.DateField()
    performance_goals = models.TextField()
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["phone_number", "first_name", "last_name", 'job_title', 'hire_date']

    objects = EmployeeManager()


# class Employee(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=255)
#     phone_number = models.CharField(max_length=20)
#     job_title = models.ForeignKey(JobTitle, on_delete=models.CASCADE)
#     department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True)
#     hire_date = models.DateField()
#     performance_goals = models.TextField()
#     manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
#
#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'


class PerformanceReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Employee, related_name='reviews_given', on_delete=models.CASCADE)
    date = models.DateField()
    comments = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.employee} review by {self.reviewer}'


class Department(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='department_manager')

    def __str__(self):
        return self.name


class Training(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.PositiveIntegerField()
    employees = models.ManyToManyField('Employee', related_name='trainings_completed')
