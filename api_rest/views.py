import base64
import json
from django.views import View
from .models import *
from django.http import JsonResponse
from django.forms import model_to_dict
from  django.db import connection


class EmployeeLoginView(View):
    def post(self,request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        user_id = 0
        session = ''
        error = ''
        if post_data['login'] == 1:
            try:
                query = "SELECT CASE WHEN (SELECT count(session_id) FROM employee_session WHERE user_id_id = {} ) <= 0 THEN to_char('UNREGISTER') ELSE (SELECT to_char(session_id) FROM employee_session WHERE user_id_id = {} ) END AS \"session_id\" FROM DUAL".format(post_data['user_id'],post_data['user_id'])
                result = cursor.execute(query)
                for i in result:
                    session = i[0]
            except:
                error = "ERROR"
        elif post_data['login'] == 2:
            try:
                login = cursor.callfunc("FN_LOGIN",int ,[post_data['username'],post_data['password']])
                connection.commit()
                user_id = login
            except:
                error = "ERROR"

        result_data = {
            "user_id":user_id,
            "session": session,
            "error": error
        }

        return JsonResponse(result_data, safe=False)

class EmployeeView(View):
    def post(self,request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        user_id = 0
        full_name = ""
        position = ""
        session_id = ""
        error = "NO ERROR"
        if post_data['user_id'] > 0:
            try:
                query = "SELECT es.user_id ,INITCAP(e.name) || ' ' || INITCAP(e.last_name) as \"full_name\" ,et.position ,es.session_id FROM employee_session es JOIN employee e ON es.user_id = e.id JOIN employee_type et ON e.employee_type_id = et.id WHERE es.user_id = {}".format(post_data['user_id'])
                result = cursor.execute(query)
                for i in result:
                    user_id = i[0]
                    full_name = i[1]
                    position = i[2]
                    session_id = i[3]
            except:
                error = "ERROR"

            result_data = {
                "user_id":user_id,
                "full_name":full_name,
                "position":position,
                "session_id":session_id,
                "error":error
            }
        return JsonResponse(result_data, safe=False)

class EmployeeDetailView(View):
    def get(self, request, pk):
        employee = Employee.objects.get(pk=pk)
        return JsonResponse(model_to_dict(employee))

class EmployeeLogoutView(View):
    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        print(post_data)
        error = "NO ERROR"
        try:
            query = "update employee_session set session_id = 'NO SESSION' where user_id = {}".format(post_data['user_id'])
            result = cursor.execute(query)
            connection.commit()
        except:
            error = "ERROR"

        result_data = {
            "error":error    
        }
        return JsonResponse(result_data, safe=False)

class ExtraServicesView(View):
    def get(self, request):
        extra_services = Services.objects.all()
        return JsonResponse(list(extra_services.values()), safe=False)

class AddExtraServicesView(View):
    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        extra_services = cursor.callfunc("FN_ADD_SERVICE",int,[post_data['service_type_id'],post_data['name'],post_data['price'],post_data['location'],post_data['available']])
        connection.commit()
        extra_services_response = {
            "response":extra_services
        } 
        return JsonResponse(extra_services_response, safe=False)

class DepartmentView(View):
    def get(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        out_cursor = django_cursor.connection.cursor()
        cursor.callproc('GET_DEPARTMENT',[out_cursor])
        department = []
        for i in out_cursor:
            department_json= {
                "address":i[0],
                "qty_room":i[1],
                "price":i[2],
                "commune":i[3],
                "department_type":i[4],
                "short_description":i[5],
                "long_description":i[6],
                "department_image":i[7] if i[7] == None else str(base64.b64encode(i[7].read()), 'utf-8')
            } 
            department.append(department_json)

        #print(department)
        return JsonResponse(department, safe=False)

class AddDepartment(View):
    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        image = base64.b64decode(post_data['department_image'])
        department = cursor.callfunc("FN_ADD_DEPARTMENT",int,[post_data['address'],post_data['qty_rooms'],post_data['price'],post_data['commune'], post_data['department_type'], post_data['short_description'], post_data['long_description'], image])
        connection.commit()
        department_response = {
            "response":department
        }
        return JsonResponse(department_response, safe=False) 

class CommuneView(View):
    def get(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        out_cursor = django_cursor.connection.cursor()
        cursor.callproc('GET_ALL_COMMUNES', [out_cursor])
        commune = []
        for i in out_cursor:
            commune_json = {
                "id": i[0],
                "commune":i[1],
                "id_region_id":i[2]
            }
            commune.append(commune_json)
        return JsonResponse(commune, safe=False)


