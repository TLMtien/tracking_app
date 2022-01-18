from django import forms
from django.contrib.auth.forms import  UserCreationForm 
from django.contrib.auth.forms import PasswordChangeForm
from .models import NewUser, SalePerson
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

def ForbiddenUsers(value):
	forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
	'email', 'user', 'join', 'sql', 'static', 'python', 'delete']
	if value.lower() in forbidden_users:
		raise ValidationError('Invalid name for user, this is a reserverd word.')

def InvalidUser(value):
	if '@' in value or '+' in value or '-' in value:
		raise ValidationError('This is an Invalid user, Do not user these chars: @ , - , + ')

def UniqueUser(value):
	if NewUser.objects.filter(user_name__iexact=value).exists():
		raise ValidationError('User with this username already exists.')

class SignupForm(forms.ModelForm):
	user_name = forms.CharField(widget=forms.TextInput(), max_length=30, required=True,)
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput(), required=True, label="Confirm your password.")

	class Meta:

		model = NewUser
		fields = ('user_name', 'password1')

	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.fields['user_name'].validators.append(ForbiddenUsers)
		self.fields['user_name'].validators.append(InvalidUser)
		self.fields['user_name'].validators.append(UniqueUser)
		

	def clean(self):
		super(SignupForm, self).clean()
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 != password2:
			self._errors['password1'] = self.error_class(['Passwords do not match. Try again'])
		return self.cleaned_data
    
#######
    
class LoginForm(forms.Form):
	username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'input-user', 'placeholder':"Tên đăng nhập", 'style':'font-size: 16px'}))
    
	password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'class': 'input-password', 'placeholder':"Mật Khẩu", 'id':"password-field", 'name':"password", 'style':'font-size: 16px'}))

#---------------------------------------------
class LoginHVNForm(forms.Form):
	username = forms.CharField(max_length=200, widget=forms.EmailInput(attrs={'class': 'input-user', 'placeholder':"example@example.com"}))
    
	password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'class': 'input-password', 'id': 'password-field', 'placeholder':"enter your password"}))

#--------------------------------------------
class ChangePasswordForm(forms.Form):
	    
	new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-user', 
													'placeholder':"Mật khẩu mới"}), required=True)
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-password', 
														'placeholder':"Nhập Lại Mật Khẩu"}), required=True)

	def clean(self):
		new_password=self.cleaned_data.get('new_password')
		confirm_password=self.cleaned_data.get('confirm_password')
		#similarly old_password
		if new_password and new_password!=confirm_password :
			self._errors['new_password'] =self.error_class(['Passwords do not match.'])
		return self.cleaned_data 

class ChangePasswordHVNForm(forms.Form):
	    
	new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-password new-pass', 'id': 'password-field',
													'placeholder':"Mật khẩu mới"}), required=True)
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-password', 'id': 'password-change',
														'placeholder':"Nhập Lại Mật Khẩu"}), required=True)

	def clean(self):
		new_password=self.cleaned_data.get('new_password')
		confirm_password=self.cleaned_data.get('confirm_password')
		#similarly old_password
		if new_password and new_password!=confirm_password :
			self._errors['new_password'] =self.error_class(['Passwords do not match.'])
		return self.cleaned_data 
