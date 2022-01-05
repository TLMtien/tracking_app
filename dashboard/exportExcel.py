import datetime
import xlwt
#from outlet.models import tableReport, report_sale
from datetime import datetime
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.chart import (
    PieChart,
    Reference,
    BarChart, Series, Reference,
)
from outlet.models import tableReport, Campain, giftReport
from . charts import pie_chart, VOLUME_PERFORMANCE, activation_progress, top10_outlet, gift
from openpyxl.chart.series import DataPoint
from openpyxl.writer.excel import save_virtual_workbook
from .rawData import Table_share
def export_chart(campainID, all_outlet, from_date, to_date):
   
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment;filename={}.xlsx'.format(str(datetime.now()))
    wb = Workbook(write_only=True)
    #wb.remove(wb.active)
    ws = wb.create_sheet()

    ##activation
    Cp = Campain.objects.get(id = campainID)
    table_rp = tableReport.objects.filter(created__gte=from_date, campain = Cp).filter(created__lte=to_date, campain = Cp)
    pie=pie_chart(campainID, table_rp)
    volume_per = VOLUME_PERFORMANCE(campainID, all_outlet)
    activation = activation_progress(campainID, all_outlet)
    top10 = top10_outlet(campainID, all_outlet)
    list_gift_rp = giftReport.objects.filter(created__gte=from_date, campain = Cp).filter(created__lte=to_date, campain = Cp)
    gift_rp = gift(campainID, list_gift_rp)
    ## Volume
    rows = [
        ('Title', 'Average Brand Volume', 'Average Target Volume'),
        ('Average Brand Volume', volume_per[2], 0),
        ('Average Target Volume', volume_per[3], 0),
    ]

    for row1 in rows:
        ws.append(row1)


    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10
    chart1.title = "AVERAGE PERFORMANCE PER ACT"

    data1 = Reference(ws, min_col=2, min_row=1, max_row=3, max_col=3)
    cats = Reference(ws, min_col=1, min_row=2, max_row=3)
    chart1.add_data(data1, titles_from_data=True)
    chart1.set_categories(cats)
    #chart1.shape = 4
    chart1.type = "col"
    #chart1.style = 12
    chart1.grouping = "stacked"
    #chart1.overlap = 100
    ws.add_chart(chart1, "J1")

    ###############################
    data = [
        ['Pie', 'Sold'],
        ['HVN', pie[0]],
        ['Brand', pie[1]],
        ['Other', pie[2]],
        ['Other beer', pie[3]],
    ]

    for row in data:
        ws.append(row)

    pie = PieChart()
    labels = Reference(ws, min_col=1, min_row=5, max_row=8)
    data = Reference(ws, min_col=2, min_row=4, max_row=8)
    pie.add_data(data, titles_from_data=True)
    pie.set_categories(labels)
    pie.title = "TABLE SHARE PERFORMANCE"

    ws.add_chart(pie, "S1")

    ###################################################
    #ACtual
    rows = [
        ('Title', 'Actual Acts', 'Total Acts'),
        ('Total Acts', activation[1], 0),
        ('Actual Acts', activation[0], 0),
    ]

    for row1 in rows:
        ws.append(row1)
    chart3 = BarChart()
    chart3.type = "bar"
    chart3.style = 10
    chart3.title = "ACTIVATION PROGRESS"

    data1 = Reference(ws, min_col=2, min_row=9, max_row=12, max_col=3)
    cats = Reference(ws, min_col=1, min_row=10, max_row=12)
    chart3.add_data(data1, titles_from_data=True)
    chart3.set_categories(cats)
    chart3.type = "bar"
    #chart1.style = 12
    chart3.grouping = "stacked"
    #chart1.overlap = 100
    ws.add_chart(chart3, "A1")
    #gift
    gift5 = 'Gift'
    gift_value5 = 0 
    gift6 = 'Gift'
    gift_value6 = 0 
    gift7 = 'Gift'
    gift_value7 = 0 
    if campainID == 4 or campainID ==1 or campainID ==2 :
        gift5 = gift_rp[1][4]
        gift6 = gift_rp[1][5]
        gift_value5 = gift_rp[0][4]
        gift_value6 = gift_rp[0][5]
    if campainID == 2:
        gift7 = gift_rp[1][6]
        gift_value7 = gift_rp[0][6]
    rows = [
        ('Title', ),
        (gift_rp[1][0], gift_rp[0][0], 0),
        (gift_rp[1][1], gift_rp[0][1], 0),
        (gift_rp[1][2], gift_rp[0][2], 0),
        (gift_rp[1][3], gift_rp[0][3], 0),
        (gift5, gift_value5, 0),
        (gift6, gift_value6, 0),
        (gift7, gift_value7, 0),
    ]

    for row1 in rows:
        ws.append(row1)

    chart2 = BarChart()
    chart2.type = "col"
    chart2.style = 10
    #chart2.title = "AVERAGE PERFORMANCE PER ACT"

    data2 = Reference(ws, min_col=2, min_row=12, max_row=20, max_col=3)
    cats = Reference(ws, min_col=1, min_row=13, max_row=19)
    chart2.add_data(data2, titles_from_data=True)
    chart2.set_categories(cats)
    #chart1.shape = 4
    chart2.type = "col"
    chart2.style = 5
    chart2.grouping = "stacked"
    chart2.overlap = 100
    ws.add_chart(chart2, "AB1")
    ######################################################
    #VOLUME PERFORMANCE
    rows = [
        ('Title', 'ActualVolume', 'Target Volume'),
        ('Target Volume', volume_per[1], 0),
        ('ActualVolume', volume_per[0], 0),
    ]

    for row1 in rows:
        ws.append(row1)
    chart4 = BarChart()
    chart4.type = "bar"
    chart4.style = 10
    chart4.title = "VOLUME PERFORMANCE"

    data1 = Reference(ws, min_col=2, min_row=20, max_row=23, max_col=3)
    cats = Reference(ws, min_col=1, min_row=21, max_row=22)
    chart4.add_data(data1, titles_from_data=True)
    chart4.set_categories(cats)
    chart4.type = "bar"
    #chart1.style = 12
    chart4.grouping = "stacked"
    #chart1.overlap = 100
    ws.add_chart(chart4, "A16")
    # TOP 10

    rows = [
       
    ]
    # ('Title', ),
        
    # ('Gift1', 50, 0),
    # ('Gift2', 25, 0),
    # ('Gift3', 35, 0),
    # ('Gift4', 45, 0),
    # ('Gift5', 55, 0),
    # ('Gift6', 65, 0),
    # ('Gift7', 65, 0),
    for i in range(len(top10[2])):
        rows.append((top10[2][i],top10[0][i],0))

    for row1 in rows:
        ws.append(row1)

    chart7 = BarChart()
    chart7.type = "col"
    chart7.style = 10
    #chart2.title = "AVERAGE PERFORMANCE PER ACT"

    data2 = Reference(ws, min_col=2, min_row=23, max_row=100, max_col=3)
    cats = Reference(ws, min_col=1, min_row=23, max_row=100)
    chart7.add_data(data2, titles_from_data=True)
    chart7.set_categories(cats)
    #chart1.shape = 4
    chart7.type = "col"
    chart7.style = 5
    chart7.grouping = "stacked"
    chart7.overlap = 100
    chart7.width = 500
    chart7.height = 100
    ws.add_chart(chart7, "A31")


    #wb.save("chart5.xlsx")
    wb.save(response) 
    return response

#export_chart()