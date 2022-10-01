from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenRefreshView
)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('test/', testEndPoint, name='test'),
    path('deptos/', DeptoView.as_view(), name='depto_list'),
    path('deptos/<int:id>', DeptoView.as_view(), name='depto_process'),
    #path('add_reservation/', AddReservation.as_view(), name='reservation_process'),
    path('reserve/', addReservation, name='reserve_process'),
    path('', getRoutes)
]