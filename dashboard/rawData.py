from outlet.models import tableReport, Campain, consumerApproachReport, report_sale, outletInfo, giftReport
from users.models import SalePerson
from .charts import sum, sum_table, percent

def Table_share(campain_id, table_rp):
    total_table = 0
    total_table_HVN = 0
    total_brand_table = 0
    other_table = 0
    other_beer_table = 0
    percent_table_share = 0
    for table in table_rp:
        total_table_HVN = sum(total_table_HVN, table.HVN_table)
        total_brand_table = sum(total_brand_table, table.brand_table)
        other_table = sum(other_table, table.other_table)
        other_beer_table = sum(other_beer_table, table.other_beer_table)
    total_table = sum_table(total_table_HVN, total_brand_table, other_table, other_beer_table)
    
    if total_table > 0:
        percent_table_share =  percent(total_brand_table, total_table)

    return total_table, total_brand_table, total_table_HVN, other_beer_table, other_table, percent_table_share

def sales_volume(campain_id, all_report_sale):
    # Cp = Campain.objects.get(id = campain_id)
    total_beer_brand = 0
    total_beer_HVN = 0
    total_beer_other = 0
    # all_report_sale =  report_sale.objects.filter(campain=Cp)
    for volume_sale in all_report_sale:
        total_beer_brand = sum(total_beer_brand, volume_sale.beer_brand)
        total_beer_HVN = sum(total_beer_HVN, volume_sale.beer_HVN)
        total_beer_other = sum(total_beer_other, volume_sale.beer_other)
        
    return total_beer_brand, total_beer_HVN, total_beer_other

def consumers_reached_rawdata(campain_id, consumers_rp):
   
    consumers_approach = 0
    total_bought_consumers = 0
    total_consumers = 0
    consumers_reach = 0
    conversion = 0
    
    for customer in consumers_rp:
        consumers_approach = sum(consumers_approach, customer.consumers_approach)
        total_consumers = sum(total_consumers, customer.Total_Consumers)
        total_bought_consumers = sum(total_bought_consumers, customer.consumers_brough)
    
    if total_consumers > 0:
        consumers_reach = percent(consumers_approach, total_consumers)
    if consumers_approach > 0:
        conversion = percent(total_bought_consumers, consumers_approach)

    return total_consumers, consumers_approach , consumers_reach, total_bought_consumers, conversion 


def gift_rawdata(campain_id, gift_rp):
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
    
    total_gift1_remaining = 0
    total_gift2_remaining = 0
    total_gift3_remaining = 0
    total_gift4_remaining = 0
    total_gift5_remaining = 0
    total_gift6_remaining = 0
    total_gift7_remaining = 0
    for gift in gift_rp:
        total_gift1_receive = gift.gift1_received
        total_gift2_receive = gift.gift2_received
        total_gift3_receive = gift.gift3_received
        total_gift4_receive = gift.gift4_received
        total_gift5_receive = gift.gift5_received
        total_gift6_receive = gift.gift6_received
        total_gift7_receive = gift.gift7_received

        total_gift1_given = gift.gift1_given
        total_gift2_given = gift.gift2_given
        total_gift3_given = gift.gift3_given
        total_gift4_given = gift.gift4_given
        total_gift5_given = gift.gift5_given
        total_gift6_given = gift.gift6_given
        total_gift7_given = gift.gift7_given
        
        total_gift1_remaining = gift.gift1_remaining
        total_gift2_remaining = gift.gift2_remaining
        total_gift3_remaining = gift.gift3_remaining
        total_gift4_remaining = gift.gift4_remaining
        total_gift5_remaining = gift.gift5_remaining
        total_gift6_remaining = gift.gift6_remaining
        total_gift7_remaining = gift.gift7_remaining
        
    gift_6 = [total_gift1_receive, total_gift2_receive, total_gift3_receive, total_gift4_receive, total_gift5_receive, total_gift6_receive, total_gift1_given, total_gift2_given, total_gift3_given, total_gift4_given, total_gift5_given, total_gift6_given, total_gift1_remaining, total_gift2_remaining, total_gift3_remaining, total_gift4_remaining, total_gift5_remaining, total_gift6_remaining]

    list_4 = [total_gift1_receive, total_gift2_receive, total_gift3_receive, total_gift4_receive, 0, 0,total_gift1_given, total_gift2_given, total_gift3_given, total_gift4_given, 0, 0, total_gift1_remaining, total_gift2_remaining, total_gift3_remaining, total_gift4_remaining, 0, 0]

    list4_scheme1 = [total_gift5_receive, total_gift2_receive, total_gift3_receive, total_gift6_receive, total_gift5_given, total_gift2_given, total_gift3_given, total_gift6_given, total_gift5_remaining, total_gift2_remaining, total_gift3_remaining, total_gift6_remaining]

    list2_scheme1 = [total_gift1_receive, total_gift2_receive, total_gift3_receive, total_gift7_receive, 0, 0, total_gift1_given, total_gift2_given, total_gift3_given, total_gift7_given, 0,0,total_gift1_remaining, total_gift2_remaining, total_gift3_remaining, total_gift7_remaining, 0 , 0]
    
    gift_3 = [total_gift1_receive, total_gift2_receive, total_gift3_receive, total_gift1_given, total_gift2_given, total_gift3_given, total_gift1_remaining, total_gift2_remaining, total_gift3_remaining]

    list_6_scheme1 = [total_gift1_receive, total_gift2_receive, total_gift1_given, total_gift2_given, total_gift1_remaining, total_gift2_remaining]
    list_6_scheme2 = [total_gift3_receive, total_gift4_receive, total_gift3_given, total_gift4_given, total_gift3_remaining, total_gift4_remaining]
    list_6_scheme3 = [total_gift3_receive, total_gift4_receive, total_gift3_given, total_gift4_given, total_gift3_remaining, total_gift4_remaining]
    list_6_scheme4 = [total_gift3_receive, total_gift2_receive, total_gift3_given, total_gift2_given, total_gift3_remaining, total_gift2_remaining]
    list_6_scheme5 = [total_gift2_receive, total_gift2_given, total_gift2_remaining]

    if campain_id == 1:
        list_gift_name = ['Ly 30cl','Ly 33cl 3D','Ly Casablanca', 'Ví', 'Nón Tiger Crystal', 'Voucher Bia']
        return gift_6,  list_gift_name

    elif campain_id == 2:
        list_gift = ['Ly 30cl', 'Voucher beer', 'Festive Box', 'Túi du lịch Tiger', 'Loa Tiger', 'Ví Tiger ', 'Iphone 13']
    
        return list2_scheme1, gift_6
    elif campain_id == 3:
        list_gift_name = ['E-voucher 25k', 'E-voucher 50k', 'E-voucher 100k']
        return gift_3, list_gift_name
    elif campain_id == 4:
        list_gift = ['Pin sạc', 'Ba lô', 'Bình Nước', 'Áo thun', 'Loa Bluetooth', 'Ly']
        
        return list_4, list4_scheme1

    elif campain_id == 5:
        list_gift_name = ['Heineken Alu', 'Ba lô', 'Combo Thời Trang', 'Combo Thể Thao']
        return list_4, list_gift_name
    
    elif campain_id == 6:
        list_gift = ['Nón Strongbow', 'Túi Jute Bag', 'Túi Canvas ', 'Dù SB']
        return list_6_scheme1, list_6_scheme2, list_6_scheme3, list_6_scheme4, list_6_scheme5

    elif campain_id == 7:
        list_gift_name = ['Túi du lịch', 'Đồng Hồ Treo Tường', 'Bình Nước 1,6L', 'Ly']
        return list_4, list_gift_name
    
    elif campain_id == 8:
        list_gift_name = ['Áo thun', 'Thùng 12 Lon', 'Nón', 'Ly']
        return list_4, list_gift_name
    else:
        list_gift_name = ['Ba lô','Thùng 12 Lon', 'Nón', '02 Lon Larue']
        return list_4, list_gift_name
    


def get_gift_scheme_rawdata(campain_id, outlet_raw, list_gift_of_outlet):
    Cp = Campain.objects.get(id = campain_id)

    if campain_id == 2:
        categories = ['Long An', 'Tiền Giang', 'Bạc Liêu', 'Cần Thơ', 'An Giang', 'Kiên Giang']
        list_gift_name1 = ['Ly 30cl', 'Voucher beer', 'Festive Box', 'Iphone 13']
        list_gift_name2 = ['Ly 30cl', 'Voucher beer', 'Festive Box', 'Túi du lịch Tiger', 'Loa Tiger', 'Ví Tiger ']
        result_scheme2 = [0,0,0,0,0,0]
        result_scheme1 = [0,0,0,0,0,0]
        #result_scheme2[1] = 
        #result_scheme1[0] = 
        if outlet_raw.province in categories:
            result_scheme2 = gift_rawdata(campain_id, list_gift_of_outlet)
        else:
            result_scheme1 = gift_rawdata(campain_id, list_gift_of_outlet)
        
        return result_scheme1[0], list_gift_name1, result_scheme2[1],  list_gift_name2

    elif campain_id == 4:
        categories = ['HCM', 'Hà Nội', 'Nha Trang' ,'Đà Nẵng']
        list_gift_name1 = ['Pin sạc', 'Ba lô', 'Bình Nước', 'Áo thun']
        list_gift_name2 = ['Loa Bluetooth', 'Ba lô', 'Bình Nước', 'Ly']
        result_scheme2 = [0,0,0,0,0,0]
        result_scheme1 = [0,0,0,0,0,0]

        if outlet_raw.province in categories:
            result_scheme = gift_rawdata(campain_id, list_gift_of_outlet)
        else:
            result_scheme1 = gift_rawdata(campain_id, list_gift_of_outlet)
        return result_scheme[0] ,list_gift_name1, result_scheme1[1], list_gift_name2
          
    
    elif campain_id == 6:
        list_gift_name1 = ['Nón Strongbow', 'Túi Jute Bag']
        list_gift_name2 = ['Túi Canvas ', 'Dù SB']
        list_gift_name3 = ['Túi Canvas ', 'Túi Jute Bag']
        list_gift_name4 = ['Túi Jute Bag']

        categories1 = ['GSO', 'YSO', 'QN']
        categories2 = ['Hot Zone']
        categories3 = ['Karaoke']
        categories4 = ['Beer Cafe']
        categories5 = ['Restaurant']
        result_scheme1 =[0,0,0,0,0,0]
        result_scheme2 = [0,0,0,0,0,0]
        result_scheme3 = [0,0,0,0,0,0]
        result_scheme4 =[0,0,0,0,0,0]
        result_scheme5 =  [0,0,0,0,0,0]
        if outlet_raw.type in categories2:
            result_scheme2 = gift_rawdata(campain_id, list_gift_of_outlet)
        elif outlet_raw.type in categories3:
            result_scheme3 = gift_rawdata(campain_id, list_gift_of_outlet)      
        elif outlet_raw.type in categories4:
            result_scheme4 = gift_rawdata(campain_id, list_gift_of_outlet)       
        elif outlet_raw.type in categories5:
            result_scheme5 = gift_rawdata(campain_id, list_gift_of_outlet)
        else :
            #if outlet_raw.type in categories1:
            result_scheme1 = gift_rawdata(campain_id, list_gift_of_outlet)
        
        return result_scheme1[0], list_gift_name1, result_scheme2[1], list_gift_name2, result_scheme3[2], list_gift_name2, result_scheme4[3], list_gift_name3, result_scheme5[4], list_gift_name4