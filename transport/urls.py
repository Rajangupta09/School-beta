"""
Urls for notice app
"""

from django.urls import path
from . import views

urlpatterns = [
    path('addVehicle', views.vehicle_register, name="addVehicle"),
    # path('addDriver', views.driver_register, name="addDriver"),
    path('driver-list/<int:empID>/edit-driver/',
         views.DriverUpdate.as_view(), name="editDriver"),
    path('driver-list/', views.DriverList.as_view(), name="driverList"),


    path('route-list/<int:routeID>/<int:detailID>/edit-shift/',
         views.ShiftUpdateView.as_view(), name="editShift"),

    path('route-list/<int:routeID>/<int:detailID>/archive-shift/',
         views.shift_archive_view, name="archiveShift"),

    path('route-list/<int:routeID>/<int:detailID>/delete-shift/',
         views.ShiftDeleteView.as_view(), name="deleteShift"),

    path('route-list/<int:routeID>/edit-route/',
         views.RouteUpdateView.as_view(), name="editRoute"),

    path('route-list/<int:routeID>/archive-route/',
         views.route_archive_view, name="archiveRoute"),


    path('route-list/<int:routeID>/delete-route/',
         views.RouteDeleteView.as_view(), name="deleteRoute"),


    path('route-list/', views.RouteListView.as_view(), name="routeList"),
    path('add-route/', views.RouteRegisterView.as_view(), name="addRoute"),
    path('vehicleList', views.vehicle_list, name="vehicleList"),
    path('vehicleListExcel', views.vehicle_list_excel, name="vehicleListExcel"),
    path('vehicleListPdf', views.vehicle_list_pdf, name="vehicleListPdf"),

    path('route-attendence-list/<str:filter>/<int:filter_id>/<slug:month>/pdf/', views.RouteAttendenceListPDF.as_view(),
         name="routeAttendenceListPDF"),

    path('route-attendence-list/<str:filter>/<int:filter_id>/<slug:month>/', views.RouteAttendenceList.as_view(),
         name="routeAttendenceList"),
    path('route-attendence-list/', views.RouteAttendenceListFilter.as_view(),
         name="routeAttendenceListFilter"),

    path('routeReportPdf', views.route_report_pdf, name="routeReportPdf"),
    path('mark-route-attendence/<int:route_detail_id>/',
         views.MarkRouteAttendence.as_view(), name="markRouteAttendence"),
    path('mark-route-attendence/', views.MarkAttendenceFilter.as_view(),
         name="markRouteAttendenceFilter"),
    path('routeReport', views.route_report, name="routeReport"),
    path('getStudentRoute', views.get_student_transport_route,
         name="getStudentRoute"),
]
