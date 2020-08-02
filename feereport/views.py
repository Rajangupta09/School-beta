from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from classform.models import ClassRoom, ClassRoomStudent
from fees.models import Fee, FeeCategory, FeeCycle, FeeDiscount, ClassSectionFees, Fine
from django.contrib.auth.decorators import login_required
from django.views import generic as generic_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.utils.timezone import localdate
from datetime import date
from datetime import timedelta
#3rd part views
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.urls import reverse_lazy
from io import StringIO
from csv import DictWriter
import xlwt
from django.http import HttpResponse
import csv
from operator import itemgetter
# Create your views here.

fee_dict={}
@login_required
def search_defaulter(request):
    if request.method == "GET":
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul',
                  'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        class_section = request.GET.get('class_room')
        if class_section:
            class_room = ClassRoom.objects.get(classSection=class_section)
            fees = Fee.objects.filter(classSection=class_room)
            try:
                class_fees = ClassSectionFees.objects.get(
                    classSection=class_room).fees
            except:
                messages.info(request, 'Add Fee for the selected class first!')
                redirect('searchDefaulter')
            months_not_paid = []
            balance_remaining = []
            for f in fees:
                s = ""
                months_paid = f.monthsPaid.split(',')
                for m in months:
                    if m not in months_paid:
                        s += '-'+m
                months_not_paid.append(s)
                balance_remaining.append(class_fees-f.amount)
            # print(fees, months_not_paid, balance_remaining)
            mylist = zip(fees, months_not_paid, balance_remaining)
            context = {
                'mylist': mylist,
                'values': request.GET,
                "class_rooms": ClassRoom.objects.all()
            }
            return render(request, 'feereport/defaulterSearch.html', context)

    return render(request, 'feereport/defaulterSearch.html', {"class_rooms": ClassRoom.objects.all()})
@login_required
def fee_collection_report_filter(request):
    return render(request,'feereport/feeCollectionfilter.html',{'classrooms':ClassRoom.objects.all()})


@login_required
def fee_collection_report(request):
    if request.method == "GET":
        fees = Fee.objects.all()
        if "classSection" in request.GET:
            classSection = request.GET['classSection']
            if classSection:
                class_room = ClassRoom.objects.get(classSection=classSection)
                fees = fees.filter(classSection=class_room).order_by('-submissionDate')
        if "mode" in request.GET:
            mode = request.GET['mode']
            if mode:
                fees = fees.filter(payment_method__contains=mode).order_by('-submissionDate')
        if "month" in request.GET:
            month = request.GET['month']
            if month:
                fees = fees.filter(submissionDate__month=month).order_by('-submissionDate')
        if "year" in request.GET:
            year = request.GET['year']
            if year:
                fees = fees.filter(submissionDate__year=year).order_by('-submissionDate')
        total = 0
        for paid in fees:
            total =  total + paid.amount
        fee_dict['fees'] = fees
        fee_dict['total'] = total
        return render(request, 'feereport/feeCollectionReport.html', {"fees": fees,'classrooms':ClassRoom.objects.all(),'total':total,'date':date.today().strftime('%Y-%m-%d'), 'yesterday': (date.today() - timedelta(days = 1)).strftime('%Y-%m-%d'),'month':date.today().month})

    return render(request, 'feereport/feeCollectionReport.html')

def fee_collection_report_sort(request):
    if request.method == 'GET':
        da = request.GET['sort']
        fees = Fee.objects.all()
        sorted_fee = fees.filter(submissionDate=da)
        return render(request,'feereport/feeCollectionReport.html',{'date':da ,'fees':sorted_fee})
    return render(request,'feereport/feeCollectionReport.html')

def fee_collection_report_pdf(request):
    data = {
        'fees': fee_dict['fees'],
        'total': fee_dict['total']
    }
    template = get_template("feereport/feeCollectionReportSort.html")
    data_p = template.render(data)
    response = BytesIO()

    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
    if not pdfPage.err:
        return HttpResponse(response.getvalue(), content_type="application/pdf")
    else:
        return HttpResponse("Error Generating PDF")

# @require_http_methods(["GET"])
def file_load_view(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(["Name", "Admission_no", "Submission_date", "Mobile Number", "Class Section", "Months paid" , 'Amount Paid'])

    users = fee_dict.get('fees')
    result = list(map(itemgetter("x", "y"), users))
    print(users)
    for user in users:
        writer.writerow(user)
    return response
    # response = HttpResponse(content_type='application/ms-excel')
    # response['Content-Disposition'] = 'attachment; filename="users.xls"'

    # wb = xlwt.Workbook(encoding='utf-8')
    # ws = wb.add_sheet('Users Data') # this will make a sheet named Users Data

    # # Sheet header, first row
    # row_num = 0

    # font_style = xlwt.XFStyle()
    # font_style.font.bold = True

    # columns = ["Name", "Admission_no", "Submission_date", "Mobile Number", "Class Section", "Months paid" , 'Amount Paid']

    # for col_num in range(len(columns)):
    #     ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column

    # # Sheet body, remaining rows
    # font_style = xlwt.XFStyle()
    # fees = fee_dict['fees']
    # rows = Fee.objects.all().values_list('classSection','payment_method','submissionDate')
    # for row in rows:
    #     row_num += 1
    #     for col_num in rows:
    #         ws.write(row_num, col_num, row[col_num], font_style)

    # wb.save(response)

    # return response