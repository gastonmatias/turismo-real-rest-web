from django.urls import path
from .views import *

urlpatterns = [
    path('employee/', EmployeeView.as_view()),
    path('employee/<int:pk>/', EmployeeDetailView.as_view()),
    path('employee_logout/',EmployeeLogoutView.as_view()),
    path('employee_login/', EmployeeLoginView.as_view()),
    path('extra_services/', ExtraServicesView.as_view()),
    path('extra_services/add/', AddExtraServicesView.as_view()),
    path('department/', DepartmentView.as_view())
]
