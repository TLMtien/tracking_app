from django.http import response
from django.shortcuts import render
from dateutil.relativedelta import relativedelta

from dashboard.models import KPI
#from .forms import TimeReportForm, TimeDashBoard
from outlet.models import posmReport, outletInfo, tableReport, report_sale, consumerApproachReport, giftReport, Campain
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.http import JsonResponse
from .forms import KPIForm
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from .charts import pie_chart, total_consumers_reached, HNK_volume_sale, top10_outlet, volume_achieved_byProvince, gift
# Create your views here.

# tigerTP 1
# tigerFA 2
# tigerHZA 3
# heineken 4
# heineken_hnk 5
# STB 6
# bivina 7
# Larue 8
# Larue_SPE 9
def sum(a, b):
    return int(int(a) + int(b))

def percent(a,b):
    return (int(a)*100)/(int(b))

# class dash_board_View(DetailView):
#     model = Campain
#     template_name = 'dashboard/dashboard.html'

#dashboard_view
login_required
def dash_board_View(request, campainID):
    campain = Campain.objects.get(id=campainID)
    return render(request,'dashboard/dashboard.html')

#HVN
login_required
def List_outlet_management(request, campainID):
    campain = Campain.objects.get(id=campainID)
    all_outlet = outletInfo.objects.filter(compain=campain)
    return render(request,  'dashboard/management.html', {'list_outlet_view':all_outlet})

login_required
def management_View(request):
    #campain = Campain.objects.get(id=campainID)
    return render(request,'dashboard/management.html')
# login_required
#ADMIN HVN
# class ListOutletDashbordView(ListView):
#     model = outletInfo
#     context_object_name = 'list_outlet_view'
#     paginate_by = 25
#     template_name = 'dashboard/management.html'

def listOutletInformation(request, campainID):
    campain = Campain.objects.get(id=campainID)
    list_outlet = outletInfo.objects.filter(compain = campain)
    
    return render(request, 'dashboard/management.html', {'list_outlet_view' : list_outlet})

def list_outlet_approval(request, campainID):
    campain = Campain.objects.get(id=campainID)
    outlet = outletInfo.objects.filter(created_by_HVN = False, compain = campain)
    
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

        campain = Campain.objects.all()
        for i in campain:
            print(i.program, i.id)
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


def KPI_view(request, campainID):
    campain = Campain.objects.get(id=campainID)
    kpi = KPI.objects.filter(campain=campain)
    return render(request, 'dashboard/kpi-setting.html', {'all_kpi':kpi})

#HVN  create_KPI
def create_KPI(request, campainID):
    campain = Campain.objects.get(id=campainID)
    if request.method == "POST":
        form = KPIForm(request.POST)
        if form.is_valid():
            volume_achieved = form.cleaned_data.get('volume_achieved')
            table_share = form.cleaned_data.get('table_share')
            consumer_reached = form.cleaned_data.get('consumer_reached')
            conversion = form.cleaned_data.get('conversion')
            start_day = request.POST.get('start_day')
            kpi = KPI.objects.create(user=request.user, campain=campain, volume_achieved=volume_achieved,
            table_share=table_share, consumer_reached=consumer_reached, conversion=conversion, start_day=start_day)
    
            kpi.save()
            all_kpi = KPI.objects.filter(campain=campain)
            return render(request, "dashboard/kpi-setting.html", {'all_kpi':all_kpi})
    else:
        form = KPIForm()
        return render(request,"dashboard/create-kpi.html", {'form':form})

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

##################################################
def charts_views(request):
    id =7
    pie=pie_chart(id)
    #print(pie)
    customer_app = total_consumers_reached(id)
    Volume_sale = HNK_volume_sale(id)
    top10 = top10_outlet(id)
    target_volume_achieved =volume_achieved_byProvince(id)
    gift_rp = gift(id)
    print(top10)
    return render(request, 'dashboard/test----test-----test.html', {'text':pie, 'customer_app':customer_app[0],'target_volume_achieved':target_volume_achieved, 
    'percent_customer_app':customer_app[1], 'Volume_sale':Volume_sale, 'top10_sale':top10[0], 'top10_table':top10[1], 'top10_name':top10[2], 'gift_rp':gift_rp[0], 'gift_name' : gift_rp[1]})

######################################
import datetime
import xlwt
from outlet.models import tableReport, report_sale
from datetime import datetime
from django.http import HttpResponse

def export(request, campainID):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename={}.xls'.format(str(datetime.now()))
    wb = xlwt.Workbook(encoding='utf-8') 
    ws=wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    Cp = Campain.objects.get(id=campainID)
    all_outlet = outletInfo.objects.filter(compain=Cp)

    colums = ['Province', 'Outlet ID', 'Type', 'Area', 'Address', 'Outlet name', 'HNK Volume Sales', 'HNK Tables', 'HVB Table Share', 'Others', 'Total Tables','Consumers Approach','Pin sạc','Ba lô', 'Bình Nước', 'Áo thun', 'Loa Bluetooth', 'Ly', 'Pin sạc','Ba lô', 'Bình Nước', 'Áo thun', 'Loa Bluetooth', 'Ly']

    if campainID == 4:
        colums = ['Province', 'Outlet ID', 'Type', 'Area', 'Address', 'Outlet name', 'HNK Volume Sales', 'HNK Tables', 'HVB Table Share', 'Others', 'Total Tables','Consumers Approach','Pin sạc','Ba lô', 'Bình Nước', 'Áo thun', 'Loa Bluetooth', 'Ly', 'Pin sạc','Ba lô', 'Bình Nước', 'Áo thun', 'Loa Bluetooth', 'Ly']

    if campainID == 5:
        colums = ['Province', 'Outlet ID', 'Type', 'Area', 'Address', 'Outlet name', 'HNK Volume Sales', 'HNK Tables', 'HVB Table Share', 'Others', 'Total Tables','Consumers Approach','Heineken Alu', 'Ba lô', 'Combo Thời Trang', 'Combo Thể Thao', 'Heineken Alu', 'Ba lô', 'Combo Thời Trang', 'Combo Thể Thao']

    if campainID == 7:
        colums = ['Province', 'Outlet ID', 'Type', 'Area', 'Address', 'Outlet name', 'HNK Volume Sales', 'HNK Tables', 'HVB Table Share', 'Others', 'Total Tables','Consumers Approach','Túi du lịch', 'Đồng Hồ Treo Tường', 'Bình Nước 1,6L', 'Ly', 'Túi du lịch', 'Đồng Hồ Treo Tường', 'Bình Nước 1,6L', 'Ly']
    
    if campainID == 8:
        colums = ['Province', 'Outlet ID', 'Type', 'Area', 'Address', 'Outlet name', 'HNK Volume Sales', 'HNK Tables', 'HVB Table Share', 'Others', 'Total Tables','Consumers Approach','Áo thun', 'Thùng 12 Lon', 'Nón', 'Ly', 'Áo thun', 'Thùng 12 Lon', 'Nón', 'Ly']

    for col_num in range(len(colums)):
        ws.write(row_num, col_num, colums[col_num], font_style)

    font_style = xlwt.XFStyle()
    
    from_date = request.POST.get('from-date')
    to_date = request.POST.get('to-date')
  
    for outlet in all_outlet:
        count_list_rp_sale = report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet = outlet).filter(created__lte=to_date, campain = Cp, outlet = outlet).count()
        list_rp_table = tableReport.objects.filter(created__gte=from_date, campain = Cp, outlet = outlet).filter(created__lte=to_date, campain = Cp, outlet = outlet)
        list_rp_sale = report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet = outlet).filter(created__lte=to_date, campain = Cp, outlet = outlet)
        list_rp_consumer = consumerApproachReport.objects.filter(created__gte=from_date, campain = Cp, outlet = outlet).filter(created__lte=to_date, campain = Cp, outlet = outlet)
        count_list_rp_consumer = consumerApproachReport.objects.filter(created__gte=from_date, campain = Cp, outlet = outlet).filter(created__lte=to_date, campain = Cp, outlet = outlet).count()
        list_gift_rp = giftReport.objects.filter(created__gte=from_date, campain = Cp, outlet = outlet).filter(created__lte=to_date, campain = Cp, outlet = outlet)
        count_list_gift_rp = giftReport.objects.filter(created__gte=from_date, campain = Cp, outlet = outlet).filter(created__lte=to_date, campain = Cp, outlet = outlet).count()
        total_sale = 0
        total_HNK = 0
        total_HVB = 0
        total_other_beer = 0
        total_table = 0
        total_consumers_approach =0
        total_gift1_receive = 0
        total_gift2_receive = 0
        total_gift3_receive = 0
        total_gift4_receive = 0
        total_gift5_receive = 0
        total_gift6_receive = 0

        total_gift1_given = 0
        total_gift2_given = 0
        total_gift3_given = 0
        total_gift4_given = 0
        total_gift5_given = 0
        total_gift6_given = 0
        if count_list_rp_sale > 0 or count_list_rp_consumer> 0 or count_list_gift_rp>0:
            for rp_sale in list_rp_sale:
                total_sale = sum(total_sale, rp_sale.beer_brand)
            for rp_table in list_rp_table:
                total_HNK = sum(total_HNK, rp_table.brand_table)
                total_HVB = sum(total_HVB, rp_table.HVN_table)
                total_other_beer = sum(total_other_beer, rp_table.other_beer_table)
                total_table = sum(total_table, rp_table.total_table)
            for consumer in list_rp_consumer:
                total_consumers_approach = sum(total_consumers_approach, consumer.consumers_approach)
            for gift in list_gift_rp:
                total_gift1_receive = sum(total_gift1_receive, gift.gift1_received)
                total_gift2_receive = sum(total_gift2_receive, gift.gift2_received)
                total_gift3_receive = sum(total_gift3_receive, gift.gift3_received)
                total_gift4_receive = sum(total_gift4_receive, gift.gift4_received)
                total_gift5_receive = sum(total_gift5_receive, gift.gift5_received)
                total_gift6_receive = sum(total_gift6_receive, gift.gift6_received)

                total_gift1_given = sum(total_gift1_given, gift.gift1_given)
                total_gift2_given = sum(total_gift2_given, gift.gift2_given)
                total_gift3_given = sum(total_gift3_given, gift.gift3_given)
                total_gift4_given = sum(total_gift4_given, gift.gift4_given)
                total_gift5_given = sum(total_gift5_given, gift.gift5_given)
                total_gift6_given = sum(total_gift6_given, gift.gift6_given)

            if campainID == 4:
                list = [outlet.province, outlet.ouletID, outlet.type, outlet.area, outlet.outlet_address, outlet.outlet_Name, total_sale, total_HNK, total_HVB, total_other_beer, total_table, total_consumers_approach, total_gift1_receive, total_gift2_receive, total_gift3_receive, total_gift4_receive, total_gift5_receive, total_gift6_receive, total_gift1_given, total_gift2_given, total_gift3_given, total_gift4_given, total_gift5_given, total_gift6_given]
                
                row_num +=1
                for col_num in range(len(list)):
                    ws.write(row_num, col_num, str(list[col_num]), font_style)
            
            else:
                list = [outlet.province, outlet.ouletID, outlet.type, outlet.area, outlet.outlet_address, outlet.outlet_Name, total_sale, total_HNK, total_HVB, total_other_beer, total_table, total_consumers_approach, total_gift1_receive, total_gift2_receive, total_gift3_receive, total_gift4_receive, total_gift1_given, total_gift2_given, total_gift3_given, total_gift4_given]
                row_num +=1
                
                for col_num in range(len(list)):
                    ws.write(row_num, col_num, str(list[col_num]), font_style)
                
    wb.save(response) 
    return response
        
    