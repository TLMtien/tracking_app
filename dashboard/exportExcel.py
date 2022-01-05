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

from openpyxl.chart.series import DataPoint
from openpyxl.writer.excel import save_virtual_workbook

def export_chart():
   
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment;filename={}.xlsx'.format(str(datetime.now()))
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()

    w = wb.active

    ##activation

    ## Volume
    rows = [
        ('Title', 'Average Brand Volume', 'Average Target Volume'),
        ('Average Brand Volume', 150, 0),
        ('Average Target Volume', 2500, 0),
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
        ['HVN', 50],
        ['Brand', 30],
        ['Other', 10],
        ['Other beer', 40],
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
        ('Total Acts', 2500, 0),
        ('Actual Acts', 150, 0),
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
    rows = [
        ('Title', ),
        ('Gift1', 50, 0),
        ('Gift2', 25, 0),
        ('Gift3', 35, 0),
        ('Gift4', 45, 0),
        ('Gift5', 55, 0),
        ('Gift6', 65, 0),
        ('Gift7', 65, 0),
    ]

    for row1 in rows:
        ws.append(row1)

    chart2 = BarChart()
    chart2.type = "col"
    chart2.style = 10
    #chart2.title = "AVERAGE PERFORMANCE PER ACT"

    data2 = Reference(ws, min_col=2, min_row=12, max_row=20, max_col=3)
    cats = Reference(ws, min_col=1, min_row=13, max_row=20)
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
        ('Target Volume', 180, 0),
        ('ActualVolume', 170, 0),
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

    #wb.save("chart5.xlsx")
    wb.save(response) 
    return response

export_chart()