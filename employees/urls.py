from django.urls import path

from employees import views

urlpatterns = [
    path('', views.api_root, name='api_root'),
    # path('', views.employee_list, name='employees'),
    path('employees/', views.employee_list, name='employees'),
    path('employees/create', views.create_employee, name='create_employee'),
    path('employees/<int:employee_id>', views.employee_detail, name='employee'),
    path('departments/<str:department_name>/employees/', views.employees_in_department, name='employees_in_department'),
    path('departments/<int:department_id>', views.department_employees, name='employees_in_department_by_id'),
    # path('employees/<int:employee_id>/reviews', views.employee_reviews, name='employee_reviews'),
    # path('employees/<int:employee_id>/reviews/<int:review_id>', views.employee_review, name='employee_review'),
    # path('employees/<int:employee_id>/trainings', views.employee_trainings, name='employee_trainings'),
    # path('employees/<int:employee_id>/trainings/<int:training_id>', views.employee_training, name='employee_training'),
]
