from os import name
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from outlet.models import tableReport, report_sale, consumerApproachReport, giftReport, outletInfo, posmReport, overallReport, Campain
from outlet.forms import tableReportForm, reportSaleForm, consumerApproachReportForm, gift_ReceiveReportForm, gift_givenReportForm
from django.views.generic import  DayArchiveView
import datetime
from users.models import SalePerson
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.




def sum(a, b):
    return str(int(a) + int(b))

def sum_table(a,b,c,d):
    return  str(int(a)+int(b)+int(c)+int(d))

def check_valid_tableReport(a,b,c,d,e):
    f = int(a)+int(b)+int(c)+int(d)
    if f <= int(e):
        return True
    return False

def check_valid_customerReport(a, b):
    if int(a)<=int(b):
        return True
    return False

#---------------------------------------------Report table----------------------------------------------------
login_required
def reportTable(request):

    if request.method == "POST":
        SP = SalePerson.objects.get(user=request.user)
        
        form = tableReportForm(request.POST,is_salePerson=request.user.is_salePerson)
        if form.is_valid():
            other_beer_table = form.cleaned_data.get('other_beer_table')
            brand_table = form.cleaned_data.get('brand_table')
            HVN_table = form.cleaned_data.get('HVN_table')
            other_table = form.cleaned_data.get('other_table')
            # total_table = form.cleaned_data.get('total_table')

            
            report_table = tableReport.objects.filter(created = datetime.date.today(), SP = request.user, outlet = SP.outlet).count()

            if report_table < 1:
                total_table = sum_table(other_beer_table, brand_table, HVN_table, other_table)
                p= tableReport.objects.create(SP=request.user, outlet=SP.outlet, campain=SP.brand, total_table=total_table,
                        other_beer_table=other_beer_table, other_table=other_table, brand_table=brand_table,  HVN_table=HVN_table)
                p.save()
                
                return render(request,"report/create_reportTable.html", {'other_beer_table':other_beer_table, 'brand_table':brand_table,
                                    'HVN_table':HVN_table,'total_table':total_table, 'other_table':other_table})

           
            report_table = tableReport.objects.get(created = datetime.date.today(), SP = request.user, outlet = SP.outlet)
            
            report_table.other_beer_table = other_beer_table
            report_table.other_table = other_table
            report_table.brand_table = brand_table
            report_table.HVN_table = HVN_table 
            total_table = sum_table(other_beer_table, brand_table, HVN_table, other_table)
            report_table.total_table = total_table
            report_table.save()
            
            return render(request,"report/sum-totaltable.html",{'sum_other_beer_table':report_table.other_beer_table, 'other_beer_table':other_beer_table,
                'sum_brand_table':report_table.brand_table, 'brand_table':brand_table, 'sum_HVN_table':report_table.HVN_table, 'HVN_table':HVN_table,
                'sum_total_table': report_table.total_table, 'total_table':total_table, 'sum_other_table':report_table.other_table, 'other_table':other_table})
        
    else:
        form = tableReportForm()
        return render(request,"report/table-number.html",{'form':form})

#--------------------------------------------------Sale report-----------------------------------------------------
login_required
def reportSale(request):
    if request.method == "POST":
        SP = SalePerson.objects.get(user=request.user)
        form = reportSaleForm(request.POST,is_salePerson=request.user.is_salePerson)
        if form.is_valid():
            beer_brand = form.cleaned_data.get('beer_brand')
            beer_HVN = form.cleaned_data.get('beer_HVN')
            beer_other = form.cleaned_data.get('beer_other')
            
            report = report_sale.objects.filter(created = datetime.date.today(), SP = request.user, outlet = SP.outlet).count()

            if report < 1:
                p = report_sale.objects.create(SP=request.user, outlet=SP.outlet, beer_brand=beer_brand, beer_HVN=beer_HVN, beer_other=beer_other, campain=SP.brand)
                p.save()
                return render(request,"report/create_salereport.html", {'beer_brand':beer_brand, 
                                        'beer_HVN':beer_HVN,'beer_other':beer_other})

           
            report = report_sale.objects.get(created = datetime.date.today(), SP = request.user, outlet = SP.outlet)
            
            report.beer_brand = sum(beer_brand, report.beer_brand)
            report.beer_HVN = sum(beer_HVN, report.beer_HVN)
            report.beer_other = sum(beer_other, report.beer_other)
            
            report.save()
            return render(request,"report/report-total-sale.html",{'sum_beer_brand':report.beer_brand, 'beer_brand':beer_brand,
                'sum_beer_HVN': report.beer_HVN, 'beer_HVN':beer_HVN, 'sum_beer_other':report.beer_other, 'beer_other': beer_other})
        
    else:
        form = reportSaleForm()
        SP = SalePerson.objects.get(user=request.user)
        beer_brand = '0'
        beer_other = '0'
        beer_HVN = '0'
        report = report_sale.objects.filter(created = datetime.date.today(), SP = request.user, outlet = SP.outlet).count()
        if report == 1:
            report = report_sale.objects.get(created = datetime.date.today(), SP = request.user, outlet = SP.outlet)
            beer_brand = report.beer_brand
            beer_other = report.beer_other
            beer_HVN = report.beer_HVN
        return render(request,"report/sales.html", {'form':form, 'beer_brand':beer_brand, 'beer_other':beer_other, 'beer_HVN':beer_HVN})

#------------------------------------------------------Report customer----------------------------------------
login_required
def report_customer(request):
    if request.method == "POST":
        form = consumerApproachReportForm(request.POST,is_salePerson=request.user.is_salePerson)
        if form.is_valid():
            SP = SalePerson.objects.get(user=request.user)
            consumers_approach = form.cleaned_data.get('consumers_approach')
            consumers_brough = form.cleaned_data.get('consumers_brough')
            Total_Consumers = form.cleaned_data.get('Total_Consumers')
            if (check_valid_customerReport(consumers_approach, Total_Consumers) == False) or (check_valid_customerReport(consumers_brough, consumers_approach) == False):
                return render(request,"report/alert-customer.html", {'consumers_approach':consumers_approach, 
                            'consumers_brough':consumers_brough,'Total_Consumers':Total_Consumers})

            
            report = consumerApproachReport.objects.filter(created = datetime.date.today(), SP = request.user, outlet = SP.outlet).count()

            if report < 1:
                p= consumerApproachReport.objects.create(SP=request.user, outlet=SP.outlet, campain=SP.brand,
                            consumers_approach=consumers_approach, consumers_brough=consumers_brough, Total_Consumers=Total_Consumers)
                p.save()
                return render(request,"report/create-report-customer.html", {'consumers_approach':consumers_approach, 
                            'consumers_brough':consumers_brough,'Total_Consumers':Total_Consumers})

           
            report = consumerApproachReport.objects.get(created = datetime.date.today(), SP = request.user, outlet = SP.outlet)
            
            report.consumers_approach = sum(consumers_approach, report.consumers_approach)
            report.consumers_brough = sum(consumers_brough, report.consumers_brough)
            report.Total_Consumers = sum(Total_Consumers, report.Total_Consumers)
            
            report.save()
            return render(request,"report/report-total-consumer.html",{'sum_consumers_approach':report.consumers_approach, 
                'consumers_approach':consumers_approach, 'sum_consumers_brough': report.consumers_brough, 'consumers_brough':consumers_brough, 
                'sum_Total_Consumers':report.Total_Consumers, 'Total_Consumers': Total_Consumers})
        
    else:
        form = consumerApproachReportForm()
        return render(request,"report/customer-access.html", {'form':form})

#---------------------------------------------Gift report-----------------------------------------------------
login_required
def gift_receiveReport(request):
    if request.method == "POST":
        form = gift_ReceiveReportForm(request.POST,is_salePerson=request.user.is_salePerson)
        if form.is_valid():
            SP = SalePerson.objects.get(user=request.user)
            gift1_received = form.cleaned_data.get('gift1_received')
            gift2_received = form.cleaned_data.get('gift2_received')
            gift3_received = form.cleaned_data.get('gift3_received')   
            gift4_received = form.cleaned_data.get('gift4_received')
            gift5_received = form.cleaned_data.get('gift5_received')
            gift6_received = form.cleaned_data.get('gift6_received')
            campain7 = Campain.objects.get(program='bivina')
            campain4 = Campain.objects.get(id=4)
            #form = gift_ReceiveReportForm()
            if SP.brand == campain7:
                report = giftReport.objects.filter(created = datetime.date.today(), SP = request.user, outlet = SP.outlet).count()
                if report < 1:
                    p, created = giftReport.objects.get_or_create(SP=request.user, outlet=SP.outlet, campain=SP.brand, gift1_received=gift1_received, 
                            gift2_received=gift2_received, gift3_received=gift3_received, gift4_received=gift4_received)
                    p.save()
                    return render(request, "report/create-list-gift-receive.html", {'gift1_received':gift1_received, 
                    'gift2_received':gift2_received,  'gift3_received':gift3_received ,'gift4_received':gift4_received})
                report = giftReport.objects.get(created = datetime.date.today(), SP = request.user, outlet = SP.outlet)
                report.gift1_received = sum(gift1_received, report.gift1_received)
                report.gift2_received = sum(gift2_received, report.gift2_received)
                report.gift3_received = sum(gift3_received, report.gift3_received)
                report.gift4_received = sum(gift4_received, report.gift4_received)
                report.save()
                return render(request, "report/create-list-gift-receive.html", {'gift1_received':gift1_received, 'gift2_received':gift2_received,
                        'gift3_received':gift3_received, 'gift4_received':gift4_received })
            else:
                report = giftReport.objects.filter(created = datetime.date.today(), SP = request.user, outlet = SP.outlet).count()
                if report < 1:
                    p = giftReport.objects.create(SP=request.user, outlet=SP.outlet, campain=SP.brand, gift1_received=gift1_received, 
                            gift2_received=gift2_received, gift3_received=gift3_received, gift4_received=gift4_received, 
                            gift5_received=gift5_received, gift6_received=gift6_received)
                    p.save()
                    return render(request, "list_gift/create-list-gift-receive.html", {'gift1_received':gift1_received, 
                    'gift2_received':gift2_received,  'gift3_received':gift3_received ,'gift4_received':gift4_received, 'gift5_received':gift5_received, 'gift6_received':gift6_received})
                report = giftReport.objects.get(created = datetime.date.today(), SP = request.user, outlet = SP.outlet)
                report.gift1_received = sum(gift1_received, report.gift1_received)
                report.gift2_received = sum(gift2_received, report.gift2_received)
                report.gift3_received = sum(gift3_received, report.gift3_received)
                report.gift4_received = sum(gift4_received, report.gift4_received)
                report.gift5_received = sum(gift5_received, report.gift5_received)
                report.gift6_received = sum(gift6_received, report.gift6_received)
                report.save()
                return render(request, "list_gift/create-list-gift-receive.html", {'gift1_received':gift1_received, 'gift2_received':gift2_received,
                        'gift3_received':gift3_received, 'gift4_received':gift4_received, 'gift5_received':gift5_received, 'gift6_received':gift6_received })
    else:
        SP = SalePerson.objects.get(user=request.user)
        campain7 = Campain.objects.get(program='bivina')
        campain4 = Campain.objects.get(id=4)
        form = gift_ReceiveReportForm()
        if SP.brand == campain7:
            return render(request,"report/listgift-received.html", {'form':form})
        return render(request,"list_gift/listgift-received.html", {'form':form})
        

login_required
def gift_givenReport(request):
    try:
        if request.method == "POST":
            form = gift_givenReportForm(request.POST,is_salePerson=request.user.is_salePerson)
            if form.is_valid():
                gift1_given = form.cleaned_data.get('gift1_given')
                gift2_given = form.cleaned_data.get('gift2_given')
                gift3_given = form.cleaned_data.get('gift3_given') 
                gift4_given = form.cleaned_data.get('gift4_given') 
                gift5_given = form.cleaned_data.get('gift5_given') 
                gift6_given = form.cleaned_data.get('gift6_given')
                campain7 = Campain.objects.get(program='bivina')
                campain4 = Campain.objects.get(id=4)
                form = gift_ReceiveReportForm()
                SP = SalePerson.objects.get(user=request.user)
                if SP.brand == campain7:
                    SP = SalePerson.objects.get(user=request.user)
                    report = giftReport.objects.get(created = datetime.date.today(), SP = request.user, outlet = SP.outlet)
                    report.gift1_given = sum(gift1_given, report.gift1_given)
                    report.gift2_given = sum(gift2_given, report.gift2_given)
                    report.gift3_given = sum(gift3_given, report.gift3_given)
                    report.gift4_given = sum(gift4_given, report.gift4_given)
                    report.save()
                    return redirect('quantity-gift')
                else:
                    SP = SalePerson.objects.get(user=request.user)
                    report = giftReport.objects.get(created = datetime.date.today(), SP = request.user, outlet = SP.outlet)
                    report.gift1_given = sum(gift1_given, report.gift1_given)
                    report.gift2_given = sum(gift2_given, report.gift2_given)
                    report.gift3_given = sum(gift3_given, report.gift3_given)
                    report.gift4_given = sum(gift4_given, report.gift4_given)
                    report.gift5_given = sum(gift4_given, report.gift5_given)
                    report.gift6_given = sum(gift4_given, report.gift6_given)
                    report.save()
                    return redirect('quantity-gift')
        else:
            form = gift_givenReportForm()
            campain7 = Campain.objects.get(program='bivina')
            campain4 = Campain.objects.get(id=4)
            form = gift_ReceiveReportForm()
            SP = SalePerson.objects.get(user=request.user)
            if SP.brand == campain7:
                return render(request,"report/listgift-sent.html", {'form':form})
            return render(request,"list_gift/listgift-sent.html", {'form':form})
    except:
        gift1_given = form.cleaned_data.get('gift1_given')
        gift2_given = form.cleaned_data.get('gift2_given')
        gift3_given = form.cleaned_data.get('gift3_given') 
        gift4_given = form.cleaned_data.get('gift4_given') 
        campain7 = Campain.objects.get(program='bivina')
        campain4 = Campain.objects.get(id=4)
        form = gift_ReceiveReportForm()
        SP = SalePerson.objects.get(user=request.user)
        if SP.brand == campain7:
            return render(request, 'report/alert-gift-given.html', {'gift1_given':gift1_given, 'gift2_given':gift2_given,
                'gift3_given':gift3_given,'gift4_given':gift4_given} )
        return HttpResponse('Bạn chưa nhập mục số quà nhận')

#---------------------------------------GIFT REMAINING--------------------

login_required
def gift_remaining(request):
    try:
        SP = SalePerson.objects.get(user=request.user)
        report = giftReport.objects.get(created = datetime.date.today(), SP = request.user, outlet = SP.outlet)
        campain7 = Campain.objects.get(program='bivina')
        campain4 = Campain.objects.get(id=4)
        if SP.brand == campain7:
            return render(request,'report/listgift-remain.html', {'gift1_remaining':report.gift1_remaining,
                'gift2_remaining': report.gift2_remaining, 'gift3_remaining': report.gift3_remaining, 'gift4_remaining': report.gift4_remaining,
                'gift1_received':report.gift1_received, 'gift2_received':report.gift2_received,
                        'gift3_received':report.gift3_received, 'gift4_received':report.gift4_received,
                'gift1_given':report.gift1_given, 'gift2_given':report.gift2_given, 
                'gift3_given':report.gift3_given, 'gift4_given':report.gift4_given})
        return render(request,'list_gift/listgift-remain.html', {'gift1_remaining':report.gift1_remaining,
                'gift2_remaining': report.gift2_remaining, 'gift3_remaining': report.gift3_remaining, 'gift4_remaining': report.gift4_remaining,'gift5_remaining': report.gift5_remaining,'gift6_remaining': report.gift6_remaining,
                'gift1_received':report.gift1_received, 'gift2_received':report.gift2_received,
                        'gift3_received':report.gift3_received, 'gift4_received':report.gift4_received,'gift5_received':report.gift5_received, 'gift6_received':report.gift6_received,
                'gift1_given':report.gift1_given, 'gift2_given':report.gift2_given, 
                'gift3_given':report.gift3_given, 'gift4_given':report.gift4_given, 'gift5_given':report.gift5_given, 'gift6_given':report.gift6_given})
    except:
        SP = SalePerson.objects.get(user=request.user)
        campain7 = Campain.objects.get(program='bivina')
        campain4 = Campain.objects.get(id=4)
        if SP.brand == campain7:
            return render(request,'report/listgift-remain.html', {'gift1_remaining':'0',
                'gift2_remaining': '0', 'gift3_remaining': '0', 'gift4_remaining': '0'})
        return render(request,'list_gift/listgift-remain.html', {'gift1_remaining':'0',
                'gift2_remaining': '0', 'gift3_remaining': '0', 'gift4_remaining': '0', 'gift5_remaining': '0', 'gift6_remaining': '0'})




#----------------------------------------------------Report POSM-----------------------------------------------------

@csrf_exempt
@login_required
def reportPosm(request):
    user = request.user
    SP = SalePerson.objects.get(user=user)
    
    # image = request.POST.get('image')
    image = request.FILES.get('image')
    print(image.name)
    print(image.content_type)
    # print(image.read())
    report = posmReport.objects.filter(created = datetime.date.today(), SP = request.user, outlet = SP.outlet).count()
    if report < 1:
        posmReport.objects.create(image= image, SP=user, outlet=SP.outlet, campain=SP.brand)
        return JsonResponse({'created': 'true'})
    
    report = posmReport.objects.get(created = datetime.date.today(), SP = request.user, outlet = SP.outlet)
    report.image.delete()
    report.image=image
    report.save()
    print(report.image.url)
    return JsonResponse({'created': 'true'})


#--------------------------------------------------------------Report EndCase--------------------------------------------------

@login_required
def reportEndcase(request):
    SP = SalePerson.objects.get(user=request.user) 
    image = request.FILES.get('image')
    report_posm = posmReport.objects.get(created = datetime.date.today(), SP = request.user, outlet = SP.outlet)
    report_table = tableReport.objects.get(created = datetime.date.today(), SP = request.user, outlet = SP.outlet)
    report_gift = giftReport.objects.get(created = datetime.date.today(), SP = request.user, outlet = SP.outlet)
    report_consumer = consumerApproachReport.objects.get(created = datetime.date.today(), SP = request.user, outlet = SP.outlet)

    report = overallReport.objects.filter(created = datetime.date.today(), user = request.user, outlet = SP.outlet, campain=SP.brand).count()
    print(report)
    if report < 1:
        report = overallReport.objects.create(user = request.user, confirm = image, outlet = SP.outlet, campain=SP.brand,
                table_Report=report_table, posm_Report=report_posm, gift_report=report_gift, consumer_report=report_consumer)
    
        return JsonResponse({'created': 'true'})
    
    report = overallReport.objects.get(created = datetime.date.today(), user = request.user, outlet = SP.outlet)
    report.confirm.delete()
    report.confirm = image
    report.report_posm = report_posm
    report.report_table = report_table
    report.report_gift = report_gift
    report.report_consumer = report_consumer
    report.save()

    return JsonResponse({'created': 'true'})