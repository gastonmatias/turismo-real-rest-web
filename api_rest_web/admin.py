from django.contrib import admin

# para poder borrar users qe tengan token valido activo (https://stackoverflow.com/questions/40604877/how-to-delete-a-django-jwt-token)
#class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):
#    def has_delete_permission(self, *args, **kwargs):
#        return True # or whatever logic you want
#
#admin.site.unregister(token_blacklist.models.OutstandingToken)
#admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)   

from django.contrib import admin
from api_rest.models import Region,Commune,DepartmentType,Department,Services,Reservation,ServicesType

# Register your models here.
#admin.site.register(User)
admin.site.register(Region)
admin.site.register(Commune)
admin.site.register(DepartmentType)
admin.site.register(Department)
admin.site.register(Services)
admin.site.register(ServicesType)
admin.site.register(Reservation)
