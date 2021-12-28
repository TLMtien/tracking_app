from django.http import response
from django.shortcuts import render
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from dashboard.models import KPI
#from .forms import TimeReportForm, TimeDashBoard
from outlet.models import posmReport, outletInfo, tableReport, report_sale, consumerApproachReport, giftReport, Campain
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.http import JsonResponse
from .forms import KPIForm

from users.models import SalePerson, NewUser
import json
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from .charts import pie_chart, total_consumers_reached, HNK_volume_sale, top10_outlet, volume_achieved_byProvince, gift, VOLUME_PERFORMANCE, activation_progress, get_outlet_province, getAll_report_outlet, get_outlet_type, get_outlet, get_gift_scheme
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
def reverse(A):
    try:
        a = A[9]
        b = A[8]
        c = A[7]
        d = A[6]
        e = A[5]
        f = A[4]
        g = A[3]
        h = A[2]
        j = A[1]
        k = A[0]
        list = [a,b,c,d,e,f,g,h,j, k]
        return list
    except:
        pass

def append_array(gift_name):
    list_gift = []
    for gift in gift_name:
        list_gift.append([gift])
    return list_gift

def sum(a, b):
    return int(int(a) + int(b))

def percent(a,b):
    return round((int(a)*100)/(int(b)), 0)

# class dash_board_View(DetailView):
#     model = Campain
#     template_name = 'dashboard/dashboard.html'

#dashboard_view
login_required
def dash_board_View(request, campainID):
    campain = Campain.objects.get(id=campainID)
    return render(request,'dashboard/dashboard.html', {"cam_id":campainID})

#HVN
login_required
def List_outlet_management(request, campainID):
    campain = Campain.objects.get(id=campainID)
    all_outlet = outletInfo.objects.filter(compain=campain)
    return render(request,  'dashboard/management.html', {'list_outlet_view':all_outlet, "cam_id":campainID})

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

login_required
def ban_sp(request):
    if request.user.is_HVN:
        print(json.loads(request.body.decode('UTF-8')))
        data = json.loads(request.body.decode('UTF-8'))
        for user_id in data.get("array_id",[]):
            print(user_id)
            try:
                user = NewUser.objects.get(pk=int(user_id))
                user.is_active = False
                user.save()
                print("save")
            except:
                pass
        return JsonResponse({'status': 'okay'})

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
    return render(request, 'dashboard/kpi-setting.html', {'all_kpi':kpi, "cam_id":campainID})

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
            return render(request, "dashboard/kpi-setting.html", {'all_kpi':all_kpi, "cam_id":campainID})
    else:
        form = KPIForm()
        return render(request,"dashboard/create-kpi.html", {'form':form})


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
###############33
#Block user
login_required
def List_sp_management(request,campainID):
    if request.user.is_HVN:
        
        is_campain_owner = False
        campains = request.user.hvn.brand.all()
        for c in campains:
            if c.id == campainID:
                is_campain_owner = True
                break
        sale_person = SalePerson.objects.filter(brand__pk=campainID)
        
        
        print(sale_person)
        return render(request,  'dashboard/sp-info.html', {'sale_person':sale_person,"is_campain_owner":is_campain_owner, "cam_id":campainID})
##################################################
def charts_views(request, campainID):
    from_date = request.POST.get('from-date')
    
    to_date = request.POST.get('to-date')
    
    if from_date == '' or from_date==None:
        from_date = (date(2021,12,20))
    if to_date == '' or to_date==None:
        to_date = (date.today())

    print(from_date)
    id = campainID
    Cp = Campain.objects.get(id = campainID)
    table_rp = tableReport.objects.filter(created__gte=from_date, campain = Cp).filter(created__lte=to_date, campain = Cp)
    pie=pie_chart(id, table_rp)
    #print(pie)
    consumers_rp = consumerApproachReport.objects.filter(created__gte=from_date, campain = Cp).filter(created__lte=to_date, campain = Cp)
    report_customer = total_consumers_reached(id, consumers_rp)
    # HNK_volume_sale
    all_report_sale =  report_sale.objects.filter(created__gte=from_date, campain = Cp).filter(created__lte=to_date, campain = Cp)
    Volume_sale = HNK_volume_sale(id, all_report_sale)
    #VOLUME_PERFORMANCE
    all_outlet = outletInfo.objects.filter(created__gte=from_date, compain = Cp).filter(created__lte=to_date, compain = Cp)
    volume_per = VOLUME_PERFORMANCE(id, all_outlet)
    Average_brand_volume = [volume_per[2], volume_per[3]]
    # Top10
    top10 = top10_outlet(id, all_outlet)
    # volume_achieved_byProvince
    target_volume_achieved =volume_achieved_byProvince(id, all_outlet)
    #gift
    list_gift_rp = giftReport.objects.filter(created__gte=from_date, campain = Cp).filter(created__lte=to_date, campain = Cp)
    gift_rp = gift(id, list_gift_rp)
    # activation
    activation = activation_progress(id, all_outlet)

    print(list_gift_rp)
    per = 0
    if volume_per[1] != 0:
        per= percent(volume_per[0], volume_per[1])
    percent_volume = per
    print(per)
    return render(request, 'dashboard/dashboard.html', {'text':pie, 'target_volume_achieved':target_volume_achieved, 
     'Volume_sale':Volume_sale, 'top10_sale':top10[0], 'top10_table':top10[1], 'top10_name':top10[2], 'gift_rp':gift_rp[0], 'gift_name' : gift_rp[1],'array_gift': append_array(gift_rp[1]),'total_consumers':report_customer[0] , 'ctm_reached':report_customer[1], 'total_bought_consumers':report_customer[2], 'per_reached':report_customer[3], 'average_conversion':report_customer[4], 'actual_volume' : volume_per[0], 'target_volume': volume_per[1], 'percent_volume':percent_volume,'Average_brand_volume': Average_brand_volume, 'activation':activation[0],'total_activation':activation[1],  'top10_sale_reverse':top10[3], 'top10_table_reverse': top10[4], 'top10_name_reverse':top10[5], 'list_province':volume_per[4], 'list_name_outlet':volume_per[5], 'list_type':volume_per[6], "cam_id":campainID})


######
#filter_outlet_province
def filter_outlet_province(request, campainID):
    if request.is_ajax and request.method == "POST":
        array_province = request.POST.get('array_province') 
        
        
        print(array_province)
         
        province = array_province.split(',')

        list_outlet_chart = get_outlet_province(campainID, province)
        list_rp = getAll_report_outlet(campainID, list_outlet_chart[0])
        pie = pie_chart(campainID, list_rp[0])
        consumers_charts = total_consumers_reached(campainID, list_rp[1])
        gift_charts = gift(campainID, list_rp[2])
        volume_performance = VOLUME_PERFORMANCE(campainID, list_outlet_chart[0])
        Average_brand_volume = [volume_performance[2], volume_performance[3]]
        top_10 = top10_outlet(campainID, list_outlet_chart[0])
        activation = activation_progress(campainID, list_outlet_chart[0])
        print(province)
        print(consumers_charts)
        print(gift_charts)
        list_outlet = ''
        list_type = ''

        for outlet in list_outlet_chart[0]:
            list_outlet += f'''<tr>
                            <div class="sidebar-menu_sub">
                                <label>
                                        <input type="checkbox" class="sidebar-menu_checkbox" name="name_outlet"  value="{outlet.id}">
                                        <span class="checkmark"></span>
                                </label>
                                <p class="sidebar-menu_item">
                                        {outlet.outlet_Name}
                                </p>
                            </div>
                        </tr>
                        '''
        # for type in list_outlet_chart[1]:
        #     print(type)
        #     list_type += f'''<tr>
        #                         <div class="sidebar-menu_sub">
        #                             <label>
        #                                 <input type="checkbox"  class="sidebar-menu_checkbox" name="type_outlet" value = "{{type}}"> 
        #                                 <span class="checkmark"></span>
        #                             </label>
        #                             <p class="sidebar-menu_item">
        #                                {type}
        #                             </p>
        #                         </div>
        #                     </tr>
        #                 '''
        Consumers = f'''
                <div class="row-1">
                                    <div class="col-12">
                                        <div class="col-4">
                                            <p class="title">
                                                Total Consumers {consumers_charts[0]}
                                            </p>
                                        </div>
                                        <div class="col-4">
                                            <p class="title">
                                                Total Reached Consumers {consumers_charts[1]}
                                            </p>
                                        </div>
                                        <div class="col-4">
                                            <p class="title">
                                                Total Bought Consumers {consumers_charts[2]}
                                            </p>
                                        </div>
                                        
                                    </div>
                                </div>
                                <div class="row-2">
                                    <div class="col-12">
                                    
                                        <div class="col-6">
                                            <span class="number">Average Reach {consumers_charts[3]}%</span>
                                        </div>
                                        <div class="col-6">
                                            <span class="number">Average Conversion {consumers_charts[4]}%</span>
                                        </div>
                                    </div>
                                </div>
                '''
        volume_per = f'''
            <p class="chart-title">VOLUME PERFORMANCE</p>
                    <br>
                    <p class="desc">(Can/Bottle)</p>
                    <p class="desc">Actual Volume</p>
                    <span class="number-one max-size">{volume_performance[0]}</span>
                    <br>
                    <p class="desc">Target Volume</p>
            <span class="number-two">{volume_performance[1]}</span>
        '''
        print(pie)
        print(gift_charts[0])
        print(consumers_charts)
        return JsonResponse({'created': 'ok', 'list_outlet':list_outlet, 'Consumers_charts':Consumers,'volume_performance':volume_per, 'pie_chart': pie, 'gift':gift_charts[0], 'array_gift': append_array(gift_charts[1]) ,'top10_sale':top_10[0], 'top10_table':top_10[1], 'top10_name':top_10[2], 'Average_brand_volume':Average_brand_volume, 'activation':activation[0],'total_activation':activation[1], 'actual_volume':volume_performance[0], 'target_volume':volume_performance[1]}) 
    return JsonResponse({'created': 'ko'}) 


def filter_outlet_type(request, campainID):
    if request.is_ajax and request.method == "POST":
        array_type = request.POST.get('array_type')

        type = array_type.split(',')
        list_outlet_chart = get_outlet_type(campainID, type)
        list_rp = getAll_report_outlet(campainID, list_outlet_chart[0])
        pie = pie_chart(campainID, list_rp[0])
        consumers_charts = total_consumers_reached(campainID, list_rp[1])
        gift_charts = gift(campainID, list_rp[2])
        volume_performance = VOLUME_PERFORMANCE(campainID, list_outlet_chart[0])
        Average_brand_volume = [volume_performance[2], volume_performance[3]]
        top_10 = top10_outlet(campainID, list_outlet_chart[0])
        activation = activation_progress(campainID, list_outlet_chart[0])
        print(type)
        print(consumers_charts)
        print(gift_charts)
        list_outlet = ''
      
        for outlet in list_outlet_chart[0]:
            list_outlet += f'''<tr>
                            <div class="sidebar-menu_sub">
                                <label>
                                        <input type="checkbox" class="sidebar-menu_checkbox" name="name_outlet"  value="{outlet.id}">
                                        <span class="checkmark"></span>
                                </label>
                                <p class="sidebar-menu_item">
                                        {outlet.outlet_Name}
                                </p>
                            </div>
                        </tr>
                        '''
        Consumers = f'''
                <div class="row-1">
                                    <div class="col-12">
                                        <div class="col-4">
                                            <p class="title">
                                                Total Consumers {consumers_charts[0]}
                                            </p>
                                        </div>
                                        <div class="col-4">
                                            <p class="title">
                                                Total Reached Consumers {consumers_charts[1]}
                                            </p>
                                        </div>
                                        <div class="col-4">
                                            <p class="title">
                                                Total Bought Consumers {consumers_charts[2]}
                                            </p>
                                        </div>
                                        
                                    </div>
                                </div>
                                <div class="row-2">
                                    <div class="col-12">
                                    
                                        <div class="col-6">
                                            <span class="number">Average Reach {consumers_charts[3]}%</span>
                                        </div>
                                        <div class="col-6">
                                            <span class="number">Average Conversion {consumers_charts[4]}%</span>
                                        </div>
                                    </div>
                                </div>
                '''
        volume_per = f'''
            <p class="chart-title">VOLUME PERFORMANCE</p>
                    <br>
                    <p class="desc">(Can/Bottle)</p>
                    <p class="desc">Actual Volume</p>
                    <span class="number-one max-size">{volume_performance[0]}</span>
                    <br>
                    <p class="desc">Target Volume</p>
            <span class="number-two">{volume_performance[1]}</span>
        '''
        return JsonResponse({'created': 'ok', 'list_outlet':list_outlet, 'Consumers_charts':Consumers, 'pie_chart': pie, 'volume_performance':volume_per,'gift':gift_charts[0], 'array_gift': append_array(gift_charts[1]), 'top10_sale':top_10[0], 'top10_table':top_10[1], 'top10_name':top_10[2], 'Average_brand_volume':Average_brand_volume, 'activation':activation[0],'total_activation':activation[1], 'actual_volume':volume_performance[0], 'target_volume':volume_performance[1]})

def filter_outlet(request, campainID):
    if request.is_ajax and request.method == "POST":
        array = request.POST.get('array')

        list_outlet = array.split(',')
        list_outlet_chart = get_outlet(campainID, list_outlet)
        list_rp = getAll_report_outlet(campainID, list_outlet_chart[0])
        pie = pie_chart(campainID, list_rp[0])
        consumers_charts = total_consumers_reached(campainID, list_rp[1])
        gift_charts = gift(campainID, list_rp[2])
        volume_performance = VOLUME_PERFORMANCE(campainID, list_outlet_chart[0])
        Average_brand_volume = [volume_performance[2], volume_performance[3]]
        top_10 = top10_outlet(campainID, list_outlet_chart[0])
        activation = activation_progress(campainID, list_outlet_chart[0])
        print(type)
        print(consumers_charts)
        print(gift_charts)
        list_outlet = ''
        print(list_outlet)
        Consumers = f'''
                <div class="row-1">
                                    <div class="col-12">
                                        <div class="col-4">
                                            <p class="title">
                                                Total Consumers {consumers_charts[0]}
                                            </p>
                                        </div>
                                        <div class="col-4">
                                            <p class="title">
                                                Total Reached Consumers {consumers_charts[1]}
                                            </p>
                                        </div>
                                        <div class="col-4">
                                            <p class="title">
                                                Total Bought Consumers {consumers_charts[2]}
                                            </p>
                                        </div>
                                        
                                    </div>
                                </div>
                                <div class="row-2">
                                    <div class="col-12">
                                    
                                        <div class="col-6">
                                            <span class="number">Average Reach {consumers_charts[3]}%</span>
                                        </div>
                                        <div class="col-6">
                                            <span class="number">Average Conversion {consumers_charts[4]}%</span>
                                        </div>
                                    </div>
                                </div>
                '''
        volume_per = f'''
            <p class="chart-title">VOLUME PERFORMANCE</p>
                    <br>
                    <p class="desc">(Can/Bottle)</p>
                    <p class="desc">Actual Volume</p>
                    <span class="number-one max-size">{volume_performance[0]}</span>
                    <br>
                    <p class="desc">Target Volume</p>
            <span class="number-two">{volume_performance[1]}</span>
        '''
        return JsonResponse({'created': 'ok', 'list_outlet':list_outlet, 'Consumers_charts':Consumers, 'pie_chart': pie, 'volume_performance':volume_per,'gift':gift_charts[0], 'array_gift': append_array(gift_charts[1]), 'top10_sale':top_10[0], 'top10_table':top_10[1], 'top10_name':top_10[2], 'Average_brand_volume':Average_brand_volume, 'activation':activation[0],'total_activation':activation[1], 'actual_volume':volume_performance[0], 'target_volume':volume_performance[1]})



def list_gift_scheme(request, campainID):
    list_gift = get_gift_scheme(campainID)
    list_gift_1 = ""
    list_gift_2 = ""
    for gift in list_gift[1]:
        list_gift_1 += f'''
                <div >
                    <p class="title">{gift}</p>
                </div>
        '''
   
    return JsonResponse({'list_scheme1':list_gift[0], 'list_scheme1_name':list_gift[1], 'list_gift_1':list_gift_1,'list_scheme2':list_gift[2], 'list_scheme2_name':list_gift[3]})

###############################
def view_export(request, campainID):
    return render(request,'dashboard/export-report.html', {"cam_id":campainID}) 
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
    
    
    if campainID == 1:
        colums = ['Province', 'Outlet ID', 'Type', 'Area', 'Address', 'Outlet name', 'HNK Volume Sales', 'HVN_volume', 'Competitor_volume','Brand Tables', 'HVB Table Share', 'other table','Other Beer Table', 'Total Tables','Total Consumers', 'Consumers Approached', 'Consumer Bought','Ly 30cl','Ly 33cl 3D','Ly Casablanca', 'Ví', 'Nón Tiger Crystal', 'Voucher Bia', 'Ly 30cl','Ly 33cl 3D','Ly Casablanca', 'Ví', 'Nón Tiger Crystal', 'Voucher Bia']
    
    elif campainID == 2:
        colums = ['Province', 'Outlet ID', 'Type', 'Area', 'Address', 'Outlet name', 'HNK Volume Sales', 'HVN_volume', 'Competitor_volume','Brand Tables', 'HVB Table Share', 'other table','Other Beer Table', 'Total Tables','Total Consumers', 'Consumers Approached', 'Consumer Bought','Ly 30cl','Voucher beer', 'Festive Box', 'Túi du lịch Tiger', 'Loa Tiger', 'Ví Tiger ', 'Iphone 13','Ly 30cl','Voucher beer', 'Festive Box', 'Túi du lịch Tiger', 'Loa Tiger', 'Ví Tiger ', 'Iphone 13']

    elif campainID == 4:
        colums = ['Province', 'Outlet ID', 'Type', 'Area', 'Address', 'Outlet name', 'HNK Volume Sales', 'HVN_volume', 'Competitor_volume','Brand Tables', 'HVB Table Share', 'other table','Other Beer Table', 'Total Tables','Total Consumers', 'Consumers Approached', 'Consumer Bought','Pin sạc','Ba lô', 'Bình Nước', 'Áo thun', 'Loa Bluetooth', 'Ly', 'Pin sạc','Ba lô', 'Bình Nước', 'Áo thun', 'Loa Bluetooth', 'Ly']

    elif campainID == 5:
        colums = ['Province', 'Outlet ID', 'Type', 'Area', 'Address', 'Outlet name', 'HNK Volume Sales', 'HVN_volume', 'Competitor_volume','Brand Tables', 'HVB Table Share', 'other table','Other Beer Table', 'Total Tables','Total Consumers', 'Consumers Approached', 'Consumer Bought','Heineken Alu', 'Ba lô', 'Combo Thời Trang', 'Combo Thể Thao', 'Heineken Alu', 'Ba lô', 'Combo Thời Trang', 'Combo Thể Thao']
    
    elif campainID == 6:
        colums = ['Province', 'Outlet ID', 'Type', 'Area', 'Address', 'Outlet name', 'HNK Volume Sales', 'HVN_volume', 'Competitor_volume','Brand Tables', 'HVB Table Share', 'other table','Other Beer Table', 'Total Tables','Total Consumers', 'Consumers Approached', 'Consumer Bought', 'Nón Strongbow', 'Túi Jute Bag', 'Túi Canvas ', 'Dù SB', 'Nón Strongbow', 'Túi Jute Bag', 'Túi Canvas ', 'Dù SB']

    elif campainID == 7:
        colums = ['Province', 'Outlet ID', 'Type', 'Area', 'Address', 'Outlet name', 'HNK Volume Sales', 'HVN_volume', 'Competitor_volume','Brand Tables', 'HVB Table Share', 'other table','Other Beer Table', 'Total Tables','Total Consumers', 'Consumers Approached', 'Consumer Bought','Túi du lịch', 'Đồng Hồ Treo Tường', 'Bình Nước 1,6L', 'Ly', 'Túi du lịch', 'Đồng Hồ Treo Tường', 'Bình Nước 1,6L', 'Ly']
    
    elif campainID == 8:
        colums = ['Province', 'Outlet ID', 'Type', 'Area', 'Address', 'Outlet name', 'HNK Volume Sales', 'HVN_volume', 'Competitor_volume','Brand Tables', 'HVB Table Share', 'other table','Other Beer Table', 'Total Tables','Total Consumers', 'Consumers Approached', 'Consumer Bought','Áo thun', 'Thùng 12 Lon', 'Nón', 'Ly', 'Áo thun', 'Thùng 12 Lon', 'Nón', 'Ly']
    
    else:
        colums = ['Province', 'Outlet ID', 'Type', 'Area', 'Address', 'Outlet name', 'HNK Volume Sales', 'HVN_volume', 'Competitor_volume','Brand Tables', 'HVB Table Share', 'other table','Other Beer Table', 'Total Tables','Total Consumers', 'Consumers Approached', 'Consumer Bought','Ba lô','Thùng 12 Lon', 'Nón', '02 Lon Larue', 'Ba lô','Thùng 12 Lon', 'Nón', '02 Lon Larue']
    
    for col_num in range(len(colums)):
        ws.write(row_num, col_num, colums[col_num], font_style)

    font_style = xlwt.XFStyle()
    
    from_date = request.POST.get('from-date')
    
    to_date = request.POST.get('to-date')
    
    print(from_date)
    #a = date.today()
    a = (date(2021,12,20))
    print(a) 
    for outlet in all_outlet:
        count_list_rp_sale = report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet = outlet).filter(created__lte=to_date, campain = Cp, outlet = outlet).count()
        list_rp_table = tableReport.objects.filter(created__gte=from_date, campain = Cp, outlet = outlet).filter(created__lte=to_date, campain = Cp, outlet = outlet)
        list_rp_sale = report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet = outlet).filter(created__lte=to_date, campain = Cp, outlet = outlet)
        list_rp_consumer = consumerApproachReport.objects.filter(created__gte=from_date, campain = Cp, outlet = outlet).filter(created__lte=to_date, campain = Cp, outlet = outlet)
        count_list_rp_consumer = consumerApproachReport.objects.filter(created__gte=from_date, campain = Cp, outlet = outlet).filter(created__lte=to_date, campain = Cp, outlet = outlet).count()
        list_gift_rp = giftReport.objects.filter(created__gte=from_date, campain = Cp, outlet = outlet).filter(created__lte=to_date, campain = Cp, outlet = outlet)
        count_list_gift_rp = giftReport.objects.filter(created__gte=from_date, campain = Cp, outlet = outlet).filter(created__lte=to_date, campain = Cp, outlet = outlet).count()
        total_sale = 0
        HVN_volume = 0
        Competitor_volume = 0
        total_HNK = 0
        total_HVB = 0
        total_other_beer = 0
        other_table = 0
        total_table = 0
        total_consumers_approach =0
        total_consumers = 0
        total_consumer_bought = 0
        total_gift1_receive = 0
        total_gift2_receive = 0
        total_gift3_receive = 0
        total_gift4_receive = 0
        total_gift5_receive = 0
        total_gift6_receive = 0
        total_gift7_receive = 0

        total_gift1_given = 0
        total_gift2_given = 0
        total_gift3_given = 0
        total_gift4_given = 0
        total_gift5_given = 0
        total_gift6_given = 0
        total_gift7_given = 0
        if count_list_rp_sale > 0 or count_list_rp_consumer> 0 or count_list_gift_rp>0:
            for rp_sale in list_rp_sale:
                total_sale = sum(total_sale, rp_sale.beer_brand)
                HVN_volume = sum(HVN_volume, rp_sale.beer_HVN)
                Competitor_volume = sum(Competitor_volume, rp_sale.beer_other)
            for rp_table in list_rp_table:
                total_HNK = sum(total_HNK, rp_table.brand_table)
                total_HVB = sum(total_HVB, rp_table.HVN_table)
                other_table = sum(other_table,  rp_table.other_table)
                total_other_beer = sum(total_other_beer, rp_table.other_beer_table)
                total_table = sum(total_table, rp_table.total_table)

            for consumer in list_rp_consumer:
                total_consumers_approach = sum(total_consumers_approach, consumer.consumers_approach)
                total_consumers = sum(total_consumers, consumer.Total_Consumers)
                total_consumer_bought = sum(total_consumer_bought, consumer.consumers_brough)

                
            for gift in list_gift_rp:
                total_gift1_receive = sum(total_gift1_receive, gift.gift1_received)
                total_gift2_receive = sum(total_gift2_receive, gift.gift2_received)
                total_gift3_receive = sum(total_gift3_receive, gift.gift3_received)
                total_gift4_receive = sum(total_gift4_receive, gift.gift4_received)
                total_gift5_receive = sum(total_gift5_receive, gift.gift5_received)
                total_gift6_receive = sum(total_gift6_receive, gift.gift6_received)
                total_gift7_receive = sum(total_gift7_receive, gift.gift7_received)

                total_gift1_given = sum(total_gift1_given, gift.gift1_given)
                total_gift2_given = sum(total_gift2_given, gift.gift2_given)
                total_gift3_given = sum(total_gift3_given, gift.gift3_given)
                total_gift4_given = sum(total_gift4_given, gift.gift4_given)
                total_gift5_given = sum(total_gift5_given, gift.gift5_given)
                total_gift6_given = sum(total_gift6_given, gift.gift6_given)
                total_gift7_given = sum(total_gift7_given, gift.gift7_given)

            if campainID == 1 or campainID == 4:
                list = [outlet.province, outlet.ouletID, outlet.type, outlet.area, outlet.outlet_address, outlet.outlet_Name, total_sale, HVN_volume, Competitor_volume, total_HNK, total_HVB, other_table, total_other_beer, total_table, total_consumers, total_consumers_approach, total_consumer_bought, total_gift1_receive, total_gift2_receive, total_gift3_receive, total_gift4_receive, total_gift5_receive, total_gift6_receive, total_gift1_given, total_gift2_given, total_gift3_given, total_gift4_given, total_gift5_given, total_gift6_given]
                
                row_num +=1
                for col_num in range(len(list)):
                    ws.write(row_num, col_num, str(list[col_num]), font_style)
            
            elif campainID == 2:
                list = [outlet.province, outlet.ouletID, outlet.type, outlet.area, outlet.outlet_address, outlet.outlet_Name, total_sale, HVN_volume, Competitor_volume, total_HNK, total_HVB, other_table, total_other_beer, total_table, total_consumers, total_consumers_approach, total_consumer_bought, total_gift1_receive, total_gift2_receive, total_gift3_receive, total_gift4_receive, total_gift5_receive, total_gift6_receive,total_gift7_receive, total_gift1_given, total_gift2_given, total_gift3_given, total_gift4_given, total_gift5_given, total_gift6_given, total_gift7_given]
                
                row_num +=1
                for col_num in range(len(list)):
                    ws.write(row_num, col_num, str(list[col_num]), font_style)
            
            else:
                list = [outlet.province, outlet.ouletID, outlet.type, outlet.area, outlet.outlet_address, outlet.outlet_Name, total_sale, HVN_volume, Competitor_volume, total_HNK, total_HVB, other_table, total_other_beer, total_table, total_consumers, total_consumers_approach, total_consumer_bought, total_gift1_receive, total_gift2_receive, total_gift3_receive, total_gift4_receive, total_gift1_given, total_gift2_given, total_gift3_given, total_gift4_given]
                row_num +=1
                
                for col_num in range(len(list)):
                    ws.write(row_num, col_num, str(list[col_num]), font_style)
                
    wb.save(response) 
    return response
        
    