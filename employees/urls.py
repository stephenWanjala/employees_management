from django.urls import path

from employees import views

urlpatterns = [
    path('employee/', views.RegisterView.as_view()),
    path('employees/', views.EmployeeList.as_view()),
    path('employees/<int:pk>/', views.EmployeeDetail.as_view()),
    path('departments/', views.DepartmentList.as_view(), name='departments'),
    path('departments/<str:department_name>/employees/', views.employees_in_department, name='employees_in_department'),
    path('departments/<int:department_id>', views.department_employees, name='employees_in_department_by_id'),
]
