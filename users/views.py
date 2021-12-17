from django.http import response
from django.http.response import Http404, HttpResponse
from django.shortcuts import render, redirect
from . forms import ChangePasswordForm, SignupForm, LoginForm, LoginHVNForm
from . models import NewUser, SalePerson
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView
import openpyxl
from outlet.models import outletInfo
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .decorators import unauthenticated_user, unauthenticated_user_HVN
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.

def index(request):
    return HttpResponse('ok')
	
#import excel data ----> create account for SP 

def Signup(request):
	excel_file = request.FILES["excel_file"]
	wb = openpyxl.load_workbook(excel_file)

	sheets = wb.sheetnames
	worksheet = wb[sheets[0]]  
	excel_data = list()	
	for row in worksheet.iter_rows():
		row_data = list()
		for cell in row:
			row_data.append(str(cell.value))
		excel_data.append(row_data)
    #loop 
	user = NewUser.objects.create_user(user_name='user_name', password1='password1')
	sp=SalePerson.objects.create(user=user, brand = '', full_name = '', province='', outlet='')
	sp.save()
	return redirect('index')
	


login_required
def PasswordChange(request):
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('PasswordChangeDone')
	else:
		form = ChangePasswordForm()

		context = {
			'form':form,
		}

		return render(request, 'users/changepass.html', context)



@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('page')
        else:
            messages.info(request, "usename or password is incorrect")
            return redirect('loginPage')
    form = LoginForm()
    return render(request, 'users/login.html', {'form':form})

@unauthenticated_user_HVN
def loginHVN(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboardforlogin")
        else:
            messages.info(request, "usename or password is incorrect")
            return redirect('loginHVN')
    form = LoginHVNForm()
    return render(request, 'users/loginHVN.html', {'form':form})

login_required
def page_user(request):
	if request.user.is_salePerson:
		return redirect('listoutlet')
	if request.user.is_HVN:
		return redirect('dashboardforlogin')
	return  Http404
	
	
login_required
def PasswordChangeDone(request):
	return render(request, 'users/successpass.html') 