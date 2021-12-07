from django.shortcuts import render, redirect
from outlet.models import tableReport, report_sale
from outlet.forms import tableReportForm, reportSaleForm
from django.views.generic import  DayArchiveView
import datetime
# Create your views here.



def sum(a, b):
    return str(int(a) + int(b))


def reportTable(request):

    if request.method == "POST":
        form = tableReportForm(request.POST,is_salePerson=request.user.is_salePerson)
        if form.is_valid():
            other_beer_table = form.cleaned_data.get('other_beer_table')
            brand_table = form.cleaned_data.get('brand_table')
            HVN_table = form.cleaned_data.get('HVN_table')
            total_table = form.cleaned_data.get('total_table')
            other_table = form.cleaned_data.get('other_table')
            
            report_table = tableReport.objects.filter(created = datetime.date.today(), SP = request.user).count()

            if report_table < 1:
                p, created = tableReport.objects.get_or_create(SP=request.user, other_beer_table=other_beer_table, 
                    total_table=total_table, other_table=other_table, brand_table=brand_table,  HVN_table=HVN_table)
                p.save()
                return render(request,"report/create_reportTable.html", {'other_beer_table':other_beer_table, 'brand_table':brand_table,
                                    'HVN_table':HVN_table,'total_table':total_table, 'other_table':other_table})

           
            report_table = tableReport.objects.get(created = datetime.date.today(), SP = request.user)
            
            report_table.other_beer_table = sum(other_beer_table, report_table.other_beer_table)
            report_table.total_table = sum(total_table, report_table.total_table)
            report_table.other_table = sum(other_table, report_table.other_table)
            report_table.brand_table = sum(brand_table, report_table.brand_table)
            report_table.HVN_table = sum(HVN_table, report_table.HVN_table)
            report_table.save()
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