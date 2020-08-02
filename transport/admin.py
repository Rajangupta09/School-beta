from django.contrib import admin
from .models import (Vehicle, Routes, Driver, Stoppage,
                     RouteVehicle, RouteDetail)
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.
# admin.site.register(Vehicle)

admin.site.register(Driver)
admin.site.register(Routes)
admin.site.register(RouteVehicle)
admin.site.register(RouteDetail)
admin.site.register(Stoppage)


class VehicleList(resources.ModelResource):

    class Meta:
        model = Vehicle
        exclude = ('id', )


class VehicleAdmin(ImportExportModelAdmin):
    resource_class = VehicleList


admin.site.register(Vehicle, VehicleAdmin)
