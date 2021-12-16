from django.http import response
from django.shortcuts import render
from dateutil.relativedelta import relativedelta
from .forms import TimeReportForm, TimeDashBoard
from outlet.models import posmReport, outletInfo, tableReport, report_sale, consumerApproachReport, giftReport, Campain
from .test import date_generator, revenue_char_bar, sum_value_iv
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.http import JsonResponse
# Create your views here.


def sum(a, b):
    return int(int(a) + int(b))

def percent(a,b):
    return (int(a)*100)/(int(b))

# login_required
#ADMIN HVN
class ListOutletDashbordView(ListView):
    model = outletInfo
    context_object_name = 'list_outlet_view'
    paginate_by = 25
    template_name = 'dashboard/management.html'

def list_outlet_approval(request):
    count = outletInfo.objects.filter(created_by_HVN = False).count()
    outlet = outletInfo.objects.filter(created_by_HVN = False)
    
    return render(request, 'dashboard/outlet-approval.html', {'list_outlet_False':outlet})

#HVN
def outlet_approval_byHVN(request):
    if request.is_ajax and request.method == "POST":
        arr = request.POST.get('arr')
        a = arr.split(',')
        for i in a:
            print(int(i))
            outlet = outletInfo.objects.get(id=i)
            outlet.created_by_HVN = True
            outlet.save()

        return JsonResponse({'created': 'success'})

#HVN
def delete_outlet_byHVN(request):
    if request.is_ajax and request.method == "POST":
        arr = request.POST.get('arr')
        a = arr.split(',')
        array = []
        for i in a:
            print(int(i))
            outlet = outletInfo.objects.get(id=i)
            outlet.delete()

        return JsonResponse({'created': 'success'})

# def sum_revenue(request):
#     user = request.user
#     form_calculate = TimeReportForm(request.GET)
        
#     if form_calculate.is_valid():
#         from_date = form_calculate.cleaned_data["from_date"]
#         to_date = form_calculate.cleaned_data["to_date"]
#         print(type(from_date))
#         all_outlet =outletInfo.objects.filter(compain='TAB_TGR')
#         for outlet in all_outlet: 
#             tb = tableReport.objects.filter(created__gte=from_date, oulet=outlet).filter(created__lte=to_date, compain='TAB_TGR')
        


#         # chart
#         dump = revenue_char_bar(tb, from_date, to_date)
#     return render(request,"dashboard/dashboard.html", {'text':[20,30,40,10]}) 
#         #return render(request,"report/dashboard.html",{ "from_date":from_date,"to_date":to_date,"chart":dump}) 
def sum_revenue(request):
    
    CP = get_object_or_404(Campain, program='tigerTP')
    total_table = 0
    total_table_HVN = 0
    total_brand_table = 0
     
    table_rp = tableReport.objects.filter(campain=CP)
    for tb in table_rp: 
        total_table = sum(total_table, tb.total_table)
        total_table_HVN = sum(total_table_HVN, tb.HVN_table)
        total_brand_table = sum(total_brand_table, tb.brand_table)
        
    a = percent(total_table_HVN, total_table)
    b = percent(total_brand_table, total_table)
    c=100-a-b
    
    ##################################
    customer_report = consumerApproachReport.objects.filter(campain=CP)
    sum_Total_Consumers = 0
    total_consumers_approach = 0
    total_consumers_brough = 0
    for cus_rp in customer_report:
        total_consumers_approach = sum(total_consumers_approach, cus_rp.consumers_approach)
        sum_Total_Consumers = sum(sum_Total_Consumers, cus_rp.Total_Consumers)
        total_consumers_brough = sum(total_consumers_brough, cus_rp.consumers_brough)
    Average_reach = percent(total_consumers_approach, sum_Total_Consumers)
    Average_conversion = percent(total_consumers_brough, total_consumers_approach)

    
    return render(request,"dashboard/dashboard.html", {'table_report':[a, b, c], 'total_consumers_approach':total_consumers_approach,
        'sum_Total_Consumers':sum_Total_Consumers,'total_consumers_brough':total_consumers_brough,
        'Average_reach':Average_reach, 'Average_conversion':Average_conversion}) 
        #return render(request,"report/dashboard.html",{ "from_date":from_date,"to_date":to_date,"chart":dump}) 
