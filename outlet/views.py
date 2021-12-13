from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import overallReport, tableReport, outletInfo, giftReport, search, posmReport, Campain
from .forms import outletInfoForm
from django.views.generic import DetailView, ListView, detail
from users.models import SalePerson


from django.http import JsonResponse
# Create your views here.
def index(request):
    return HttpResponse('ok')

login_required
def ListReport(request):
        rp = overallReport.objects.all().count()
        rpview = overallReport.objects.all()
      

        return render(request, 'outlet/index.html',{'tasks': rpview})

login_required
def outlet_create(request):
    if request.method == "POST":
        SP =SalePerson.objects.get(user=request.user)
        form = outletInfoForm(request.POST,is_salePerson=request.user.is_salePerson)
        if form.is_valid():
            outlet_Name = form.cleaned_data.get('outlet_Name')
            type = form.cleaned_data.get('type')
            outlet_address = form.cleaned_data.get('outlet_address')
            
            #create outlet
            p, created = outletInfo.objects.get_or_create(outlet_Name=outlet_Name, type=type,  outlet_address=outlet_address)
            #CP = Campain.objects.get(program=SP.brand)
            p.compain.add(SP.brand)
            p.save()

            SP.outlet = p
            SP.save()

            return redirect('successcreate')
    else:
        form = outletInfoForm()
        return render(request,"outlet/createinfooutlet.html",{'form':form})
    


# login_required
# class ListOutletView(ListView):
#     model = outletInfo
#     context_object_name = 'list_outlet'
#     #paginate_by = 2
#     template_name = 'outlet/homeoutlet.html'
login_required
def ListOutletView(request):
    user = request.user
    SP = SalePerson.objects.get(user=user)
    compain = SP.brand
    Listoutlet = outletInfo.objects.filter(compain=compain)
    return render(request, 'outlet/homeoutlet.html', {'list_outlet':Listoutlet})

login_required
class OutletDetailView(DetailView):
    model = outletInfo
    template_name = 'outlet/outletdetails.html'
 


login_required
def searchView(request):
    if request.is_ajax():
        province = request.POST.get('province')
        district = request.POST.get('district')
        search.objects.create(province=province, district=district)
        redirect('create')
        return JsonResponse({'created': True})
    return JsonResponse({'created': False})


