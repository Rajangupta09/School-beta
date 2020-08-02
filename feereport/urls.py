from django.urls import path
from . import views

urlpatterns = [
    path('searchDefaulter/', views.search_defaulter, name="searchDefaulter"),
    # path('feeCollectionReportFilter/', views.feeCollectionReportFilter.as_view(), name="feeCollectionReport"),
    # # path('feeCollectionReport_pdf/', views.fee_collection_report_pdf, name="feeCollectionReport_pdf"),
    # path('feeCollectionReport/<int:classSection>/<str:mode>/<int:month>/<int:year>',
    #      views.FeeCollectionReport.as_view(), name="FeeCollectionReport"),
     path('feeCollectionReport/', views.fee_collection_report, name="feeCollectionReport"),
     path('feeCollectionReportsort/', views.fee_collection_report_sort, name="feeCollectionReportsort"),
     path('feeCollectionReportfilter/', views.fee_collection_report_filter, name="feeCollectionReportfilter"),
    path('feeCollectionReportPdf/', views.fee_collection_report_pdf, name="feeCollectionReportpdf"),
    path('feeCollectionReportcsv', views.file_load_view, name="feeCollectionReportcsv"),
]
