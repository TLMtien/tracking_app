import datetime, calendar
import json
from django.db.models import Q
from dateutil.relativedelta import relativedelta

def sum_value_iv(queryset):
    total_value = 0
    for iv in queryset:
        total_value += int(iv.value)
    return total_value

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

def date_generator(date_start, date_end):
    difference = relativedelta(date_end,date_start)
    months = difference.years*12 + difference.months

    date_iter = date_start
    for i in range(months):
        yield date_iter
        if date_start.month == 12:
            month = add_months(datetime.date(date_start.year + 1, 1, 28),i)
        else:
            month = add_months(datetime.date(date_start.year, date_start.month + 1, 28),i)
        # print(month)
        if month < date_end:
            # list_date.insert(-1,month)
            date_iter = month
    yield date_end

def revenue_char_bar(iv_isp, from_date, to_date):
    date_gen = date_generator(from_date, to_date)

    
    for d in date_gen:
        
        if d == from_date:     
            accrued_expenses_isp = sum_value_iv(iv_isp.filter(Q(date_upload__year=d.year), Q(date_upload__month=d.month), Q(date_upload__day__gte=d.day)))
        elif d == to_date:  
            accrued_expenses_isp = sum_value_iv(iv_isp.filter(Q(date_upload__year=d.year), Q(date_upload__month=d.month), Q(date_upload__day__lte=d.day)))
        else:
            accrued_expenses_isp = sum_value_iv(iv_isp.filter(Q(date_upload__year=d.year), Q(date_upload__month=d.month)))

    
        
    #return json.dumps(chart)