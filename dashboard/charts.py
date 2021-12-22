import json
from django.db.models import Q
from outlet.models import tableReport, Campain, consumerApproachReport, report_sale, outletInfo, giftReport

def sum(a, b):
    return int(int(a) + int(b))

def sum_sale(a,b,c):
    return int(a) + int(b) + int(c)

def sum_table(a, b, c, d):
    return int(int(a) + int(b) + int(c) + int(d))

def percent(a,b):
    return round((int(a)*100)/(int(b)), 0)

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
   
    Cp = Campain.objects.get(id = campain_id)
    ctm_reached = 0
    total_bought_consumers = 0
    total_consumers = 0
    per_reached = 0
    average_conversion = 0
    consumers_rp = consumerApproachReport.objects.filter(campain=Cp)
    for customer in consumers_rp:
        ctm_reached = sum(ctm_reached, customer.consumers_approach)
        total_consumers = sum(total_consumers, customer.Total_Consumers)
        total_bought_consumers = sum(total_bought_consumers, customer.consumers_brough)
    
    if total_consumers > 0  and ctm_reached > 0:
        per_reached = percent(ctm_reached, total_consumers)
        average_conversion = percent(total_bought_consumers, ctm_reached)

    return total_consumers, ctm_reached, total_bought_consumers, per_reached, average_conversion

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

def VOLUME_PERFORMANCE(campain_id):
    if campain_id == 1:
        volume_achieved = 168
    elif campain_id == 2:
        volume_achieved = 360
    elif campain_id == 3:
        volume_achieved = 120
    elif campain_id == 4:
        volume_achieved = 120
    elif campain_id == 5:
        volume_achieved = 480
    elif campain_id == 6:
        volume_achieved = 48
    elif campain_id == 7:
        volume_achieved = 192
    elif campain_id == 8:
        volume_achieved = 192
    else :
        volume_achieved = 192

    Cp = Campain.objects.get(id = campain_id)
    all_outlet = outletInfo.objects.filter(compain=Cp)
    count = 0
    total_sale = 0
    for outlet in all_outlet:
        all_report_sale =  report_sale.objects.filter(campain=Cp, outlet=outlet)
        count_report_sale =  report_sale.objects.filter(campain=Cp, outlet=outlet).count()  #report of outlet
        if count_report_sale > 0:
            count = count + 1
            for report_Sale in all_report_sale:
                total_sale = sum(total_sale, report_Sale.beer_brand)
    
    average_volume = 0
    if count > 0:
        average_volume = (total_sale)/(count)
    
    total_volume_achieved = volume_achieved * count

    return [total_sale, total_volume_achieved , average_volume, volume_achieved]

def activation_progress(campain_id):
    Cp = Campain.objects.get(id = campain_id)
    all_outlet = outletInfo.objects.filter(compain=Cp)
    count = 0
    list = []
    for outlet in all_outlet:
        all_report_sale =  report_sale.objects.filter(campain=Cp, outlet=outlet)
        for rp_sale in all_report_sale:
            if rp_sale.SP != list:
                list.append(rp_sale)
                count = count + 1
    
    return count

    
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

def gift(campain_id):
    Cp = Campain.objects.get(id = campain_id)
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

    list_gift_rp = giftReport.objects.filter(campain = Cp)
    #all report in 1 outlet
    
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
    
    percent_gift1 =0
    percent_gift2 = 0
    percent_gift3 = 0
    percent_gift4 = 0
    percent_gift5 = 0
    percent_gift6 = 0

    if total_gift1_receive != 0:
        percent_gift1 = percent(total_gift1_given, total_gift1_receive)
    if total_gift2_receive != 0:
        percent_gift2 = percent(total_gift2_given, total_gift2_receive)
    if total_gift3_receive != 0:
        percent_gift3 = percent(total_gift3_given, total_gift3_receive)
    if total_gift4_receive != 0:
        percent_gift4 = percent(total_gift4_given, total_gift4_receive)
    if total_gift5_receive != 0:
        percent_gift5 = percent(total_gift5_given, total_gift5_receive)
    if total_gift5_receive != 0:
        percent_gift6 = percent(total_gift6_given, total_gift6_receive)
    list = [percent_gift1, percent_gift2, percent_gift3, percent_gift4, percent_gift5, percent_gift6]
    list_4 = [percent_gift1, percent_gift2, percent_gift3, percent_gift4]
    list_gift = []

    if campain_id == 4:
        list_gift = ['Pin sạc', 'Ba lô', 'Bình Nước', 'Áo thun', 'Loa Bluetooth', 'Ly']
        return list, list_gift

    elif campain_id == 5:
        list_gift = ['Heineken Alu', 'Ba lô', 'Combo Thời Trang', 'Combo Thể Thao']
        return list_4, list_gift

    elif campain_id == 7:
        list_gift = ['Túi du lịch', 'Đồng Hồ Treo Tường', 'Bình Nước 1,6L', 'Ly']
        return list_4, list_gift
    
    elif campain_id == 8:
        list_gift = ['Áo thun', 'Thùng 12 Lon', 'Nón', 'Ly']
        return list_4, list_gift

    return list, list_gift
