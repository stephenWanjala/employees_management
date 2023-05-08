from django.db import models


# Create your models here.


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=20)
    job_title = models.ForeignKey('JobTitle', on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    hire_date = models.DateField()
    performance_goals = models.TextField()
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


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
        related_name='managed_departments')

    def __str__(self):
        return self.name


class JobTitle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Training(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.PositiveIntegerField()
    employees = models.ManyToManyField('Employee', related_name='trainings_completed')

