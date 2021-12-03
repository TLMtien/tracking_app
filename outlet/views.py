from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import reportData
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
    if request.user.is_salePerson:
        if request.method == "POST":
            form = outletInfoForm(request.POST,hnk_staff=request.user.is_salePerson)
            if form.is_valid():
                return render(request,"users/login.html",{'form':form})
        else:
            form = outletInfoForm()
            return render(request,"users/login.html",{'form':form})
   