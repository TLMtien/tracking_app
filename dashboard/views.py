from django.http import response
from django.shortcuts import redirect, render
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from dashboard.models import KPI
#from .forms import TimeReportForm, TimeDashBoard
from outlet.models import posmReport, outletInfo, tableReport, report_sale, consumerApproachReport, giftReport, Campain
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.views.generic import DetailView, ListView
from django.http import JsonResponse
from .forms import KPIForm, unlock_password
from urllib.parse import unquote
from users.models import SalePerson, NewUser
import json
from django.contrib import messages
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from .charts import pie_chart, total_consumers_reached, HNK_volume_sale, top10_outlet, volume_achieved_byProvince, gift, VOLUME_PERFORMANCE, activation_progress, get_outlet_province, getAll_report_outlet, get_outlet_type, get_outlet, get_gift_scheme, get_outlet_type_province, get_outletName_type_province
from .rawData import Table_share, sales_volume, consumers_reached_rawdata, gift_rawdata, get_gift_scheme_rawdata
from .exportExcel import export_chart
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
    
    return render(request, 'dashboard/outlet-approval.html', {'list_outlet_False':outlet, "cam_id":campainID})

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
        return render(request,"dashboard/create-kpi.html", {'form':form,"cam_id":campainID})


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
        return render(request, "dashboard/sp-info.html", {'sale_person':sale_person,"is_campain_owner":is_campain_owner, "cam_id":campainID})
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
    
    #VOLUME_PERFORMANCE
    #all_outlet = outletInfo.objects.filter(compain = Cp, created_by_HVN=True).filter(compain = Cp, created_by_HVN=True)
    all_outlet = []
    Cp = Campain.objects.get(id=campainID)
    sale_person = SalePerson.objects.filter(brand__pk=campainID)  # all_SP
    for SP in sale_person:
        outlet=SP.outlet
        rp_table = tableReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
        rp_sale =  report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
        gift_rp = giftReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
    
        if rp_table.exists() or rp_sale.exists() or gift_rp.exists():
            
            if not outlet in all_outlet and outlet.created_by_HVN:
                all_outlet.append(outlet)
    # volumperformance
    volume_per = VOLUME_PERFORMANCE(id, all_outlet, from_date, to_date)
    Average_brand_volume = [volume_per[2], volume_per[3]]
    # Top10
    top10 = top10_outlet(id, all_outlet)
    # volume_achieved_byProvince
    target_volume_achieved =volume_achieved_byProvince(id, all_outlet)
    #all_rp
    list_rp = getAll_report_outlet(campainID, all_outlet, from_date, to_date)
    #gift
    #list_gift_rp = giftReport.objects.filter(created__gte=from_date, campain = Cp).filter(created__lte=to_date, campain = Cp)
    gift_rp = gift(id, list_rp[2])
    #table_rp = tableReport.objects.filter(created__gte=from_date, campain = Cp).filter(created__lte=to_date, campain = Cp)
    pie=pie_chart(id, list_rp[0])
    #print(pie)
    #consumers_rp = consumerApproachReport.objects.filter(created__gte=from_date, campain = Cp).filter(created__lte=to_date, campain = Cp)
    report_customer = total_consumers_reached(id, list_rp[1])
    # HNK_volume_sale
    #all_report_sale =  report_sale.objects.filter(created__gte=from_date, campain = Cp).filter(created__lte=to_date, campain = Cp)
    Volume_sale = HNK_volume_sale(id, list_rp[3])
    # activation
    activation = activation_progress(id, all_outlet, from_date, to_date)

    #print(list_gift_rp)
    per = 0
    if volume_per[1] != 0:
        per= percent(volume_per[0], volume_per[1])
    percent_volume = per
    print(per)
    return render(request, 'dashboard/dashboard.html', {'text':pie, 'target_volume_achieved':target_volume_achieved, 
     'Volume_sale':Volume_sale, 'top10_sale':top10[0], 'top10_table':top10[1], 'top10_name':top10[2], 'gift_rp':gift_rp[0], 'gift_name' : gift_rp[1],'array_gift': append_array(gift_rp[1]),'total_consumers':report_customer[0] , 'ctm_reached':report_customer[1], 'total_bought_consumers':report_customer[2], 'per_reached':report_customer[3], 'average_conversion':report_customer[4], 'actual_volume' : volume_per[0], 'target_volume': volume_per[1], 'percent_volume':percent_volume,'Average_brand_volume': Average_brand_volume, 'activation':activation[0],'total_activation':activation[1],  'top10_sale_reverse':top10[3], 'top10_table_reverse': top10[4], 'top10_name_reverse':top10[5], 'list_province':volume_per[4], 'list_name_outlet':volume_per[5], 'list_type':volume_per[6], "cam_id":campainID, 'from_date':from_date,'to_date':to_date})


######
#filter_outlet_province
def filter_outlet_province(request, campainID):
    if request.is_ajax and request.method == "POST":
        array_province = request.POST.get('array_province') 
        from_date = request.POST.get('from_date') 
        to_date = request.POST.get('to_date') 
        print(from_date)
        print(to_date)
        if from_date == '' or from_date==None:
            from_date = (date(2021,12,20))
        if to_date == '' or to_date==None:
            to_date = (date.today())
        # fromdate-todate
        province = array_province.split(',')

        list_outlet_chart = get_outlet_province(campainID, province, from_date, to_date)
        list_rp = getAll_report_outlet(campainID, list_outlet_chart[0], from_date, to_date)
        
            
        pie = pie_chart(campainID, list_rp[0])
        consumers_charts = total_consumers_reached(campainID, list_rp[1])
        gift_charts = gift(campainID, list_rp[2])
        volume_performance = VOLUME_PERFORMANCE(campainID, list_outlet_chart[0], from_date, to_date)
        Average_brand_volume = [volume_performance[2], volume_performance[3]]
        top_10 = top10_outlet(campainID, list_outlet_chart[0])
        activation = activation_progress(campainID, list_outlet_chart[0], from_date, to_date)
        #print(province)
        #print(consumers_charts)
        #print(gift_charts)
        list_outlet = ''
        list_type = ''
        if len(list_outlet_chart[0]) == 0:
            #all_outlet = outletInfo.objects.filter(compain = Cp, created_by_HVN=True)
            #all__outlet
            all_outlet = []
            Cp = Campain.objects.get(id=campainID)
            sale_person = SalePerson.objects.filter(brand__pk=campainID)  # all_SP
            for SP in sale_person:
                outlet=SP.outlet
                rp_table = tableReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
                rp_sale =  report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
                gift_rp = giftReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
            
                if rp_table.exists() or rp_sale.exists() or gift_rp.exists():
                    
                    if not outlet in all_outlet and outlet.created_by_HVN:
                        all_outlet.append(outlet)
            #end all_outlet
            volume_perf = VOLUME_PERFORMANCE(campainID, all_outlet, from_date, to_date)
            volume_performance[5] = volume_perf[5]
            volume_performance[6] = volume_perf[6]

            list_rp = getAll_report_outlet(campainID, all_outlet, from_date, to_date)
        
            pie = pie_chart(campainID, list_rp[0])
            consumers_charts = total_consumers_reached(campainID, list_rp[1])
            gift_charts = gift(campainID, list_rp[2])
            
            Average_brand_volume = [volume_perf[2], volume_perf[3]]
            top_10 = top10_outlet(campainID, all_outlet)
            activation = activation_progress(campainID, all_outlet, from_date, to_date)
        for outlet in volume_performance[5]:
            list_outlet += f'''
                            <div class="sidebar-menu_sub">
                                    <label>
                                        <input type="checkbox" class="sidebar-menu_checkbox" name="name_outlet" value="{outlet}">
                                        <span class="checkmark"></span>
                                    </label>
                                    <p class="sidebar-menu_item">
                                        {outlet}
                                    </p>
                            </div>
                        '''
        for type in volume_performance[6]:
            print(type)
            list_type += f'''<tr>
                                <div class="sidebar-menu_sub">
                                    <label>
                                        <input type="checkbox"  class="sidebar-menu_checkbox" name="type_outlet" value = "{type}"> 
                                        <span class="checkmark"></span>
                                    </label>
                                    <p class="sidebar-menu_item">
                                       {type}
                                    </p>
                                </div>
                            </tr>
                        '''
        Consumers = f'''
                <div class="row-1">
                                    <div class="col-12">
                                        <div class="col-4">
                                            <p class="title">
                                                Total Consumers <br> {consumers_charts[0]}
                                            </p>
                                        </div>
                                        <div class="col-4">
                                            <p class="title">
                                                Total Reached Consumers <br> {consumers_charts[1]}
                                            </p>
                                        </div>
                                        <div class="col-4">
                                            <p class="title">
                                                Total Bought Consumers <br> {consumers_charts[2]}
                                            </p>
                                        </div>
                                        
                                    </div>
                                </div>
                                <div class="row-2">
                                    <div class="col-12">
                                    
                                        <div class="col-6">
                                            <span class="number">Average Reach <br> {consumers_charts[3]}%</span>
                                        </div>
                                        <div class="col-6">
                                            <span class="number">Average Conversion <br> {consumers_charts[4]}%</span>
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
        return JsonResponse({'created': 'ok', 'list_outlet':list_outlet, 'list_type_outlet': list_type,'Consumers_charts':Consumers,'volume_performance':volume_per, 'pie_chart': pie, 'gift':gift_charts[0], 'array_gift': append_array(gift_charts[1]) ,'top10_sale':top_10[0], 'top10_table':top_10[1], 'top10_name':top_10[2], 'Average_brand_volume':Average_brand_volume, 'activation':activation[0],'total_activation':activation[1], 'actual_volume':volume_performance[0], 'target_volume':volume_performance[1]}) 
    return JsonResponse({'created': 'ko'}) 


def filter_outlet_type(request, campainID):
    if request.is_ajax and request.method == "POST":
        array_type = request.POST.get('array_type')
        from_date = request.POST.get('from_date') 
        to_date = request.POST.get('to_date') 
        print(from_date)
        print(to_date)
        if from_date == '' or from_date==None:
            from_date = (date(2021,12,20))
        if to_date == '' or to_date==None:
            to_date = (date.today())
        type = array_type.split(',')
        # endcall ajax
        list_outlet_chart = get_outlet_type(campainID, type, from_date, to_date)
        list_rp = getAll_report_outlet(campainID, list_outlet_chart[0], from_date, to_date)
        pie = pie_chart(campainID, list_rp[0])
        consumers_charts = total_consumers_reached(campainID, list_rp[1])
        gift_charts = gift(campainID, list_rp[2])
        volume_performance = VOLUME_PERFORMANCE(campainID, list_outlet_chart[0], from_date, to_date)
        Average_brand_volume = [volume_performance[2], volume_performance[3]]
        top_10 = top10_outlet(campainID, list_outlet_chart[0])
        activation = activation_progress(campainID, list_outlet_chart[0], from_date, to_date)
        print(type)
        print(consumers_charts)
        print(gift_charts)
        list_outlet = ''
      
        for outlet in list_outlet_chart[0]:
            list_outlet += f'''<tr>
                            <div class="sidebar-menu_sub">
                                <label>
                                        <input type="checkbox" class="sidebar-menu_checkbox" name="name_outlet"  value="{outlet.outlet_Name}">
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
                                                Total Consumers <br> {consumers_charts[0]}
                                            </p>
                                        </div>
                                        <div class="col-4">
                                            <p class="title">
                                                Total Reached Consumers <br> {consumers_charts[1]}
                                            </p>
                                        </div>
                                        <div class="col-4">
                                            <p class="title">
                                                Total Bought Consumers <br> {consumers_charts[2]}
                                            </p>
                                        </div>
                                        
                                    </div>
                                </div>
                                <div class="row-2">
                                    <div class="col-12">
                                    
                                        <div class="col-6">
                                            <span class="number">Average Reach <br> {consumers_charts[3]}%</span>
                                        </div>
                                        <div class="col-6">
                                            <span class="number">Average Conversion <br> {consumers_charts[4]}%</span>
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


def filter_outlet_type_province(request, campainID): 
    #get_outlet_type_province
    if request.is_ajax and request.method == "POST":
        total_array = request.POST.get('total_array')
        from_date = request.POST.get('from_date') 
        to_date = request.POST.get('to_date') 
        print(from_date)
        print(to_date)
        if from_date == '' or from_date==None:
            from_date = (date(2021,12,20))
        if to_date == '' or to_date==None:
            to_date = (date.today())
        # endcall ajax
        list_outlet_typeAndProvince = total_array.split(',')
        list_outlet_chart = get_outlet_type_province(campainID, list_outlet_typeAndProvince, from_date, to_date)
        print(list_outlet_chart)
        list_rp = getAll_report_outlet(campainID, list_outlet_chart[0], from_date, to_date)
        pie = pie_chart(campainID, list_rp[0])
        consumers_charts = total_consumers_reached(campainID, list_rp[1])
        gift_charts = gift(campainID, list_rp[2])
        volume_performance = VOLUME_PERFORMANCE(campainID, list_outlet_chart[0], from_date, to_date)
        Average_brand_volume = [volume_performance[2], volume_performance[3]]
        top_10 = top10_outlet(campainID, list_outlet_chart[0])
        activation = activation_progress(campainID, list_outlet_chart[0], from_date, to_date)
        #print(type)
        print(consumers_charts)
        print(gift_charts)
        list_outlet = ''
        print(list_outlet)
        if len(list_outlet_chart[0]) == 0:
            #Cp = Campain.objects.get(id = campainID)
            #all_outlet = outletInfo.objects.filter(compain = Cp, created_by_HVN=True)
            # filter outlet
            all_outlet = []
            Cp = Campain.objects.get(id=campainID)
            sale_person = SalePerson.objects.filter(brand__pk=campainID)  # all_SP
            for SP in sale_person:
                outlet=SP.outlet
                rp_table = tableReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
                rp_sale =  report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
                gift_rp = giftReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
            
                if rp_table.exists() or rp_sale.exists() or gift_rp.exists():
                    
                    if not outlet in all_outlet and outlet.created_by_HVN:
                        all_outlet.append(outlet)
            # end filter outlet
            volume_perf = VOLUME_PERFORMANCE(campainID, all_outlet, from_date, to_date)
            volume_performance[5] = volume_perf[5]
            volume_performance[6] = volume_perf[6]

            list_rp = getAll_report_outlet(campainID, all_outlet, from_date, to_date)
        
            pie = pie_chart(campainID, list_rp[0])
            consumers_charts = total_consumers_reached(campainID, list_rp[1])
            gift_charts = gift(campainID, list_rp[2])
            
            Average_brand_volume = [volume_perf[2], volume_perf[3]]
            top_10 = top10_outlet(campainID, all_outlet)
            activation = activation_progress(campainID, all_outlet, from_date, to_date)
            

        for outlet in volume_performance[5]:
            list_outlet += f'''
                            <div class="sidebar-menu_sub">
                                    <label>
                                        <input type="checkbox" class="sidebar-menu_checkbox" name="name_outlet" value="{outlet}">
                                        <span class="checkmark"></span>
                                    </label>
                                    <p class="sidebar-menu_item">
                                        {outlet}
                                    </p>
                            </div>
                        '''
        list_type = ''
        for type in volume_performance[6]:
            print(type)
            list_type += f'''<tr>
                                <div class="sidebar-menu_sub">
                                    <label>
                                        <input type="checkbox"  class="sidebar-menu_checkbox" name="type_outlet" value = "{type}"> 
                                        <span class="checkmark"></span>
                                    </label>
                                    <p class="sidebar-menu_item">
                                       {type}
                                    </p>
                                </div>
                            </tr>
                        '''
        Consumers = f'''
                <div class="row-1">
                                    <div class="col-12">
                                        <div class="col-4">
                                            <p class="title">
                                                Total Consumers <br> {consumers_charts[0]}
                                            </p>
                                        </div>
                                        <div class="col-4">
                                            <p class="title">
                                                Total Reached Consumers <br> {consumers_charts[1]}
                                            </p>
                                        </div>
                                        <div class="col-4">
                                            <p class="title">
                                                Total Bought Consumers <br> {consumers_charts[2]}
                                            </p>
                                        </div>
                                        
                                    </div>
                                </div>
                                <div class="row-2">
                                    <div class="col-12">
                                    
                                        <div class="col-6">
                                            <span class="number">Average Reach <br> {consumers_charts[3]}%</span>
                                        </div>
                                        <div class="col-6">
                                            <span class="number">Average Conversion <br> {consumers_charts[4]}%</span>
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
        return JsonResponse({'created': 'ok', 'list_outlet':list_outlet, 'Consumers_charts':Consumers, 'pie_chart': pie, 'volume_performance':volume_per,'gift':gift_charts[0], 'array_gift': append_array(gift_charts[1]), 'top10_sale':top_10[0], 'top10_table':top_10[1], 'top10_name':top_10[2], 'Average_brand_volume':Average_brand_volume, 'activation':activation[0],'total_activation':activation[1], 'actual_volume':volume_performance[0], 'target_volume':volume_performance[1], 'list_type_outlet': list_type})

def filter_outletName_Province_type(request, campainID):
    # get_outletName_type_province
    if request.is_ajax and request.method == "POST":
        total_array = request.POST.get('total_array')
        from_date = request.POST.get('from_date') 
        to_date = request.POST.get('to_date') 
        print(from_date)
        print(to_date)
        if from_date == '' or from_date==None:
            from_date = (date(2021,12,20))
        if to_date == '' or to_date==None:
            to_date = (date.today())
        list_outlet_typeAndProvince = total_array.split(',')
        #endcall ajax
        list_outlet_chart = get_outletName_type_province(campainID, list_outlet_typeAndProvince)
        print(list_outlet_chart)
        list_rp = getAll_report_outlet(campainID, list_outlet_chart[0], from_date, to_date)
        pie = pie_chart(campainID, list_rp[0])
        consumers_charts = total_consumers_reached(campainID, list_rp[1])
        gift_charts = gift(campainID, list_rp[2])
        volume_performance = VOLUME_PERFORMANCE(campainID, list_outlet_chart[0], from_date, to_date)
        Average_brand_volume = [volume_performance[2], volume_performance[3]]
        top_10 = top10_outlet(campainID, list_outlet_chart[0])
        activation = activation_progress(campainID, list_outlet_chart[0], from_date, to_date)
        print(type)
        print(consumers_charts)
        print(gift_charts)
        list_outlet = ''
        print(list_outlet)
        if len(list_outlet_chart[0]) == 0:
            Cp = Campain.objects.get(id = campainID)
            #all_outlet = outletInfo.objects.filter(compain = Cp, created_by_HVN=True)
            # filter outlet
            all_outlet = []
            #Cp = Campain.objects.get(id=campainID)
            sale_person = SalePerson.objects.filter(brand__pk=campainID)  # all_SP
            for SP in sale_person:
                outlet=SP.outlet
                rp_table = tableReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
                rp_sale =  report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
                gift_rp = giftReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
            
                if rp_table.exists() or rp_sale.exists() or gift_rp.exists():
                    
                    if not outlet in all_outlet and outlet.created_by_HVN:
                        all_outlet.append(outlet)
                #end filter outlet
            volume_perf = VOLUME_PERFORMANCE(campainID, all_outlet, from_date, to_date)
            volume_performance[5] = volume_perf[5]
            volume_performance[6] = volume_perf[6]

            list_rp = getAll_report_outlet(campainID, all_outlet, from_date, to_date)
        
            pie = pie_chart(campainID, list_rp[0])
            consumers_charts = total_consumers_reached(campainID, list_rp[1])
            gift_charts = gift(campainID, list_rp[2])
            
            Average_brand_volume = [volume_perf[2], volume_perf[3]]
            top_10 = top10_outlet(campainID, all_outlet)
            activation = activation_progress(campainID, all_outlet, from_date, to_date)
        for outlet in volume_performance[5]:
            list_outlet += f'''
                            <div class="sidebar-menu_sub">
                                    <label>
                                        <input type="checkbox" class="sidebar-menu_checkbox" name="name_outlet" value="{outlet}">
                                        <span class="checkmark"></span>
                                    </label>
                                    <p class="sidebar-menu_item">
                                        {outlet}
                                    </p>
                            </div>
                        '''
        Consumers = f'''
                <div class="row-1">
                                    <div class="col-12">
                                        <div class="col-4">
                                            <p class="title">
                                                Total Consumers <br> {consumers_charts[0]}
                                            </p>
                                        </div>
                                        <div class="col-4">
                                            <p class="title">
                                                Total Reached Consumers <br> {consumers_charts[1]}
                                            </p>
                                        </div>
                                        <div class="col-4">
                                            <p class="title">
                                                Total Bought Consumers <br> {consumers_charts[2]}
                                            </p>
                                        </div>
                                        
                                    </div>
                                </div>
                                <div class="row-2">
                                    <div class="col-12">
                                    
                                        <div class="col-6">
                                            <span class="number">Average Reach <br> {consumers_charts[3]}%</span>
                                        </div>
                                        <div class="col-6">
                                            <span class="number">Average Conversion <br> {consumers_charts[4]}%</span>
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
        from_date = request.POST.get('from_date') 
        to_date = request.POST.get('to_date') 
        print(from_date)
        print(to_date)
        if from_date == '' or from_date==None:
            from_date = (date(2021,12,20))
        if to_date == '' or to_date==None:
            to_date = (date.today())
        list_outlet = array.split(',')
        #endcall ajax
        list_outlet_chart = get_outlet(campainID, list_outlet)
        list_rp = getAll_report_outlet(campainID, list_outlet_chart[0], from_date, to_date)
        pie = pie_chart(campainID, list_rp[0])
        consumers_charts = total_consumers_reached(campainID, list_rp[1])
        gift_charts = gift(campainID, list_rp[2])
        volume_performance = VOLUME_PERFORMANCE(campainID, list_outlet_chart[0], from_date, to_date)
        Average_brand_volume = [volume_performance[2], volume_performance[3]]
        top_10 = top10_outlet(campainID, list_outlet_chart[0])
        activation = activation_progress(campainID, list_outlet_chart[0], from_date, to_date)
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
                                                Total Consumers <br> {consumers_charts[0]}
                                            </p>
                                        </div>
                                        <div class="col-4">
                                            <p class="title">
                                                Total Reached Consumers <br> {consumers_charts[1]}
                                            </p>
                                        </div>
                                        <div class="col-4">
                                            <p class="title">
                                                Total Bought Consumers <br> {consumers_charts[2]}
                                            </p>
                                        </div>
                                        
                                    </div>
                                </div>
                                <div class="row-2">
                                    <div class="col-12">
                                    
                                        <div class="col-6">
                                            <span class="number">Average Reach <br> {consumers_charts[3]}%</span>
                                        </div>
                                        <div class="col-6">
                                            <span class="number">Average Conversion  <br> {consumers_charts[4]}%</span>
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
   
    return JsonResponse({'list_scheme1':list_gift[0], 'list_scheme1_name':list_gift[1], 'list_gift_1':list_gift_1,'list_scheme2':list_gift[2], 'list_scheme2_name':list_gift[3], 'list_scheme3':list_gift[4], 'list_scheme3_name':list_gift[5], 'list_scheme4':list_gift[6], 'list_scheme4_name':list_gift[7], 'list_scheme5':list_gift[8], 'list_scheme5_name':list_gift[9]})

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
    from_date = request.POST.get('from-date')
    to_date = request.POST.get('to-date')
    Full_Report = request.POST.get('Full Report')
    Dashboard = request.POST.get('Dashboard')
    Raw_Data = request.POST.get('Raw Data')
    Photo_Report = request.POST.get('Photo Report')
    all_outlet = []
    Cp = Campain.objects.get(id=campainID)
    sale_person = SalePerson.objects.filter(brand__pk=campainID)  # all_SP
    for SP in sale_person:
        outlet=SP.outlet
        rp_table = tableReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
        rp_sale =  report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
        list_gift_rp = giftReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
    
        if rp_table.exists() or rp_sale.exists() or list_gift_rp.exists():
            
            if not outlet in all_outlet: #and outlet.created_by_HVN:
                all_outlet.append(outlet)
    
    array_image = [] 
    array_outlet = [] 
    array_created = []
    picture = posmReport.objects.filter(created__gte=from_date, campain = Cp).filter(created__lte=to_date, campain = Cp)
    if picture.exists():
        for i in picture:
            array_image.append(str(i.image)) 
            array_outlet.append(i.outlet) 
            array_created.append(i.created) 
            print(i.image)
    print(array_image)
    #for user_id in data.get("array_id",[]):
    
    
    #all_outlet = outletInfo.objects.filter(compain=Cp, created_by_HVN = True)
    
    # a = export_chart(campainID, all_outlet, from_date, to_date)
    #return JsonResponse({'status': 'ok'})
    value = '1'
    if Full_Report == '1':
        value = '1'
    elif Dashboard == '2':
        value = '2'
    elif Raw_Data == '3':
        value = '3'
    elif Photo_Report == '4':
        value = '4'
    print(value)
    return export_chart(campainID, all_outlet, from_date, to_date, value, array_image, array_outlet, array_created)
    
        
def raw_data(request, campainID):
    
    date_filter = request.GET.get("date_filter") #
   
    province = ''
    if not date_filter:
        date_filter = date.today()
    else:
        date_filter = datetime.strptime(date_filter,"%Y-%m-%d")
    
    province_filter = request.GET.get("province_filter")
    if province_filter:
        province = unquote(province_filter)
        
    
        print(type(province))

    print(date_filter)

    Cp = Campain.objects.get(id=campainID)
    List_outlet = []
    List_raw_data = []
    list_name_gift = []
    list_name_gift1 = [] 
    list_name_gift2 = []
    list_name_gift3 = []
    list_name_gift4 = []
    
    
    sale_person = SalePerson.objects.filter(brand__pk=campainID)
    if province:
        for SP in sale_person:
            outlet=SP.outlet
            print(type(outlet.province))
            if outlet.province == province :
                rp_table = tableReport.objects.filter(campain = Cp, outlet=SP.outlet, created = date_filter)
                rp_sale =  report_sale.objects.filter(campain=Cp, outlet=SP.outlet, created = date_filter)
                consumers_rp = consumerApproachReport.objects.filter(campain=Cp, outlet=SP.outlet, created = date_filter)
                list_gift_rp = giftReport.objects.filter(campain = Cp, outlet = SP.outlet, created=date_filter)
                print(outlet.province)
                if rp_table.exists() or rp_sale.exists() or list_gift_rp.exists():
                    if not SP.outlet in List_outlet: 
                        List = []
                        list_name_gift = []
                        list_name_gift1 = [] 
                        list_name_gift2 = []
                        list_name_gift3 = []
                        list_name_gift4 = []
                        List_outlet.append(SP.outlet)
                        table_share = Table_share(campainID, rp_table)
                        SaleVolume = sales_volume(campainID, rp_sale)
                        consumer = consumers_reached_rawdata(campainID, consumers_rp)
                        if campainID == 1 or campainID == 3 or campainID == 5 or campainID == 7 or campainID == 8 or campainID == 9:
                            gift = gift_rawdata(campainID, list_gift_rp)
                            List = [SP.outlet.province, SP.outlet.ouletID, SP.outlet.type, SP.outlet.area, SP.outlet.outlet_address, SP.outlet.outlet_Name, SaleVolume[0], SaleVolume[1], SaleVolume[2], table_share[0], table_share[1], table_share[2], table_share[3], table_share[4], table_share[5], consumer[0], consumer[1], consumer[2], consumer[3], consumer[4], gift[0]]
                            
                        if campainID == 2 or campainID == 4 or campainID == 6:
                            gift = get_gift_scheme_rawdata(campainID, SP.outlet, list_gift_rp)
                            List = [SP.outlet.province, SP.outlet.ouletID, SP.outlet.type, SP.outlet.area, SP.outlet.outlet_address, SP.outlet.outlet_Name, SaleVolume[0], SaleVolume[1], SaleVolume[2], table_share[0], table_share[1], table_share[2], table_share[3], table_share[4], table_share[5], consumer[0], consumer[1], consumer[2], consumer[3], consumer[4], gift[0], gift[2]]
                            print(gift[0])
                            print(gift[2])
                            list_name_gift1.append(gift[3])
                        
                        if campainID == 6:
                            gift = get_gift_scheme_rawdata(campainID, SP.outlet, list_gift_rp)
                            List = [SP.outlet.province, SP.outlet.ouletID, SP.outlet.type, SP.outlet.area, SP.outlet.outlet_address, SP.outlet.outlet_Name, SaleVolume[0], SaleVolume[1], SaleVolume[2], table_share[0], table_share[1], table_share[2], table_share[3], table_share[4], table_share[5], consumer[0], consumer[1], consumer[2], consumer[3], consumer[4], gift[0], gift[2], gift[4], gift[6], gift[8]]
                            #print(gift[0])
                            #print(gift[2])
                            list_name_gift1.append(gift[3])
                            list_name_gift2.append(gift[5])
                            list_name_gift3.append(gift[7])
                            list_name_gift4.append(gift[9])

                    list_name_gift.append(gift[1])
                    List_raw_data.append(List)
                    #print(List)
                #print(list_name_gift)
        return render(request,'dashboard/raw-data.html', {"cam_id":campainID, 'List_raw_data':List_raw_data, 'list_name_gift':list_name_gift,'list_name_gift1':list_name_gift1, 'list_name_gift2':list_name_gift2, 'list_name_gift3':list_name_gift3, 'list_name_gift4':list_name_gift4, "date_filter":date_filter.strftime("%Y-%m-%d"),"province_filter":province_filter, 'province':province})
    else:
        sale_person = SalePerson.objects.filter(brand__pk=campainID)
        for SP in sale_person:
            outlet=SP.outlet
            print(type(outlet.province))
            rp_table = tableReport.objects.filter(campain = Cp, outlet=SP.outlet, created = date_filter)
            rp_sale =  report_sale.objects.filter(campain=Cp, outlet=SP.outlet, created = date_filter)
            consumers_rp = consumerApproachReport.objects.filter(campain=Cp, outlet=SP.outlet, created = date_filter)
            list_gift_rp = giftReport.objects.filter(campain = Cp, outlet = SP.outlet, created=date_filter)
        
            if rp_table.exists() or rp_sale.exists() or list_gift_rp.exists():
                if not SP.outlet in List_outlet: 
                    List = []
                    list_name_gift = []
                    list_name_gift1 = [] 
                    list_name_gift2 = []
                    list_name_gift3 = []
                    list_name_gift4 = []
                    List_outlet.append(SP.outlet)
                    table_share = Table_share(campainID, rp_table)
                    SaleVolume = sales_volume(campainID, rp_sale)
                    consumer = consumers_reached_rawdata(campainID, consumers_rp)
                    if campainID == 1 or campainID == 3 or campainID == 5 or campainID == 7 or campainID == 8 or campainID == 9:
                        gift = gift_rawdata(campainID, list_gift_rp)
                        List = [SP.outlet.province, SP.outlet.ouletID, SP.outlet.type, SP.outlet.area, SP.outlet.outlet_address, SP.outlet.outlet_Name, SaleVolume[0], SaleVolume[1], SaleVolume[2], table_share[0], table_share[1], table_share[2], table_share[3], table_share[4], table_share[5], consumer[0], consumer[1], consumer[2], consumer[3], consumer[4], gift[0]]
                        
                    if campainID == 2 or campainID == 4 or campainID == 6:
                        gift = get_gift_scheme_rawdata(campainID, SP.outlet, list_gift_rp)
                        List = [SP.outlet.province, SP.outlet.ouletID, SP.outlet.type, SP.outlet.area, SP.outlet.outlet_address, SP.outlet.outlet_Name, SaleVolume[0], SaleVolume[1], SaleVolume[2], table_share[0], table_share[1], table_share[2], table_share[3], table_share[4], table_share[5], consumer[0], consumer[1], consumer[2], consumer[3], consumer[4], gift[0], gift[2]]
                        print(gift[0])
                        print(gift[2])
                        list_name_gift1.append(gift[3])
                    
                    if campainID == 6:
                        gift = get_gift_scheme_rawdata(campainID, SP.outlet, list_gift_rp)
                        List = [SP.outlet.province, SP.outlet.ouletID, SP.outlet.type, SP.outlet.area, SP.outlet.outlet_address, SP.outlet.outlet_Name, SaleVolume[0], SaleVolume[1], SaleVolume[2], table_share[0], table_share[1], table_share[2], table_share[3], table_share[4], table_share[5], consumer[0], consumer[1], consumer[2], consumer[3], consumer[4], gift[0], gift[2], gift[4], gift[6], gift[8]]
                        #print(gift[0])
                        #print(gift[2])
                        list_name_gift1.append(gift[3])
                        list_name_gift2.append(gift[5])
                        list_name_gift3.append(gift[7])
                        list_name_gift4.append(gift[9])

                    list_name_gift.append(gift[1])
                    List_raw_data.append(List)
                    #print(List)
                #print(list_name_gift)
        return render(request,'dashboard/raw-data.html', {"cam_id":campainID, 'List_raw_data':List_raw_data, 'list_name_gift':list_name_gift,'list_name_gift1':list_name_gift1, 'list_name_gift2':list_name_gift2, 'list_name_gift3':list_name_gift3, 'list_name_gift4':list_name_gift4, "date_filter":date_filter.strftime("%Y-%m-%d"),"province_filter":province_filter})
        

def edit_rawdata(request, campainID):
    date_filter = request.GET.get("date_filter") #
   
    province = ''
    if not date_filter:
        date_filter = date.today()
    else:
        date_filter = datetime.strptime(date_filter,"%Y-%m-%d")
    
    province_filter = request.GET.get("province_filter")
    if province_filter:
        province = unquote(province_filter)
        
    
        print(type(province))

    print(date_filter)

    Cp = Campain.objects.get(id=campainID)
    List_outlet = []
    List_raw_data = []
    list_name_gift = []
    list_name_gift1 = [] 
    list_name_gift2 = []
    list_name_gift3 = []
    list_name_gift4 = []
    
    
    sale_person = SalePerson.objects.filter(brand__pk=campainID)
    if province:
        for SP in sale_person:
            outlet=SP.outlet
            print(type(outlet.province))
            if outlet.province == province :
                rp_table = tableReport.objects.filter(campain = Cp, outlet=SP.outlet, created = date_filter)
                rp_sale =  report_sale.objects.filter(campain=Cp, outlet=SP.outlet, created = date_filter)
                consumers_rp = consumerApproachReport.objects.filter(campain=Cp, outlet=SP.outlet, created = date_filter)
                list_gift_rp = giftReport.objects.filter(campain = Cp, outlet = SP.outlet, created=date_filter)
                print(outlet.province)
                if rp_table.exists() or rp_sale.exists() or list_gift_rp.exists():
                    if not SP.outlet in List_outlet: 
                        List = []
                        list_name_gift = []
                        list_name_gift1 = [] 
                        list_name_gift2 = []
                        list_name_gift3 = []
                        list_name_gift4 = []
                        rp_id_sale = 0
                        rp_id_table = 0
                        rp_id_consumer = 0
                        rp_id_gift = 0
                        ##################################
                        for rp in rp_sale:
                            rp_id_sale = rp.id
                        for rp in rp_table:
                            rp_id_table = rp.id
                        for rp in consumers_rp:
                            rp_id_consumer = rp.id
                        for rp in list_gift_rp:
                            rp_id_gift = rp.id
                        List_outlet.append(SP.outlet)
                        table_share = Table_share(campainID, rp_table)
                        SaleVolume = sales_volume(campainID, rp_sale)
                        
                        consumer = consumers_reached_rawdata(campainID, consumers_rp)
                        if campainID == 1 or campainID == 3 or campainID == 5 or campainID == 7 or campainID == 8 or campainID == 9:
                            gift = gift_rawdata(campainID, list_gift_rp)
                            List = [SP.outlet.province, SP.outlet.ouletID, SP.outlet.type, SP.outlet.area, SP.outlet.outlet_address, SP.outlet.outlet_Name, SaleVolume[0], SaleVolume[1], SaleVolume[2], table_share[0], table_share[1], table_share[2], table_share[3], table_share[4], table_share[5], consumer[0], consumer[1], consumer[2], consumer[3], consumer[4], rp_id_sale, rp_id_table, rp_id_consumer, rp_id_gift, gift[0]]
                            
                        if campainID == 2 or campainID == 4 or campainID == 6:
                            gift = get_gift_scheme_rawdata(campainID, SP.outlet, list_gift_rp)
                            List = [SP.outlet.province, SP.outlet.ouletID, SP.outlet.type, SP.outlet.area, SP.outlet.outlet_address, SP.outlet.outlet_Name, SaleVolume[0], SaleVolume[1], SaleVolume[2], table_share[0], table_share[1], table_share[2], table_share[3], table_share[4], table_share[5], consumer[0], consumer[1], consumer[2], consumer[3], consumer[4], rp_id_sale, rp_id_table, rp_id_consumer, rp_id_gift, gift[0], gift[2]]
                            print(gift[0])
                            print(gift[2])
                            list_name_gift1.append(gift[3])
                        
                        if campainID == 6:
                            gift = get_gift_scheme_rawdata(campainID, SP.outlet, list_gift_rp)
                            List = [SP.outlet.province, SP.outlet.ouletID, SP.outlet.type, SP.outlet.area, SP.outlet.outlet_address, SP.outlet.outlet_Name, SaleVolume[0], SaleVolume[1], SaleVolume[2], table_share[0], table_share[1], table_share[2], table_share[3], table_share[4], table_share[5], consumer[0], consumer[1], consumer[2], consumer[3], consumer[4],rp_id_sale, rp_id_table, rp_id_consumer, rp_id_gift, gift[0], gift[2], gift[4], gift[6], gift[8]]
                            #print(gift[0])
                            #print(gift[2])
                            list_name_gift1.append(gift[3])
                            list_name_gift2.append(gift[5])
                            list_name_gift3.append(gift[7])
                            list_name_gift4.append(gift[9])

                    list_name_gift.append(gift[1])
                    List_raw_data.append(List)
                    #print(List)
                #print(list_name_gift)
        return render(request,'dashboard/edit-raw-data.html', {"cam_id":campainID, 'List_raw_data':List_raw_data, 'list_name_gift':list_name_gift,'list_name_gift1':list_name_gift1, 'list_name_gift2':list_name_gift2, 'list_name_gift3':list_name_gift3, 'list_name_gift4':list_name_gift4, "date_filter":date_filter.strftime("%Y-%m-%d"),"province_filter":province_filter, 'province':province})
    else:
        sale_person = SalePerson.objects.filter(brand__pk=campainID)
        for SP in sale_person:
            outlet=SP.outlet
            print(type(outlet.province))
            rp_table = tableReport.objects.filter(campain = Cp, outlet=SP.outlet, created = date_filter)
            rp_sale =  report_sale.objects.filter(campain=Cp, outlet=SP.outlet, created = date_filter)
            consumers_rp = consumerApproachReport.objects.filter(campain=Cp, outlet=SP.outlet, created = date_filter)
            list_gift_rp = giftReport.objects.filter(campain = Cp, outlet = SP.outlet, created=date_filter)
        
            if rp_table.exists() or rp_sale.exists() or list_gift_rp.exists():
                if not SP.outlet in List_outlet: 
                    List = []
                    list_name_gift = []
                    list_name_gift1 = [] 
                    list_name_gift2 = []
                    list_name_gift3 = []
                    list_name_gift4 = []
                    list_id_report = []
                    rp_id_sale = 0
                    rp_id_table = 0
                    rp_id_consumer = 0
                    rp_id_gift = 0
                    ##################################
                    for rp in rp_sale:
                        rp_id_sale = rp.id
                    for rp in rp_table:
                        rp_id_table = rp.id
                    for rp in consumers_rp:
                        rp_id_consumer = rp.id
                    for rp in list_gift_rp:
                        rp_id_gift = rp.id
                    
                    list_id_report = [rp_id_sale, rp_id_table, rp_id_consumer, rp_id_gift]
                    print(list_id_report)    
                    ###################################
                    List_outlet.append(SP.outlet)
                    table_share = Table_share(campainID, rp_table)
                    SaleVolume = sales_volume(campainID, rp_sale)
                    consumer = consumers_reached_rawdata(campainID, consumers_rp)
                    if campainID == 1 or campainID == 3 or campainID == 5 or campainID == 7 or campainID == 8 or campainID == 9:
                        gift = gift_rawdata(campainID, list_gift_rp)
                        List = [SP.outlet.province, SP.outlet.ouletID, SP.outlet.type, SP.outlet.area, SP.outlet.outlet_address, SP.outlet.outlet_Name, SaleVolume[0], SaleVolume[1], SaleVolume[2], table_share[0], table_share[1], table_share[2], table_share[3], table_share[4], table_share[5], consumer[0], consumer[1], consumer[2], consumer[3], consumer[4], rp_id_sale, rp_id_table, rp_id_consumer, rp_id_gift, gift[0]]
                        
                    if campainID == 2 or campainID == 4 or campainID == 6:
                        gift = get_gift_scheme_rawdata(campainID, SP.outlet, list_gift_rp)
                        List = [SP.outlet.province, SP.outlet.ouletID, SP.outlet.type, SP.outlet.area, SP.outlet.outlet_address, SP.outlet.outlet_Name, SaleVolume[0], SaleVolume[1], SaleVolume[2], table_share[0], table_share[1], table_share[2], table_share[3], table_share[4], table_share[5], consumer[0], consumer[1], consumer[2], consumer[3], consumer[4], rp_id_sale, rp_id_table, rp_id_consumer, rp_id_gift, gift[0], gift[2]]
                        print(gift[0])
                        print(gift[2])
                        list_name_gift1.append(gift[3])
                    
                    if campainID == 6:
                        gift = get_gift_scheme_rawdata(campainID, SP.outlet, list_gift_rp)
                        List = [SP.outlet.province, SP.outlet.ouletID, SP.outlet.type, SP.outlet.area, SP.outlet.outlet_address, SP.outlet.outlet_Name, SaleVolume[0], SaleVolume[1], SaleVolume[2], table_share[0], table_share[1], table_share[2], table_share[3], table_share[4], table_share[5], consumer[0], consumer[1], consumer[2], consumer[3], consumer[4], rp_id_sale, rp_id_table, rp_id_consumer, rp_id_gift, gift[0], gift[2], gift[4], gift[6], gift[8]]
                        #print(gift[0])
                        #print(gift[2])
                        list_name_gift1.append(gift[3])
                        list_name_gift2.append(gift[5])
                        list_name_gift3.append(gift[7])
                        list_name_gift4.append(gift[9])

                    list_name_gift.append(gift[1])
                    List_raw_data.append(List)
                    #print(List)
                #print(list_name_gift) 
        return render(request,'dashboard/edit-raw-data.html', {"cam_id":campainID, 'List_raw_data':List_raw_data, 'list_name_gift':list_name_gift,'list_name_gift1':list_name_gift1, 'list_name_gift2':list_name_gift2, 'list_name_gift3':list_name_gift3, 'list_name_gift4':list_name_gift4, "date_filter":date_filter.strftime("%Y-%m-%d"),"province_filter":province_filter})
        
    #return render(request, 'dashboard/edit-raw-data.html', {"cam_id":campainID})

def unlock(request, campainID):
    if request.method == "POST":
        currentpassword = request.user.password
        form = unlock_password(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            check = check_password(password, currentpassword)
            print(password)
            print(currentpassword)
            print(check)
            if check:
                
                return redirect("edit_rawdata", campainID = campainID)
            messages.error(request, "password is incorrect")
            return render(request,"dashboard/unlock.html",{'form':form, 'cam_id':campainID})
           
    form = unlock_password()
    return render(request,"dashboard/unlock.html",{'form':form, 'cam_id':campainID})

# def edit_volume_sale(request, campainID):
#     if request.user.is_HVN:
#         print(json.loads(request.body.decode('UTF-8')))
#         data = json.loads(request.body.decode('UTF-8'))
#         data = data.get("array_report_sale",[])
#         sale_id = data[0][0]
#         date = data[1][0]
#         beer_brand = data[2][0]
#         beer_HVN = data[3][0]
#         beer_other = data[4][0]
#         print(sale_id, beer_brand)
#         Cp = Campain.objects.get(id=campainID)
#         try:
#             rp_sale = report_sale.objects.get(id=sale_id)
#             if beer_brand != '':
#                 rp_sale.beer_brand = beer_brand
#                 rp_sale.save()
#             if beer_HVN != '':
#                 rp_sale.beer_HVN = beer_HVN
#                 rp_sale.save()
#             if beer_other != '':
#                 rp_sale.beer_other = beer_other
#                 rp_sale.save()
#         except:
#             pass
#         return JsonResponse({'status': 'ok'})

# def edit_table_sale(request, campainID):
#     if request.user.is_HVN:
#         print(json.loads(request.body.decode('UTF-8')))
#         data = json.loads(request.body.decode('UTF-8'))
#         data = data.get("array_report_sale",[])
#         sale_id = data[0][0]
#         brand_table = data[1][0]
#         HVN_table = data[2][0]
#         other_beer_table = data[3][0]
#         other_table = data[4][0]
#         total_table = 0
#         percent_table_share = 0
#         print(brand_table, HVN_table, other_beer_table, other_table)
#         Cp = Campain.objects.get(id=campainID)
#         try:
#             rp_table = tableReport.objects.get(id=sale_id)
#             rp_table.brand_table = brand_table
#             rp_table.HVN_table = HVN_table
#             rp_table.other_beer_table = other_beer_table
#             rp_table.other_table = other_table
#             rp_table.save()
#             total_table = rp_table.total_table
#             if int(total_table) > 0:
#                 percent_table_share =  percent(brand_table, total_table)
#         except:
#             pass
        
      
#         print(total_table, percent_table_share)
#         return JsonResponse({'status': 'ok', 'total_table': total_table, 'percent_table_share':percent_table_share, 'id':sale_id})

# def edit_consumer_rp(request, campainID):
#     if request.user.is_HVN:
#         print(json.loads(request.body.decode('UTF-8')))
#         data = json.loads(request.body.decode('UTF-8'))
#         data = data.get("array_report_sale",[])
#         sale_id = data[0][0]
#         Total_Consumers = data[1][0]
#         consumers_approach = data[2][0]
#         consumers_brough = data[3][0]
#         consumers_reach = 0
#         conversion = 0
#         print(Total_Consumers, consumers_approach, consumers_brough)
#         try:
#             consumers_rp = consumerApproachReport.objects.get(id=sale_id)
#             consumers_rp.Total_Consumers = Total_Consumers
#             consumers_rp.consumers_approach = consumers_approach
#             consumers_rp.consumers_brough = consumers_brough
#             consumers_rp.save()
#             if int(Total_Consumers) > 0:
#                 consumers_reach = percent(consumers_approach, Total_Consumers)
#             if int(consumers_approach) > 0:
#                 conversion = percent(consumers_brough, consumers_approach)
#         except:
#             pass
        
#         print(consumers_reach, conversion)
#         return JsonResponse({'status': 'ok', 'consumers_reach': consumers_reach, 'conversion':conversion, 'id':sale_id})



def edit_volume_sale(request, campainID):
    if request.user.is_HVN:
        print(json.loads(request.body.decode('UTF-8')))
        data = json.loads(request.body.decode('UTF-8'))
        data = data.get("array_report_sale",[])
        sale_id = data[0]
        date = data[1]
        beer_brand = data[2]
        beer_HVN = data[3]
        beer_other = data[4]
        print(sale_id, beer_brand)
        print(len(sale_id))
        try:
            for i in range(len(sale_id)):
                rp_sale = report_sale.objects.get(id=sale_id[i])
                rp_sale.beer_brand = beer_brand[i]
                rp_sale.beer_HVN = beer_HVN[i]
                rp_sale.beer_other = beer_other[i]
                rp_sale.save()
        except:
            pass
        return JsonResponse({'status': 'ok'})

def edit_table_sale(request, campainID):
    if request.user.is_HVN:
        print(json.loads(request.body.decode('UTF-8')))
        data = json.loads(request.body.decode('UTF-8'))
        data = data.get("array_report_sale",[])
        sale_id = data[0]
        brand_table = data[1]
        HVN_table = data[2]
        other_beer_table = data[3]
        other_table = data[4]
        list_total_table = []
        list_percent_table_share = []
        print(brand_table, HVN_table, other_beer_table, other_table)
        Cp = Campain.objects.get(id=campainID)
        try:
            for i in range(len(sale_id)):
                total_table = 0
                percent_table_share = 0
                rp_table = tableReport.objects.get(id=sale_id[i])
                rp_table.brand_table = brand_table[i]
                rp_table.HVN_table = HVN_table[i]
                rp_table.other_beer_table = other_beer_table[i]
                rp_table.other_table = other_table[i]
                rp_table.save()
                total_table = rp_table.total_table
                if int(total_table) > 0:
                    percent_table_share =  percent(rp_table.brand_table, rp_table.total_table)
                list_total_table.append(total_table)
                list_percent_table_share.append(percent_table_share)
        except:
            pass
        
        print(total_table, percent_table_share)
        return JsonResponse({'status': 'ok', 'list_total_table': list_total_table, 'list_percent_table_share':list_percent_table_share, 'id':sale_id})

def edit_consumer_rp(request, campainID):
    if request.user.is_HVN:
        print(json.loads(request.body.decode('UTF-8')))
        data = json.loads(request.body.decode('UTF-8'))
        data = data.get("array_report_sale",[])
        sale_id = data[0]
        Total_Consumers = data[1]
        consumers_approach = data[2]
        consumers_brough = data[3]
        list_consumers_reach = []
        list_conversion = []
        print(Total_Consumers, consumers_approach, consumers_brough)
        try:
            for i in range(len(sale_id)):
                consumers_reach = 0
                conversion = 0
                consumers_rp = consumerApproachReport.objects.get(id=sale_id[i])
                consumers_rp.Total_Consumers = Total_Consumers[i]
                consumers_rp.consumers_approach = consumers_approach[i]
                consumers_rp.consumers_brough = consumers_brough[i]
                consumers_rp.save()
                if int(consumers_rp.Total_Consumers) > 0:
                    consumers_reach = percent(consumers_rp.consumers_approach, consumers_rp.Total_Consumers)
                if int(consumers_rp.consumers_approach) > 0:
                    conversion = percent(consumers_rp.consumers_brough, consumers_rp.consumers_approach)
                list_consumers_reach.append(consumers_reach)
                list_conversion.append(conversion)
        except:
            pass
        
        print(consumers_reach, conversion)
        return JsonResponse({'status': 'ok', 'list_consumers_reach':list_consumers_reach, 'list_conversion':list_conversion, 'id':sale_id})

def edit_gift_rp(request, campainID):
    if request.user.is_HVN:
        print(json.loads(request.body.decode('UTF-8')))
        data = json.loads(request.body.decode('UTF-8'))
        data = data.get("array_report_sale",[])
        sale_id = data[0]
        gift_receive_1 = data[1]
        gift_receive_2 = data[2]
        gift_receive_3 = data[3]
        gift_receive_4 = data[4]
        gift_receive_5 = data[5]
        gift_receive_6 = data[6]
        gift_receive_7 = data[7]

        gift_given_1 = data[8]
        gift_given_2 = data[9]
        gift_given_3 = data[10]
        gift_given_4 = data[11]
        gift_given_5 = data[12]
        gift_given_6 = data[13]
        gift_given_7 = data[14]
        list_gift_remain = []
        try:
            for i in range(len(sale_id)):
                gift1_remaining = 0
                gift2_remaining = 0
                gift3_remaining = 0
                gift4_remaining = 0
                gift5_remaining = 0
                gift6_remaining = 0
                gift7_remaining = 0
                try:
                    gift_rp = giftReport.objects.get(id=sale_id[i])
                    li = []
                    gift_rp.gift1_received = gift_receive_1[i]
                    gift_rp.gift2_received = gift_receive_2[i]
                    gift_rp.gift3_received = gift_receive_3[i]
                    gift_rp.gift4_received = gift_receive_4[i]
                    gift_rp.gift5_received = gift_receive_5[i]
                    gift_rp.gift6_received = gift_receive_6[i]
                    gift_rp.gift7_received = gift_receive_7[i]

                    gift_rp.gift1_given = gift_given_1[i]
                    gift_rp.gift2_given = gift_given_2[i]
                    gift_rp.gift3_given = gift_given_3[i]
                    gift_rp.gift4_given = gift_given_4[i]
                    gift_rp.gift5_given = gift_given_5[i]
                    gift_rp.gift6_given = gift_given_6[i]
                    gift_rp.gift7_given = gift_given_7[i]
                    gift_rp.save()
                    if int(gift_rp.gift1_remaining) > 0:
                        gift1_remaining = gift_rp.gift1_remaining
                    if int(gift_rp.gift2_remaining) > 0:
                        gift2_remaining = gift_rp.gift2_remaining
                    if int(gift_rp.gift3_remaining) > 0:
                        gift3_remaining = gift_rp.gift3_remaining
                    if int(gift_rp.gift4_remaining) > 0:
                        gift4_remaining = gift_rp.gift4_remaining
                    if int(gift_rp.gift5_remaining) > 0:
                        gift5_remaining = gift_rp.gift5_remaining
                    if int(gift_rp.gift6_remaining) > 0:
                        gift6_remaining = gift_rp.gift6_remaining
                    if int(gift_rp.gift7_remaining) > 0:
                        gift7_remaining = gift_rp.gift7_remaining
                    li = [gift1_remaining, gift2_remaining, gift3_remaining, gift4_remaining, gift5_remaining, gift6_remaining, gift7_remaining]
                    list_gift_remain.append(li)
                except:
                    gift1_remaining = 0
                    gift2_remaining = 0
                    gift3_remaining = 0
                    gift4_remaining = 0
                    gift5_remaining = 0
                    gift6_remaining = 0
                    gift7_remaining = 0
                    li = [gift1_remaining, gift2_remaining, gift3_remaining, gift4_remaining, gift5_remaining, gift6_remaining, gift7_remaining]
                    list_gift_remain.append(li)
        except:
            pass
        
        return JsonResponse({'status': 'ok', 'list_gift_remain':list_gift_remain, 'id':sale_id})


################################
#Export chart
# from openpyxl import Workbook
# from openpyxl.chart import (
#     PieChart,
#     Reference,
#     BarChart, Series, Reference,
# )
# def export_chart(campainID):
   
#     response = HttpResponse(
#         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
#     )
#     response['Content-Disposition'] = 'attachment;filename={}.xlsx'.format(str(datetime.now()))
#     wb = Workbook(write_only=True)
#     ws = wb.create_sheet()

#     ##activation

#     ## Volume
#     rows = [
#         ('Title', 'Average Brand Volume', 'Average Target Volume'),
#         ('Average Brand Volume', 150, 0),
#         ('Average Target Volume', 2500, 0),
#     ]

#     for row1 in rows:
#         ws.append(row1)


#     chart1 = BarChart()
#     chart1.type = "col"
#     chart1.style = 10
#     chart1.title = "AVERAGE PERFORMANCE PER ACT"

#     data1 = Reference(ws, min_col=2, min_row=1, max_row=3, max_col=3)
#     cats = Reference(ws, min_col=1, min_row=2, max_row=3)
#     chart1.add_data(data1, titles_from_data=True)
#     chart1.set_categories(cats)
#     #chart1.shape = 4
#     chart1.type = "col"
#     #chart1.style = 12
#     chart1.grouping = "stacked"
#     #chart1.overlap = 100
#     ws.add_chart(chart1, "J1")

#     ###############################
#     data = [
#         ['Pie', 'Sold'],
#         ['HVN', 50],
#         ['Brand', 30],
#         ['Other', 10],
#         ['Other beer', 40],
#     ]

#     for row in data:
#         ws.append(row)

#     pie = PieChart()
#     labels = Reference(ws, min_col=1, min_row=5, max_row=8)
#     data = Reference(ws, min_col=2, min_row=4, max_row=8)
#     pie.add_data(data, titles_from_data=True)
#     pie.set_categories(labels)
#     pie.title = "TABLE SHARE PERFORMANCE"

#     ws.add_chart(pie, "S1")

#     ###################################################
#     #ACtual
#     rows = [
#         ('Title', 'Actual Acts', 'Total Acts'),
#         ('Total Acts', 2500, 0),
#         ('Actual Acts', 150, 0),
#     ]

#     for row1 in rows:
#         ws.append(row1)
#     chart3 = BarChart()
#     chart3.type = "bar"
#     chart3.style = 10
#     chart3.title = "ACTIVATION PROGRESS"

#     data1 = Reference(ws, min_col=2, min_row=9, max_row=12, max_col=3)
#     cats = Reference(ws, min_col=1, min_row=10, max_row=12)
#     chart3.add_data(data1, titles_from_data=True)
#     chart3.set_categories(cats)
#     chart3.type = "bar"
#     #chart1.style = 12
#     chart3.grouping = "stacked"
#     #chart1.overlap = 100
#     ws.add_chart(chart3, "A1")
#     #gift
#     rows = [
#         ('Title', ),
#         ('Gift1', 50, 0),
#         ('Gift2', 25, 0),
#         ('Gift3', 35, 0),
#         ('Gift4', 45, 0),
#         ('Gift5', 55, 0),
#         ('Gift6', 65, 0),
#         ('Gift7', 65, 0),
#     ]

#     for row1 in rows:
#         ws.append(row1)

#     chart2 = BarChart()
#     chart2.type = "col"
#     chart2.style = 10
#     #chart2.title = "AVERAGE PERFORMANCE PER ACT"

#     data2 = Reference(ws, min_col=2, min_row=12, max_row=20, max_col=3)
#     cats = Reference(ws, min_col=1, min_row=13, max_row=20)
#     chart2.add_data(data2, titles_from_data=True)
#     chart2.set_categories(cats)
#     #chart1.shape = 4
#     chart2.type = "col"
#     chart2.style = 5
#     chart2.grouping = "stacked"
#     chart2.overlap = 100
#     ws.add_chart(chart2, "AB1")
#     ######################################################
#     #VOLUME PERFORMANCE
#     rows = [
#         ('Title', 'ActualVolume', 'Target Volume'),
#         ('Target Volume', 180, 0),
#         ('ActualVolume', 170, 0),
#     ]

#     for row1 in rows:
#         ws.append(row1)
#     chart4 = BarChart()
#     chart4.type = "bar"
#     chart4.style = 10
#     chart4.title = "VOLUME PERFORMANCE"

#     data1 = Reference(ws, min_col=2, min_row=20, max_row=23, max_col=3)
#     cats = Reference(ws, min_col=1, min_row=21, max_row=22)
#     chart4.add_data(data1, titles_from_data=True)
#     chart4.set_categories(cats)
#     chart4.type = "bar"
#     #chart1.style = 12
#     chart4.grouping = "stacked"
#     #chart1.overlap = 100
#     ws.add_chart(chart4, "A16")

#     #wb.save("chart5.xlsx")
#     wb.save(response) 
#     return response
