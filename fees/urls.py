from django.urls import path
from . import views
# from wkhtmltopdf.views import PDFTemplateView
from . import views as web_views

urlpatterns = [
    path('addFine/', views.add_fine, name="addFine"),
    path('addFeeClass/', views.add_fee_class, name="addFeeClass"),

    path('fee-categories/<int:pk>/delete', views.FeeCategoryDeleteView.as_view(),
         name="deleteFeeCategory"),

    path('fee-categories/<int:pk>/edit/', views.FeeCategoryUpdateView.as_view(),
         name="editFeeCategory"),

    path('fee-categories/', views.FeeCategoryCreateView.as_view(),
         name="feeCategories"),

    path('fee-cycles/<int:pk>/delete/', views.FeeCycleDeleteView.as_view(),
         name="deleteFeeCycle"),

    path('fee-cycles/<int:pk>/edit/', views.FeeCycleUpdateView.as_view(),
         name="editFeeCycle"),

    path('fee-cycles/', views.FeeCycleCreateView.as_view(),
         name="feeCycles"),

    path('fee-configurations/<int:pk>/delete/', views.FeeConfigurationDeleteView.as_view(),
         name="deleteFeeConfiguration"),

    path('fee-configurations/<int:pk>/edit/', views.FeeConfigurationUpdateView.as_view(),
         name="editFeeConfiguration"),

    path('fee-configurations/', views.FeeConfigurationCreateView.as_view(),
         name="feeConfigurations"),

    path('fee-discounts/<int:pk>/delete/', views.FeeDiscountDeleteView.as_view(),
         name="deleteFeeDiscount"),

    path('fee-discounts/<int:pk>/edit/', views.FeeDiscountUpdateView.as_view(),
         name="editFeeDiscount"),

    path('fee-discounts/', views.FeeDiscountCreateView.as_view(),
         name="feeDiscounts"),

    path('student-discounts/<int:pk>/delete/', views.StudentDiscountDeleteView.as_view(),
         name="deleteStudentDiscount"),

    path('student-discounts/<int:pk>/edit/', views.StudentDiscountUpdateView.as_view(),
         name="editStudentDiscount"),

    path('student-discounts/', views.StudentDiscountCreateView.as_view(),
         name="studentDiscounts"),

    path('fee-head-mapping/', views.FeeHeadMappingFilter.as_view(),
         name="feeHeadMappingFilter"),

    path('fee-head-mapping/<int:admission_no>', views.FeeHeadMappingView.as_view(),
         name="feeHeadMapping"),

    path('collect-fee', views.fee_collection, name="collectFee"),
    path('fee-slip/<int:admission_no>/<int:session_id>/', views.fee_slip, name="fee_slip"),
    path('fee-collection/', views.FeeCollectionFilter.as_view(),
         name="feeCollectionFilter"),
    path('fee-collection/<int:admission_no>/<int:session_id>/',
         views.FeeCollection.as_view(), name="feeCollection"),

]
