from django.shortcuts import render
from dateutil.relativedelta import relativedelta

# Create your views here.
# def sum_revenue(request):
#     user = request.user
#     if user.is_admin:
#         customers = User.objects.exclude(profile__isnull=True)
#         form_calculate = CalculateRevenueForm(request.GET)
        
#     if form_calculate.is_valid():
#         from_date = form_calculate.cleaned_data["from_date"]
#         to_date = form_calculate.cleaned_data["to_date"]
#         projects = Project.objects.all()
#         print(type(from_date))

#         iv_isp = InvoiceISP.objects.filter(
#             date_upload__gte=from_date).filter(date_upload__lte=to_date)
#         value_iv_isp = sum_value_iv(iv_isp)

#         iv_general = InvoiceGeneral.objects.filter(
#             date_upload__gte=from_date).filter(date_upload__lte=to_date)
#         value_iv_general = sum_value_iv(iv_general)

#         iv_customer = InvoiceCustomer.objects.filter(
#             date_upload__gte=from_date).filter(date_upload__lte=to_date)
#         value_iv_customer = sum_value_iv(iv_customer)

#         value_iv_isp_not_pay = sum_value_iv(iv_isp.filter(payment=False))
#         value_iv_customer_not_pay = sum_value_iv(iv_customer.filter(paymented=False))
#         value_iv_general_not_pay = sum_value_iv(iv_general.filter(payment=False))

#         total_profit = value_iv_customer - (value_iv_general + value_iv_isp)

#         vendors = Vendor.objects.all()

#         # chart
#         dump = revenue_char_bar(iv_isp, iv_general, iv_customer, from_date, to_date)

#         return render(request,"user/calculate_revenue.html",{"customers":customers,"total_revenue":value_iv_customer,"accrued_expenses":value_iv_general + value_iv_isp,"total_profit":total_profit,"value_iv_general":value_iv_general,"value_iv_isp":value_iv_isp,"value_iv_isp_not_pay":value_iv_isp_not_pay,"value_iv_customer_not_pay":value_iv_customer_not_pay,"value_iv_general_not_pay":value_iv_general_not_pay,"from_date":from_date,"to_date":to_date,"iv_general":iv_general,"vendors":vendors,"projects":projects,"chart":dump}) 
