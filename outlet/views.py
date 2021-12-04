from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import reportData, outletInfo
from .forms import outletInfoForm, saleInformForm, giftInform
# Create your views here.
def index(request):
    return HttpResponse('ok')

login_required
def ListReport(request):
        rp = reportData.objects.all().count()
        rpview = reportData.objects.all()
      

        return render(request, 'outlet/index.html',{'tasks': rpview})

def outlet_create(request):
    SP = request.user
    if request.user.is_salePerson:
        if request.method == "POST":
            form = outletInfoForm(request.POST,is_salePerson=request.user.is_salePerson)
            if form.is_valid():
                outlet_Name = form.cleaned_data.get('outlet_Name')
                province  = form.cleaned_data.get('province')
                outletID = form.cleaned_data.get('outletID')
                type = form.cleaned_data.get('type')
                area = form.cleaned_data.get('area')
                outlet_address = form.cleaned_data.get('outlet_address')

                p, created = outletInfo.objects.get_or_create(outlet_Name=outlet_Name, province =province, SP=SP, outletID=outletID, type=type, area=area, outlet_address=outlet_address)
                p.save()
                reportData.objects
                return render(request,"users/login.html",{'form':form})
        else:
            form = outletInfoForm()
            return render(request,"users/login.html",{'form':form})
    return HttpResponse('faulty')

def saleINFO_create(request):

   pass