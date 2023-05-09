from django.urls import path
from employees import views

urlpatterns = [
    path('employees/', views.EmployeeList.as_view()),
    path('employees/<int:pk>/', views.EmployeeDetail.as_view()),
]
