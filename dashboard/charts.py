import json
from django.db.models import Q
from outlet.models import tableReport, Campain, consumerApproachReport, report_sale, outletInfo

def sum(a, b):
    return int(int(a) + int(b))

def sum_sale(a,b,c):
    return int(a) + int(b) + int(c)

def sum_table(a, b, c, d):
    return int(int(a) + int(b) + int(c) + int(d))

def percent(a,b):
    return round((int(a)*100)/(int(b)), 2)

def get_allReport_outlet(outlet, campain_id):
    Cp = Campain.objects.get(id=campain_id)
    total_sale = 0
    total_HNK = 0
    total_HVB = 0
    total_other_beer = 0
    total_table = 0
    list_rp_sale = report_sale.objects.filter(campain = Cp, outlet = outlet)
    list_rp_table = tableReport.objects.filter(campain = Cp, outlet = outlet)
    for rp_sale in list_rp_sale:
        total_sale = sum(total_sale, rp_sale.beer_brand)

    for rp_table in list_rp_table:
        total_HNK = sum(total_HNK, rp_table.brand_table)
        total_HVB = sum(total_HVB, rp_table.HVN_table)
        total_other_beer = sum(total_other_beer, rp_table.other_beer_table)
        total_table = sum(total_table, rp_table.total_table)
    
    

    

def pie_chart(campain_id):
    try:
        total_table = 0
        total_table_HVN = 0
        total_brand_table = 0
        other_table = 0
        other_beer_table = 0
        Cp = Campain.objects.get(id = campain_id)
        table_rp = tableReport.objects.filter(campain=Cp)
        for table in table_rp:
            total_table_HVN = sum(total_table_HVN, table.HVN_table)
            total_brand_table = sum(total_brand_table, table.brand_table)
            other_table = sum(other_table, table.other_table)
            other_beer_table = sum(other_beer_table, table.other_beer_table)

        total_table = sum_table(total_table_HVN, total_brand_table, other_table, other_beer_table)
        list = []
        percent_table_HVN = percent(total_table_HVN, total_table)
        percent_brand_table = percent(total_brand_table, total_table)
        percent_other_table = percent(other_table, total_table)
        percent_other_beer_table = percent(other_beer_table, total_table)
        list= [percent_table_HVN, percent_brand_table, percent_other_table, percent_other_beer_table]
        return list
    except:
        return [0,0,0,0]

def total_consumers_reached(campain_id):
    try:
        Cp = Campain.objects.get(id = campain_id)
        ctm_reached = 0
        total_consumers = 0
        consumers_rp = consumerApproachReport.objects.filter(campain=Cp)
        for customer in consumers_rp:
            ctm_reached = sum(ctm_reached, customer.consumers_approach)
            total_consumers = sum(total_consumers, customer.Total_Consumers)
        
        per_reached = percent(ctm_reached, total_consumers)
        return ctm_reached, per_reached
    except:
        return [0,0]

def HNK_volume_sale(campain_id):
    try:
        Cp = Campain.objects.get(id = campain_id)
        total_beer_brand = 0
        total_beer_HVN = 0
        total_beer_other = 0
        all_report_sale =  report_sale.objects.filter(campain=Cp)
        for volume_sale in all_report_sale:
            total_beer_brand = sum(total_beer_brand, volume_sale.beer_brand)
            total_beer_HVN = sum(total_beer_HVN, volume_sale.beer_HVN)
            total_beer_other = sum(total_beer_other, volume_sale.beer_other)
        total = sum_sale(total_beer_brand, total_beer_HVN, total_beer_other)
        return percent(total_beer_brand, total)
    except:
        return 0


def top10_outlet(campain_id):
    
        Cp = Campain.objects.get(id = campain_id)
        
        list_volume = []
        list_table = []
        list_name = []
        new_list_volume = []
        new_list_table = []
        new_list_name = []
        all_outlet = outletInfo.objects.filter(compain=Cp)
        for outlet in all_outlet:
            all_report_sale =  report_sale.objects.filter(campain=Cp, outlet=outlet)
            
            table_rp = tableReport.objects.filter(campain=Cp, outlet=outlet)

            sum_beer_brand = 0
            total_table_brand = 0
            total_table = 0
            #all report in 1 outlet
            

            for rp_table in table_rp:
                total_table_brand = sum(total_table_brand, rp_table.brand_table)
                total_table = sum(total_table, rp_table.total_table)

            for rp_sale in all_report_sale:
                sum_beer_brand = sum(sum_beer_brand, rp_sale.beer_brand)
            
            #Table share
            if total_table !=0:
                list_table.append(percent(total_table_brand, total_table))
                list_volume.append(sum_beer_brand)
                list_name.append(outlet.outlet_Name)
            
        #get 10 outlet
        new_list = sorted(list_volume)[-10:]
        for i in range(len(new_list)):
            for j in range(len(list_volume)):
                if(new_list[i] == list_volume[j]):
                    if not   list_name[j] in new_list_name:
                        new_list_volume.append(list_volume[j])
                        new_list_table.append(list_table[j])
                        new_list_name.append(list_name[j])

        return new_list_volume, new_list_table, new_list_name
    
    
def volume_achieved_byProvince(campain_id):
    list_province = []
    Cp = Campain.objects.get(id = campain_id)
    all_outlet = outletInfo.objects.filter(compain=Cp)
    
    # filter province

    for outlet in all_outlet:
        if not outlet.province in list_province: 
            list_province.append(outlet.province)
    result = 0
    test = []
    for pro in range(len(list_province)):
        list_outlet_province = all_outlet.filter(province=list_province[pro])  #filter outlet in province
        sale_outlet = []
        sum_sale_pro = 0
        for outlet in list_outlet_province:
            all_report_sale =  report_sale.objects.filter(campain=Cp, outlet=outlet)  #report of outlet
            total_sale = 0
            total_beer_HVN = 0
            total_beer_other = 0
            for report_Sale in all_report_sale:
                total_sale = sum(total_sale, report_Sale.beer_brand)
                total_beer_HVN = sum(total_beer_HVN, report_Sale.beer_HVN)
                total_beer_other = sum(total_beer_other, report_Sale.beer_other)
            sum_sale_pro = sum(sum_sale_pro, sum_sale(total_sale, total_beer_HVN, total_beer_other))
            sale_outlet.append(total_sale) #   mỗi outlet_sale
        
        for i in range(len(sale_outlet)):
            if sum_sale_pro !=0:
                result = sum(result,percent(sale_outlet[i], sum_sale_pro)) 
                test.append(percent(sale_outlet[i], sum_sale_pro))
    return result

    