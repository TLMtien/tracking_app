from django.db.models import query
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import overallReport, tableReport, outletInfo, giftReport
from .forms import outletInfoForm, giftReportForm, tableReportForm
from django.views.generic import DetailView, ListView, detail
# Create your views here.
def index(request):
    return HttpResponse('ok')

login_required
def ListReport(request):
        rp = overallReport.objects.all().count()
        rpview = overallReport.objects.all()
      

        return render(request, 'outlet/index.html',{'tasks': rpview})

def outlet_create(request):
    if request.method == "POST":
        form = outletInfoForm(request.POST,is_salePerson=request.user.is_salePerson)
        if form.is_valid():
            outlet_Name = form.cleaned_data.get('outlet_Name')
            type = form.cleaned_data.get('type')
            outlet_address = form.cleaned_data.get('outlet_address')

            p, created = outletInfo.objects.get_or_create(outlet_Name=outlet_Name, type=type,  outlet_address=outlet_address)
            p.save()
            return redirect('successcreate')
    else:
        form = outletInfoForm()
        return render(request,"outlet/createinfooutlet.html",{'form':form})
    

# def gift_report_create(request):
#     SP = request.user
#     if request.user.is_salePerson:
#         if request.method == "POST":
#             outlet = outletInfo.objects.filter(SP=request.user).last()
#             form = giftReportForm(request.POST,is_salePerson=request.user.is_salePerson)
#             if form.is_valid():
#                 gift1_received = form.cleaned_data.get('gift1_received')
#                 gift2_received = form.cleaned_data.get('gift2_received')
#                 gift3_received = form.cleaned_data.get('gift3_received')
#                 gift4_received = form.cleaned_data.get('gift4_received')
#                 gift5_received = form.cleaned_data.get('gift5_received')

#                 gift1_given = form.cleaned_data.get('gift1_given')
#                 gift2_given = form.cleaned_data.get('gift2_given')
#                 gift3_given = form.cleaned_data.get('gift3_given')
#                 gift4_given = form.cleaned_data.get('gift4_given')
#                 gift5_given = form.cleaned_data.get('gift5_given')
                
#                 p, created = giftReport.objects.get_or_create(outlet=outlet, SP=SP, gift1_received=gift1_received,
#                                                             gift2_received=gift2_received, gift3_received=gift3_received,
#                                                             gift4_received=gift4_received, gift5_received=gift5_received,
#                                                             gift1_given=gift1_given, gift2_given=gift2_given, 
#                                                             gift3_given=gift3_given, gift4_given=gift4_given, gift5_given=gift5_given,
#                                                             )
#                 p.save()
#                 return render(request,"users/login.html",{'form':form})
#         else:
#             form = giftReportForm()
#             return render(request,"users/login.html",{'form':form})
#     return HttpResponse('')

# def table_report_create(request):
#     SP = request.user
#     if request.user.is_salePerson:
#         if request.method == "POST":
#             outlet = outletInfo.objects.filter(SP=request.user).last()
#             form = tableReportForm(request.POST,is_salePerson=request.user.is_salePerson)
#             if form.is_valid():
#                 total_table = form.cleaned_data.get('total_table')
#                 brand_table = form.cleaned_data.get('brand_table')
#                 other_beer_table = form.cleaned_data.get('other_beer_table')
#                 HVN_table = form.cleaned_data.get('HVN_table')
#                 other_table = form.cleaned_data.get('other_table')
#                 p, created = tableReport.objects.get_or_create( total_table=total_table, brand_table=brand_table,
#                                                                other_beer_table=other_beer_table, HVN_table=HVN_table,
#                                                                other_table=other_table, SP=SP, outlet=outlet,
#                                                              )
#                 p.save()
#         else:
#             form = tableReportForm()
#             return render(request,"users/login.html",{'form':form})
#     return HttpResponse('')


# def search_outlet(request):
#     query = request.GET.get("query")
#     outlet = outletInfo.objects.filter(province=query)

#     return render(request)

login_required
class ListOutletView(ListView):
    model = outletInfo
    context_object_name = 'list_outlet'
    #paginate_by = 2
    template_name = 'outlet/homeoutlet.html'

login_required
class OutletDetailView(DetailView):
    model = outletInfo
    template_name = 'outlet/outletdetails.html'

