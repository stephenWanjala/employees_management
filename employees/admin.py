from django.contrib import admin

from employees import models

# Register your models here.
admin.site.register(models.Employee)
admin.site.register(models.PerformanceReview)
admin.site.register(models.Department)
admin.site.register(models.JobTitle)
admin.site.register(models.Training)
