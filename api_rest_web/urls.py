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
    path('servicios_extra/', GetService.as_view(), name='getService'),
    path('disponibilidad_depto/<int:id>', GetFechasNoDisponibles.as_view(), name='getFechasNoDisponibles'),
    path('reservas/<int:id>', GetReservas.as_view(), name='getReservas'),
    path('cancelar_reserva/<int:id>', CancelarReserva.as_view(), name='cancelarReserva'),
    path('editar_reserva/<int:id>', EditarReserva.as_view(), name='editarReserva'),
    path('services_by_reservation/<int:id>', getServicesByReservation.as_view(), name='getServicesByIdReserva'),
    path('add_transaction/', AddTransactionView.as_view()), 
    path('', getRoutes)
]