from django.urls import path

from employees import views

urlpatterns= [
    # path('', views.employee_list, name='employees'),
    path('employees/', views.employee_list, name='employees'),
    # path('employees/<int:employee_id>', views.employee, name='employee'),
    # path('employees/<int:employee_id>/reviews', views.employee_reviews, name='employee_reviews'),
    # path('employees/<int:employee_id>/reviews/<int:review_id>', views.employee_review, name='employee_review'),
    # path('employees/<int:employee_id>/trainings', views.employee_trainings, name='employee_trainings'),
    # path('employees/<int:employee_id>/trainings/<int:training_id>', views.employee_training, name='employee_training'),
    ]