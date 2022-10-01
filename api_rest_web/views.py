from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from api_rest_web.serializer import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views import View
import base64
import cx_Oracle

from  django.db import connection
from django.forms import model_to_dict

#from backend_django.api.models import Department
from api_rest.models import Department

# Create your views here.

""" INIT autenticacion cliente """
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# muestra utilidades de api rest en http://localhost:8000/api/
@api_view(['GET'])
def getRoutes(request):
    routes = [
        #'/api/token/',
        #'/api/register/',
        #'/api/token/refresh/',
        #'/api/deptos/'
        '/api_web/token/',
        '/api_web/register/',
        '/api_web/token/refresh/',
        #'/api_rest_web/deptos/'
    ]
    return Response(routes)

#  solo para testear de qe token capturado funca
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get('text')
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST) 
    
""" FIN autenticacion cliente """

""" # INIT servicios para front """

class DeptoView(View):
    # Funcion Para obtener datos de deptos
    def get(self, request,id=0):

        # SI viene una id como parametro, buscar SOLO 1 depa, filtrando x el id otorgado
        if(id>0):
            django_cursor = connection.cursor()
            cursor = django_cursor.connection.cursor()
            out_cursor = django_cursor.connection.cursor()
            cursor.callproc('GET_DEPTO_BY_ID',[out_cursor,id])
            departments = []
            
            for i in out_cursor:
                department_json= {
                    "id": i[0],
                    "address": i[1],
                    "short_description": i[2],
                    "long_description": i[3],
                    "qty_rooms": i[4],
                    "price": i[5],
                    "department_image": i[6] if i[6] == None else str(base64.b64encode(i[6].read()), 'utf-8'),
                    "region": i[7],
                    "commune": i[8]
                }
                departments.append(department_json)
        
            return JsonResponse({
                'message': 'success',
                'deptos': departments
            })                       

        # si NO viene una id como parametro, buscar TODOS los depas
        else:
            #data = execute_proc('departments_list',[out_cur])
            django_cursor = connection.cursor()
            cursor = django_cursor.connection.cursor()
            out_cursor = django_cursor.connection.cursor()
            cursor.callproc('DEPARTMENTS_LIST',[out_cursor])
            departments = []
            
            for i in out_cursor:
                department_json= {
                    "id": i[0],
                    "address": i[1],
                    "short_description": i[2],
                    "long_description": i[3],
                    "qty_rooms": i[4],
                    "price": i[5],
                    "department_image": i[6] if i[6] == None else str(base64.b64encode(i[6].read()), 'utf-8'),
                    "region": i[7],
                    "commune": i[8]
                }
                departments.append(department_json)
            
            return JsonResponse({
                'message': 'success',
                'deptos': departments
            })        

# ! INIT ADD Reservation
def addReservation(request):   
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        qty_customers = request.POST.get('qty_customers')
        reservation_amount = request.POST.get('reservation_amount')
        total_amount = request.POST.get('total_amount')
        user_id = request.POST.get('user_id')
        department_id = request.POST.get('department_id')
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        salida = cursor.var(cx_Oracle.NUMBER)
        cursor.callproc('ADD_RESERVATION',[check_in,check_out,qty_customers,reservation_amount,total_amount,user_id,department_id,salida])
        
        id_reservation = salida.getvalue() #id obtenido

        services_selected = [6,7,8,9]

        reserv_detail_records = []

        for i in services_selected:
            cursor.callproc('ADD_RESERVATION_DETAILS',[i,id_reservation,salida])
            reserv_detail_records.append(salida.getvalue())

        json_salida = {
            "id_reservation":id_reservation,
            "services": reserv_detail_records
        }

        return JsonResponse(json_salida, safe= False)


#class AddReservation(View):
#    def post(self,request):    
#        check_in = request.POST.get('check_in')
#        check_out = request.POST.get('check_out')
#        qty_customers = request.POST.get('qty_customers')
#        reservation_amount = request.POST.get('reservation_amount')
#        total_amount = request.POST.get('total_amount')
#        user_id = request.POST.get('user_id')
#        department_id = request.POST.get('department_id')
#        django_cursor = connection.cursor()
#        cursor = django_cursor.connection.cursor()
#        salida = cursor.var(cx_Oracle.NUMBER)
#        cursor.callproc('ADD_RESERVATION',[check_in,check_out,qty_customers,reservation_amount,total_amount,user_id,department_id,salida])
#        
#        response = salida.getvalue()
#        
#        return JsonResponse(response, safe= False)

# funcion helper para ejecutar consultas a la bd,
# ademas rescata columnas de la consulta y las implementa como "clave" en el json a retornar
def execute_to_dict(query, params=None):
    with connection.cursor() as c:
        c.execute(query, params or [])
        names = [col[0].lower() for col in c.description]
        return [dict(list(zip(names, values))) for values in c.fetchall()]



def execute_proc(proced_almac,params=None):
    django_cursor = connection.cursor()
    
    #cursor LLAMA (permite conectar con oracle SIN orm)
    cursor = django_cursor.connection.cursor()
    
    # cursor de salida (que RECIBE)
    out_cursor = django_cursor.connection.cursor()
    
    cursor.callproc(proced_almac,params)
    
    return out_cursor

    #with connection.cursor() as c:
    #    c.execute(query, params or [])
    #    names = [col[0].lower() for col in c.description]
    #    return [dict(list(zip(names, values))) for values in c.fetchall()]    