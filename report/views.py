from django.shortcuts import render, redirect
from outlet.models import tableReport, report_sale, consumerApproachReport, giftReport
from outlet.forms import tableReportForm, reportSaleForm, consumerApproachReportForm, gift_ReceiveReportForm, gift_givenReportForm
from django.views.generic import  DayArchiveView
import datetime
# Create your views here.



def sum(a, b):
    return str(int(a) + int(b))

def sum_table(a,b,c,d):
    return  str(int(a)+int(b)+int(c)+int(d))

def reportTable(request):

    if request.method == "POST":
        form = tableReportForm(request.POST,is_salePerson=request.user.is_salePerson)
        if form.is_valid():
            other_beer_table = form.cleaned_data.get('other_beer_table')
            brand_table = form.cleaned_data.get('brand_table')
            HVN_table = form.cleaned_data.get('HVN_table')
            other_table = form.cleaned_data.get('other_table')
            
            report_table = tableReport.objects.filter(created = datetime.date.today(), SP = request.user).count()

            if report_table < 1:
                p, created = tableReport.objects.get_or_create(SP=request.user, other_beer_table=other_beer_table, 
                     other_table=other_table, brand_table=brand_table,  HVN_table=HVN_table)
                p.save()

                return render(request,"report/create_reportTable.html", {'other_beer_table':other_beer_table, 'brand_table':brand_table,
                                    'HVN_table':HVN_table,'total_table':p.total_table, 'other_table':other_table})

           
            report_table = tableReport.objects.get(created = datetime.date.today(), SP = request.user)
            
            report_table.other_beer_table = sum(other_beer_table, report_table.other_beer_table)
            report_table.other_table = sum(other_table, report_table.other_table)
            report_table.brand_table = sum(brand_table, report_table.brand_table)
            report_table.HVN_table = sum(HVN_table, report_table.HVN_table)
            report_table.save()
            total_table = sum_table(other_beer_table, brand_table, HVN_table, other_table)
            return render(request,"report/sum-totaltable.html",{'sum_other_beer_table':report_table.other_beer_table, 'other_beer_table':other_beer_table,
                'sum_brand_table':report_table.brand_table, 'brand_table':brand_table, 'sum_HVN_table':report_table.HVN_table, 'HVN_table':HVN_table,
                'sum_total_table': report_table.total_table, 'total_table':total_table, 'sum_other_table':report_table.other_table, 'other_table':other_table})
        
    else:
        form = tableReportForm()
        return render(request,"report/table-number.html",{'form':form})


def reportSale(request):
    if request.method == "POST":
        form = reportSaleForm(request.POST,is_salePerson=request.user.is_salePerson)
        if form.is_valid():
            beer_brand = form.cleaned_data.get('beer_brand')
            beer_HVN = form.cleaned_data.get('beer_HVN')
            beer_other = form.cleaned_data.get('beer_other')
            
            
            report = report_sale.objects.filter(created = datetime.date.today(), SP = request.user).count()

            if report < 1:
                p, created = report_sale.objects.get_or_create(SP=request.user, beer_brand=beer_brand, beer_HVN=beer_HVN, beer_other=beer_other)
                p.save()
                return render(request,"report/create_salereport.html", {'beer_brand':beer_brand, 
                                        'beer_HVN':beer_HVN,'beer_other':beer_other})

           
            report = report_sale.objects.get(created = datetime.date.today(), SP = request.user)
            
            report.beer_brand = sum(beer_brand, report.beer_brand)
            report.beer_HVN = sum(beer_HVN, report.beer_HVN)
            report.beer_other = sum(beer_other, report.beer_other)
            
            report.save()
            return render(request,"report/report-total-sale.html",{'sum_beer_brand':report.beer_brand, 'beer_brand':beer_brand,
                'sum_beer_HVN': report.beer_HVN, 'beer_HVN':beer_HVN, 'sum_beer_other':report.beer_other, 'beer_other': beer_other})
        
    else:
        form = reportSaleForm()
        return render(request,"report/sales.html", {'form':form})


def report_customer(request):
    if request.method == "POST":
        form = consumerApproachReportForm(request.POST,is_salePerson=request.user.is_salePerson)
        if form.is_valid():
            consumers_approach = form.cleaned_data.get('consumers_approach')
            consumers_brough = form.cleaned_data.get('consumers_brough')
            Total_Consumers = form.cleaned_data.get('Total_Consumers')
            
            
            report = consumerApproachReport.objects.filter(created = datetime.date.today(), SP = request.user).count()

            if report < 1:
                p, created = consumerApproachReport.objects.get_or_create(SP=request.user, consumers_approach=consumers_approach, 
                                                    consumers_brough=consumers_brough, Total_Consumers=Total_Consumers)
                p.save()
                return render(request,"report/create-report-customer.html", {'consumers_approach':consumers_approach, 
                            'consumers_brough':consumers_brough,'Total_Consumers':Total_Consumers})

           
            report = consumerApproachReport.objects.get(created = datetime.date.today(), SP = request.user)
            
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


def gift_receiveReport(request):
    if request.method == "POST":
        form = gift_ReceiveReportForm(request.POST,is_salePerson=request.user.is_salePerson)
        if form.is_valid():
            gift1_received = form.cleaned_data.get('gift1_received')
            gift2_received = form.cleaned_data.get('gift2_received')
            gift3_received = form.cleaned_data.get('gift3_received')   

            report = giftReport.objects.filter(created = datetime.date.today(), SP = request.user).count()
            if report < 1:
                p, created = giftReport.objects.get_or_create(SP=request.user, gift1_received=gift1_received, 
                                                        gift2_received=gift2_received, gift3_received=gift3_received)
                p.save()
                return render(request, "report/create-list-gift-receive.html", {'gift1_received':gift1_received, 'gift2_received':gift2_received,
                    'gift3_received':gift3_received, 'gift1_remaining':p.gift1_remaining,
                    'gift2_remaining': p.gift2_remaining, 'gift3_remaining': p.gift3_remaining })
            report = giftReport.objects.get(created = datetime.date.today(), SP = request.user)
            report.gift1_received = sum(gift1_received, report.gift1_received)
            report.gift2_received = sum(gift2_received, report.gift2_received)
            report.gift3_received = sum(gift3_received, report.gift3_received)
            report.save()
            return render(request, "report/create-list-gift-receive.html", {'gift1_received':gift1_received, 'gift2_received':gift2_received,
                    'gift3_received':gift3_received, 'gift1_remaining':report.gift1_received,
                    'gift2_remaining': report.gift2_received, 'gift3_remaining': report.gift3_received })
    else:
        form = gift_ReceiveReportForm()
        return render(request,"report/listgift-received.html", {'form':form})


def gift_givenReport(request):
    if request.method == "POST":
        form = gift_givenReportForm(request.POST,is_salePerson=request.user.is_salePerson)
        if form.is_valid():
            gift1_given = form.cleaned_data.get('gift1_given')
            gift2_given = form.cleaned_data.get('gift2_given')
            gift3_given = form.cleaned_data.get('gift3_given')   

            report = giftReport.objects.get(created = datetime.date.today(), SP = request.user)
            report.gift1_given = sum(gift1_given, report.gift1_given)
            report.gift2_given = sum(gift2_given, report.gift2_given)
            report.gift3_given = sum(gift3_given, report.gift3_given)
            report.save()

            return redirect('listgift-remain')
    else:
        form = gift_givenReportForm()
        return render(request,"report/listgift-sent.html", {'form':form})

def gift_remaining(request):
    try:
        report = giftReport.objects.get(created = datetime.date.today(), SP = request.user)
        return render(request,'report/listgift-remain.html', {'gift1_remaining':report.gift1_remaining,
            'gift2_remaining': report.gift2_remaining, 'gift3_remaining': report.gift3_remaining})
    except:
        redirect('quantity-gift')