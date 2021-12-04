from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from . forms import ChangePasswordForm, SignupForm
from . models import NewUser, SalePerson
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView
import openpyxl
from django.urls import reverse_lazy
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
			return redirect('index')
	else:
		form = ChangePasswordForm(instance=user)

	context = {
		'form':form,
	}

	return render(request, 'index', context)


class LoginView(LoginView):
    template_name = 'users/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('page')

login_required
def page_user(request):
	if request.user.is_HVN or request.user.is_HVNVip:
		return HttpResponse('ok')
	
	return HttpResponse('ko')