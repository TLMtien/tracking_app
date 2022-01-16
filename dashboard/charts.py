import json
from django.db.models import Q
from outlet.models import tableReport, Campain, consumerApproachReport, report_sale, outletInfo, giftReport
from users.models import SalePerson
from operator import and_
from functools import reduce
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
    
    

def Average_Sale_volume(all_sale_report):
    result = 0
    beer_brand = 0
    beer_HVN = 0
    beer_other = 0
    for rp in all_sale_report:
        beer_brand = sum(beer_brand, rp.beer_brand)
        beer_HVN = sum(beer_HVN, rp.beer_HVN)
        beer_other = sum(beer_other, rp.beer_other)
    total_Sale = sum_sale(beer_brand, beer_HVN, beer_other)
    try:
        result = percent(beer_brand, total_Sale)
    except:
        result = 0
    return result

def Average_table_share(all_table_report):
    result = 0
    brand_table = 0
    total_table = 0

    for rp in all_table_report:
        brand_table = sum(brand_table, rp.brand_table)
        total_table = sum(total_table, rp.total_table)
    try:
        result = percent(brand_table, total_table)
    except:
        result = 0
    return result

def pie_chart(campain_id, table_rp):
    try:
        total_table = 0
        total_table_HVN = 0
        total_brand_table = 0
        other_table = 0
        other_beer_table = 0
        # Cp = Campain.objects.get(id = campain_id)
        # table_rp = tableReport.objects.filter(campain=Cp)
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

def total_consumers_reached(campain_id, consumers_rp):
   
    # Cp = Campain.objects.get(id = campain_id)
    # consumers_rp = consumerApproachReport.objects.filter(campain=Cp)
    ctm_reached = 0
    total_bought_consumers = 0
    total_consumers = 0
    per_reached = 0
    average_conversion = 0
    
    for customer in consumers_rp:
        ctm_reached = sum(ctm_reached, customer.consumers_approach)
        total_consumers = sum(total_consumers, customer.Total_Consumers)
        total_bought_consumers = sum(total_bought_consumers, customer.consumers_brough)
    
    if total_consumers > 0  and ctm_reached > 0:
        per_reached = percent(ctm_reached, total_consumers)
        average_conversion = percent(total_bought_consumers, ctm_reached)

    return total_consumers, ctm_reached, total_bought_consumers, per_reached, average_conversion

def HNK_volume_sale(campain_id, all_report_sale):
    try:
        # Cp = Campain.objects.get(id = campain_id)
        total_beer_brand = 0
        total_beer_HVN = 0
        total_beer_other = 0
        # all_report_sale =  report_sale.objects.filter(campain=Cp)
        for volume_sale in all_report_sale:
            total_beer_brand = sum(total_beer_brand, volume_sale.beer_brand)
            total_beer_HVN = sum(total_beer_HVN, volume_sale.beer_HVN)
            total_beer_other = sum(total_beer_other, volume_sale.beer_other)
        total = sum_sale(total_beer_brand, total_beer_HVN, total_beer_other)
        return percent(total_beer_brand, total)
    except:
        return 0

def VOLUME_PERFORMANCE(campain_id, all_outlet, from_date, to_date):
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
    # all_outlet = outletInfo.objects.filter(compain=Cp)
    count = 0
    count_volume_achieved = 0
    total_sale = 0
    list_province = []
    list_name_outlet = []
    list_type = []
    for outlet in all_outlet:
        all_report_sale =  report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
        count_report_sale =  report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet).count()  #report of outlet
        count_gift =  giftReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet).count()
        if count_report_sale > 0 or count_gift>0:
            if not outlet.province in list_province:        #filter province
                list_province.append(outlet.province)
            if not outlet.outlet_Name in list_name_outlet:        #filter province
                list_name_outlet.append(outlet.outlet_Name)
            if not outlet.type in list_type:        #filter province
                list_type.append(outlet.type)

            count = count + 1
            count_volume_achieved = count_volume_achieved + volume_achieved
            for report_Sale in all_report_sale:
                total_sale = sum(total_sale, report_Sale.beer_brand)
    
    average_volume = 0
    if count_volume_achieved  > 0:
        average_volume = percent(total_sale, count_volume_achieved )
    
    total_volume_achieved = volume_achieved * count

    return [total_sale, total_volume_achieved , average_volume, volume_achieved, list_province, list_name_outlet, list_type]

def activation_progress(campain_id, all_outlet, from_date, to_date):
    Cp = Campain.objects.get(id = campain_id)
    if campain_id == 1:
        total_act = 8194
    elif campain_id == 2:
        total_act = 1188
    elif campain_id == 3:
        total_act = 700
    elif campain_id == 4:
        total_act = 720
    elif campain_id == 5:
        total_act = 800
    elif campain_id == 6:
        total_act = 1500
    elif campain_id == 7:
        total_act = 2700
    elif campain_id == 8:
        total_act = 2580
    else :
        total_act = 660
   
    count = 0
    list = []
    
    for outlet in all_outlet:
        all_report_table = tableReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
        rp_sale =  report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
        all_gift_rp = giftReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
    
        for rp_sale in all_report_table:
            if rp_sale.SP != list:
                list.append(rp_sale.SP)
                count = count + 1
    
    return count, total_act

    
def top10_outlet(campain_id, all_outlet, from_date, to_date):
    
        Cp = Campain.objects.get(id = campain_id)
        
        list_volume = []
        list_table = []
        list_name = []
        new_list_volume = []
        new_list_table = []
        new_list_name = []

        new_list_volume_reverse = []
        new_list_table_reverse = []
        new_list_name_reverse = []
        # all_outlet = outletInfo.objects.filter(compain=Cp)
        for outlet in all_outlet:
            all_report_sale =  report_sale.objects.filter(campain=Cp, outlet=outlet, created__gte=from_date).filter(campain=Cp, outlet=outlet, created__lte=to_date)
            
            table_rp = tableReport.objects.filter(campain=Cp, outlet=outlet, created__gte=from_date).filter(campain=Cp, outlet=outlet, created__lte=to_date)

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
        new_list = sorted(list_volume, reverse=True)
        for i in range(len(new_list)):
            for j in range(len(list_volume)):
                if(new_list[i] == list_volume[j]):
                    if not   list_name[j] in new_list_name:
                        new_list_volume.append(list_volume[j])
                        new_list_table.append(list_table[j])
                        new_list_name.append(list_name[j])
        #---------------------------------------------------->>
        new_list_reverse = sorted(list_volume)    
        for i in range(len(new_list_reverse)):
            for j in range(len(list_volume)):
                if(new_list_reverse[i] == list_volume[j]):
                    if not  list_name[j] in new_list_name_reverse:
                        new_list_volume_reverse.append(list_volume[j])
                        new_list_table_reverse.append(list_table[j])
                        new_list_name_reverse.append(list_name[j])

        return new_list_volume, new_list_table, new_list_name, new_list_volume_reverse, new_list_table_reverse, new_list_name_reverse
    
    
def volume_achieved_byProvince(campain_id, all_outlet):
    list_province = []
    Cp = Campain.objects.get(id = campain_id)
    # all_outlet = outletInfo.objects.filter(compain=Cp)
    
    # filter province

    for outlet in all_outlet:
        if not outlet.province in list_province: 
            list_province.append(outlet.province)
    result = 0
    test = []
    for pro in range(len(list_province)):
        list_outlet_province = []
        for outlet in all_outlet:
            if outlet.province in list_province[pro]:
                #list_outlet_province = all_outlet.filter(province=list_province[pro])  #filter outlet in province
                list_outlet_province.append(outlet)
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

# ------------------>>>>>>GIFT
def gift(campain_id, list_gift_rp):
    Cp = Campain.objects.get(id = campain_id)
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

    #list_gift_rp = giftReport.objects.filter(campain = Cp)
    #all report in 1 outlet
    
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
    
    percent_gift1 =0
    percent_gift2 = 0
    percent_gift3 = 0
    percent_gift4 = 0
    percent_gift5 = 0
    percent_gift6 = 0
    percent_gift7 = 0

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
    if total_gift6_receive != 0:
        percent_gift6 = percent(total_gift6_given, total_gift6_receive)
    
    if total_gift7_receive != 0:
        percent_gift7 = percent(total_gift7_given, total_gift7_receive)

    list = [percent_gift1, percent_gift2, percent_gift3, percent_gift4, percent_gift5, percent_gift6]
    list_4 = [percent_gift1, percent_gift2, percent_gift3, percent_gift4]
    list_7 = [percent_gift1, percent_gift2, percent_gift3, percent_gift4, percent_gift5, percent_gift6, percent_gift7]
    

    if campain_id == 4:
        list_gift = ['Pin sạc', 'Ba lô', 'Bình Nước', 'Áo thun', 'Loa Bluetooth', 'Ly']
        list_gift_1 = [percent_gift1, percent_gift2, percent_gift3, percent_gift4]
        
        list_gift_2 = [percent_gift5, percent_gift2, percent_gift3, percent_gift6]
        return list, list_gift, list_gift_1, list_gift_2

    elif campain_id == 1:
        list_gift = ['Ly 30cl','Ly 33cl 3D','Ly Casablanca', 'Ví', 'Nón Tiger Crystal', 'Voucher Bia']
        return list, list_gift

    elif campain_id == 2:
        list_gift = ['Ly 30cl', 'Voucher beer', 'Festive Box', 'Túi du lịch Tiger', 'Loa Tiger', 'Ví Tiger ', 'Iphone 13']
        list_gift_1 = [percent_gift1, percent_gift2, percent_gift3, percent_gift7]
        
        list_gift_2 = [percent_gift1, percent_gift2, percent_gift3, percent_gift4, percent_gift5, percent_gift6]
        return list_7, list_gift, list_gift_1, list_gift_2

    elif campain_id == 5:
        list_gift = ['Heineken Alu', 'Ba lô', 'Combo Thời Trang', 'Combo Du Lịch']
        return list_4, list_gift
    
    elif campain_id == 6:
        list_gift = ['Nón Strongbow', 'Túi Jute Bag', 'Túi Canvas ', 'Dù SB']
        list_gift_1 = [percent_gift1, percent_gift2]
        list_gift_2 = [percent_gift3, percent_gift4]
        list_gift_3 = [percent_gift3, percent_gift2]
        list_gift_4 = [percent_gift2]
        return list_4, list_gift, list_gift_1, list_gift_2, list_gift_3, list_gift_4

    elif campain_id == 7:
        list_gift = ['Túi du lịch', 'Đồng Hồ Treo Tường', 'Bình Nước 1,6L', 'Ly']
        return list_4, list_gift
    
    elif campain_id == 8:
        list_gift = ['Áo thun', 'Thùng 12 Lon', 'Nón', 'Ly']
        return list_4, list_gift
    else:
        list_gift = ['Ba lô','Thùng 12 Lon', 'Nón', '02 Lon Larue']
        return list_4, list_gift
    

# get outlet_province
def get_outlet_province(campain_id, province, from_date, to_date):
    list_outlet = []
    list_type = []
    Cp = Campain.objects.get(id = campain_id)

    for pro in province:
        #all_outlet_province = outletInfo.objects.filter(compain=Cp, province=pro, created_by_HVN=True)
        # all_outlet_province
        all_outlet_province = []
        Cp = Campain.objects.get(id=campain_id)
        sale_person = SalePerson.objects.filter(brand__pk=campain_id)  # all_SP
        for SP in sale_person:
            outlet=SP.outlet
            rp_table = tableReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
            rp_sale =  report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
            gift_rp = giftReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
        
            if rp_table.exists() or rp_sale.exists() or gift_rp.exists():
                
                if not outlet in all_outlet_province and outlet.created_by_HVN and outlet.province==pro:
                    all_outlet_province.append(outlet)
        # end
        for outlet in all_outlet_province:
            count_report_sale =  report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet).count()  #report of outlet
            count_gift =  giftReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet).count()
            count_table = tableReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet).count()
            if count_report_sale > 0 or count_gift > 0 or count_table > 0:
                if not outlet.type in list_type: 
                    list_type.append(outlet.type)

                list_outlet.append(outlet)
    
        
    return list_outlet, list_type

def get_outlet_type(campain_id, type, from_date, to_date):
    list_outlet = []
    list_province = []
    Cp = Campain.objects.get(id = campain_id)
    for tp in type:
        #all_outlet_type = outletInfo.objects.filter(compain=Cp, type=tp, created_by_HVN=True)
        #filter outlet
        all_outlet_type = []
        Cp = Campain.objects.get(id=campain_id)
        sale_person = SalePerson.objects.filter(brand__pk=campain_id)  # all_SP
        for SP in sale_person:
            outlet=SP.outlet
            rp_table = tableReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
            rp_sale =  report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
            gift_rp = giftReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
        
            if rp_table.exists() or rp_sale.exists() or gift_rp.exists():
                
                if not outlet in all_outlet_type and outlet.created_by_HVN and outlet.type == tp:
                    all_outlet_type.append(outlet)
        #end get-outlet
        for outlet in all_outlet_type:
            count_report_sale =  report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet).count()  #report of outlet
            count_gift =  giftReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet).count()
            count_table = tableReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet).count()
            if count_report_sale > 0 or count_gift > 0 or count_table > 0:
                list_outlet.append(outlet)
    
    return list_outlet, list_province

def get_outlet_type_province(campain_id, list_province_type1, from_date, to_date):
    Cp = Campain.objects.get(id = campain_id)
    list_outlet = []
    list_outlet1 = []
    list_province = []
    list_type = []
    list_province_type = []
    for i in list_province_type1:
        if not i in  list_province_type:
            list_province_type.append(i)

            
    for list in list_province_type:
        #all_outlet_province = outletInfo.objects.filter(compain=Cp, province=list, created_by_HVN=True)
        # filter outlet
        all_outlet_province = []
        Cp = Campain.objects.get(id=campain_id)
        sale_person = SalePerson.objects.filter(brand__pk=campain_id)  # all_SP
        for SP in sale_person:
            outlet=SP.outlet
            rp_table = tableReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
            rp_sale =  report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
            gift_rp = giftReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
        
            if rp_table.exists() or rp_sale.exists() or gift_rp.exists():
                
                if not outlet in all_outlet_province and outlet.created_by_HVN and outlet.province == list:
                    all_outlet_province.append(outlet)
        # end filter outlet
        for outlet in all_outlet_province:
            count_report_sale =  report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet).count()  #report of outlet
            count_gift =  giftReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet).count()
            count_table = tableReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet).count()
            if count_report_sale > 0 or count_gift > 0 or count_table > 0:
                list_outlet1.append(outlet)
                if outlet.type in list_province_type:    
                    list_outlet.append(outlet)
    if len(list_outlet) == 0:
        list_outlet = list_outlet1
    if len(list_outlet1) == 0:
        for tp in list_province_type:
            #all_outlet_type = outletInfo.objects.filter(compain=Cp, type=tp, created_by_HVN=True)
            # filter outlet
            all_outlet_type = []
            Cp = Campain.objects.get(id=campain_id)
            sale_person = SalePerson.objects.filter(brand__pk=campain_id)  # all_SP
            for SP in sale_person:
                outlet=SP.outlet
                rp_table = tableReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
                rp_sale =  report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
                gift_rp = giftReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
            
                if rp_table.exists() or rp_sale.exists() or gift_rp.exists():
                    
                    if not outlet in all_outlet_type and outlet.created_by_HVN and outlet.type==tp:
                        all_outlet_type.append(outlet)
            # end filter outlet
            for outlet in all_outlet_type:
                count_report_sale =  report_sale.objects.filter(campain=Cp, outlet=outlet).count()  #report of outlet
                count_gift =  giftReport.objects.filter(campain = Cp, outlet=outlet).count()
                count_table = tableReport.objects.filter(campain = Cp, outlet=outlet).count()
                if count_report_sale > 0 or count_gift > 0 or count_table > 0:
                    list_outlet.append(outlet)
    return list_outlet, list_province

def get_outletName_type_province(campain_id, list_province_type_outletname):
    Cp = Campain.objects.get(id = campain_id)
    list_outlet = []
    list_outlet1 = []
    list_outlet2 = []
    list_province = []
    list_type = []
    for list in list_province_type_outletname:
        all_outlet_province = outletInfo.objects.filter(compain=Cp, province=list, created_by_HVN=True)
        for outlet in all_outlet_province:
            count_report_sale =  report_sale.objects.filter(campain=Cp, outlet=outlet).count()  #report of outlet
            count_gift =  giftReport.objects.filter(campain = Cp, outlet=outlet).count()
            count_table = tableReport.objects.filter(campain = Cp, outlet=outlet).count()
            if count_report_sale > 0 or count_gift > 0 or count_table > 0:
                list_outlet2.append(outlet)
                if outlet.type in list_province_type_outletname: 
                    list_outlet1.append(outlet)
                    if outlet.outlet_Name in list_province_type_outletname:    
                        list_outlet.append(outlet)
    if len(list_outlet) == 0:
        if len(list_outlet1) > 0:
            list_outlet = list_outlet1
        else:
            list_outlet = list_outlet2

    if len(list_outlet) == 0:
        for name in list_province_type_outletname:
            all_outlet_type = outletInfo.objects.filter(compain=Cp, outlet_Name=name, created_by_HVN=True)
            for outlet in all_outlet_type:
                count_report_sale =  report_sale.objects.filter(campain=Cp, outlet=outlet).count()  #report of outlet
                count_gift =  giftReport.objects.filter(campain = Cp, outlet=outlet).count()
                count_table = tableReport.objects.filter(campain = Cp, outlet=outlet).count()
                if count_report_sale > 0 or count_gift > 0 or count_table > 0:
                    list_outlet.append(outlet)
    return list_outlet, list_province

def get_outlet(campain_id, outlet_name):
    list_outlet = []
    list_province = []
    Cp = Campain.objects.get(id = campain_id)
    for name in outlet_name:
        all_outlet_type = outletInfo.objects.filter(compain=Cp, outlet_Name=name, created_by_HVN=True)
        for outlet in all_outlet_type:
            count_report_sale =  report_sale.objects.filter(campain=Cp, outlet=outlet).count()  #report of outlet
            count_gift =  giftReport.objects.filter(campain = Cp, outlet=outlet).count()
            count_table = tableReport.objects.filter(campain = Cp, outlet=outlet).count()
            if count_report_sale > 0 or count_gift > 0 or count_table > 0:
                list_outlet.append(outlet)
    return list_outlet, list_province

def getAll_report_outlet(campain_id, list_outlet, from_date, to_date):
    Cp = Campain.objects.get(id = campain_id)
    list_table = []
    list_consumer = []
    list_gift = []
    list_sale_volume = []
    for outlet in list_outlet:
        table_rp = tableReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
        consumers_rp = consumerApproachReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
        list_gift_rp = giftReport.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
        all_report_sale =  report_sale.objects.filter(created__gte=from_date, campain = Cp, outlet=outlet).filter(created__lte=to_date, campain = Cp, outlet=outlet)
        for rp in table_rp:
            list_table.append(rp)
        for rp in consumers_rp:
            list_consumer.append(rp)
        for rp in list_gift_rp:
            list_gift.append(rp)
        for rp in all_report_sale:
            list_sale_volume.append(rp)
    return list_table, list_consumer, list_gift, list_sale_volume
## filter Province
# def chart_filter_province(campain_id, province):
#     list_outlet = get_outlet_province(campain_id, province)
#     list_rp = getAll_report_outlet(campain_id, list_outlet)
#     pie = pie_chart(campain_id, list_rp[0])
#     consumers_charts = total_consumers_reached(campain_id, list_rp[1])
#     gift_charts = gift(campain_id, list_rp[2])
#     volume_performance = VOLUME_PERFORMANCE(campain_id, list_outlet)
#     top_10 = top10_outlet(campain_id, list_outlet)

def get_gift_scheme(campain_id):
    Cp = Campain.objects.get(id = campain_id)
    if campain_id == 2 :
        categories = ['Long An', 'Tiền Giang', 'Bạc Liêu', 'Cần Thơ', 'An Giang', 'Kiên Giang']
        list_gift_rp_scheme = []
        list_gift_rp_scheme1 = []
        list_gift_name1 = ['Ly 30cl', 'Voucher beer', 'Festive Box', 'Iphone 13']
        list_gift_name2 = ['Ly 30cl', 'Voucher beer', 'Festive Box', 'Túi du lịch Tiger', 'Loa Tiger', 'Ví Tiger ']
        for c in categories:
            all_outlet_scheme = outletInfo.objects.filter(compain = Cp, province =c)
            for outlet in all_outlet_scheme:
                count_report_sale =  report_sale.objects.filter(campain=Cp, outlet=outlet).count()  #report of outlet
                count_gift =  giftReport.objects.filter(campain = Cp, outlet=outlet).count()
                count_table = tableReport.objects.filter(campain = Cp, outlet=outlet).count()
                if count_report_sale > 0 or count_gift > 0 or count_table > 0:
                    list_gift = giftReport.objects.filter(campain = Cp, outlet=outlet)
                    for gift_1 in list_gift:
                        list_gift_rp_scheme.append(gift_1)

        for c in categories:
            all_outlet_scheme = outletInfo.objects.filter(compain = Cp).exclude(province =c)
            for outlet in all_outlet_scheme:
                count_report_sale =  report_sale.objects.filter(campain=Cp, outlet=outlet).count()  #report of outlet
                count_gift =  giftReport.objects.filter(campain = Cp, outlet=outlet).count()
                count_table = tableReport.objects.filter(campain = Cp, outlet=outlet).count()
                if count_report_sale > 0 or count_gift > 0 or count_table > 0:
                    list_gift = giftReport.objects.filter(campain = Cp, outlet=outlet)
                    for gift_1 in list_gift:
                        list_gift_rp_scheme1.append(gift_1)

        result_scheme = gift(campain_id, list_gift_rp_scheme)
        result_scheme1 = gift(campain_id, list_gift_rp_scheme1)
        return result_scheme[3],list_gift_name2, result_scheme1[2], list_gift_name1,  list_gift_name1, list_gift_name2, list_gift_name1, list_gift_name1, list_gift_name1, list_gift_name1
       

        # all_outlet_scheme = outletInfo.objects.filter(reduce(and_, [Q(compain = Cp, province =c) for c in categories]))
        # list_gift_name1 = ['Ly 30cl', 'Voucher beer', 'Festive Box', 'Iphone 13']
        # list_gift_name2 = ['Ly 30cl', 'Voucher beer', 'Festive Box', 'Túi du lịch Tiger', 'Loa Tiger', 'Ví Tiger ']
        # list_gift_rp_scheme = giftReport.objects.filter(reduce(and_, [Q(campain = Cp, outlet=outlet) for outlet in all_outlet_scheme]))
        # list_gift_rp_scheme1 = giftReport.objects.filter(campain = Cp).exclude(reduce(and_, [Q(outlet=outlet) for outlet in all_outlet_scheme]))
        # result_scheme = gift(campain_id, list_gift_rp_scheme)
        # result_scheme1 = gift(campain_id, list_gift_rp_scheme1)
        # return result_scheme[3],list_gift_name2, result_scheme1[2], list_gift_name1

    elif campain_id == 4:
        categories = ['HCM', 'Hà Nội', 'Nha Trang' ,'Đà Nẵng']
        list_gift_rp_scheme = []
        list_gift_rp_scheme1 = []
        for c in categories:
            all_outlet_scheme = outletInfo.objects.filter(compain = Cp, province =c)
            for outlet in all_outlet_scheme:
                count_report_sale =  report_sale.objects.filter(campain=Cp, outlet=outlet).count()  #report of outlet
                count_gift =  giftReport.objects.filter(campain = Cp, outlet=outlet).count()
                count_table = tableReport.objects.filter(campain = Cp, outlet=outlet).count()
                if count_report_sale > 0 or count_gift > 0 or count_table > 0:
                    list_gift = giftReport.objects.filter(campain = Cp, outlet=outlet)
                    for gift_1 in list_gift:
                        list_gift_rp_scheme.append(gift_1)

        for c in categories:
            all_outlet_scheme = outletInfo.objects.filter(compain = Cp).exclude(province =c)
            for outlet in all_outlet_scheme:
                count_report_sale =  report_sale.objects.filter(campain=Cp, outlet=outlet).count()  #report of outlet
                count_gift =  giftReport.objects.filter(campain = Cp, outlet=outlet).count()
                count_table = tableReport.objects.filter(campain = Cp, outlet=outlet).count()
                if count_report_sale > 0 or count_gift > 0 or count_table > 0:
                    list_gift = giftReport.objects.filter(campain = Cp, outlet=outlet)
                    for gift_1 in list_gift:
                        list_gift_rp_scheme1.append(gift_1)
        
        list_gift_name1 = ['Pin sạc', 'Ba lô', 'Bình Nước', 'Áo thun']

        list_gift_name2 = ['Loa Bluetooth', 'Ba lô', 'Bình Nước', 'Ly']
        #list_gift_rp_scheme = giftReport.objects.filter(reduce(and_, [Q(campain = Cp, outlet=outlet) for outlet in all_outlet_scheme]))
        #list_gift_rp_scheme1 = giftReport.objects.filter(campain = Cp).exclude(reduce(and_, [Q(outlet=outlet) for outlet in all_outlet_scheme]))
        result_scheme = gift(campain_id, list_gift_rp_scheme)
        result_scheme1 = gift(campain_id, list_gift_rp_scheme1)
        return result_scheme[2],list_gift_name1, result_scheme1[3], list_gift_name2, list_gift_name1, list_gift_name2, list_gift_name1, list_gift_name1, list_gift_name1, list_gift_name1
       
    
    elif campain_id == 6:
        ['Nón Strongbow', 'Túi Jute Bag', 'Túi Canvas ', 'Dù SB']
        list_gift_name1 = ['Nón Strongbow', 'Túi Jute Bag']
        list_gift_name2 = ['Túi Canvas ', 'Dù SB']
        list_gift_name3 = ['Túi Canvas ', 'Túi Jute Bag']
        list_gift_name4 = ['Túi Jute Bag']

        categories = ['GSO', 'YSO', 'QN']
        list_gift_rp_scheme1 = []
        list_gift_rp_scheme2 = []
        list_gift_rp_scheme3 = []
        list_gift_rp_scheme4 = []
        list_gift_rp_scheme5 = []
        for c in categories:
            all_outlet_scheme = outletInfo.objects.filter(compain = Cp, type =c)
            for outlet in all_outlet_scheme:
                count_report_sale =  report_sale.objects.filter(campain=Cp, outlet=outlet).count()  #report of outlet
                count_gift =  giftReport.objects.filter(campain = Cp, outlet=outlet).count()
                count_table = tableReport.objects.filter(campain = Cp, outlet=outlet).count()
                if count_report_sale > 0 or count_gift > 0 or count_table > 0:
                    list_gift = giftReport.objects.filter(campain = Cp, outlet=outlet)
                    for gift_1 in list_gift:
                        list_gift_rp_scheme1.append(gift_1)
        
        all_outlet_scheme = outletInfo.objects.filter(compain = Cp, type = 'Hot Zone')
        for outlet in all_outlet_scheme:
            count_report_sale =  report_sale.objects.filter(campain=Cp, outlet=outlet).count()  #report of outlet
            count_gift =  giftReport.objects.filter(campain = Cp, outlet=outlet).count()
            count_table = tableReport.objects.filter(campain = Cp, outlet=outlet).count()
            if count_report_sale > 0 or count_gift > 0 or count_table > 0:
                list_gift = giftReport.objects.filter(campain = Cp, outlet=outlet)
                for gift_1 in list_gift:
                    list_gift_rp_scheme2.append(gift_1)

        all_outlet_scheme = outletInfo.objects.filter(compain = Cp, type = 'Karaoke')
        for outlet in all_outlet_scheme:
            count_report_sale =  report_sale.objects.filter(campain=Cp, outlet=outlet).count()  #report of outlet
            count_gift =  giftReport.objects.filter(campain = Cp, outlet=outlet).count()
            count_table = tableReport.objects.filter(campain = Cp, outlet=outlet).count()
            if count_report_sale > 0 or count_gift > 0 or count_table > 0:
                list_gift = giftReport.objects.filter(campain = Cp, outlet=outlet)
                for gift_1 in list_gift:
                    list_gift_rp_scheme3.append(gift_1)
        
        all_outlet_scheme = outletInfo.objects.filter(compain = Cp, type = 'Beer Cafe')
        for outlet in all_outlet_scheme:
            count_report_sale =  report_sale.objects.filter(campain=Cp, outlet=outlet).count()  #report of outlet
            count_gift =  giftReport.objects.filter(campain = Cp, outlet=outlet).count()
            count_table = tableReport.objects.filter(campain = Cp, outlet=outlet).count()
            if count_report_sale > 0 or count_gift > 0 or count_table > 0:
                list_gift = giftReport.objects.filter(campain = Cp, outlet=outlet)
                for gift_1 in list_gift:
                    list_gift_rp_scheme4.append(gift_1)

        all_outlet_scheme = outletInfo.objects.filter(compain = Cp, type = 'Restaurant')
        for outlet in all_outlet_scheme:
            count_report_sale =  report_sale.objects.filter(campain=Cp, outlet=outlet).count()  #report of outlet
            count_gift =  giftReport.objects.filter(campain = Cp, outlet=outlet).count()
            count_table = tableReport.objects.filter(campain = Cp, outlet=outlet).count()
            if count_report_sale > 0 or count_gift > 0 or count_table > 0:
                list_gift = giftReport.objects.filter(campain = Cp, outlet=outlet)
                for gift_1 in list_gift:
                    list_gift_rp_scheme5.append(gift_1)

        result_scheme1 = gift(campain_id, list_gift_rp_scheme1)
        result_scheme2 = gift(campain_id, list_gift_rp_scheme2)
        result_scheme3 = gift(campain_id, list_gift_rp_scheme3)
        result_scheme4 = gift(campain_id, list_gift_rp_scheme4)
        result_scheme5 = gift(campain_id, list_gift_rp_scheme5)

        return result_scheme1[2], list_gift_name1, result_scheme2[3], list_gift_name2, result_scheme3[3], list_gift_name2, result_scheme4[4], list_gift_name3, result_scheme5[5], list_gift_name4
       
