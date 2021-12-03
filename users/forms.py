from django import forms
from django.contrib.auth.forms import  UserCreationForm 
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
    

class ChangePasswordForm(forms.ModelForm):
	id = forms.CharField(widget=forms.HiddenInput())
	old_password = forms.CharField(widget=forms.PasswordInput(), label="Old password", required=True)
	new_password = forms.CharField(widget=forms.PasswordInput(), label="New password", required=True)
	confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm new password", required=True)

	class Meta:
		model = NewUser
		fields = ('id', 'old_password', 'new_password', 'confirm_password')

	def clean(self):
		super(ChangePasswordForm, self).clean()
		id = self.cleaned_data.get('id')
		old_password = self.cleaned_data.get('old_password')
		new_password = self.cleaned_data.get('new_password')
		confirm_password = self.cleaned_data.get('confirm_password')
		user = NewUser.objects.get(pk=id)
		if not user.check_password(old_password):
			self._errors['old_password'] =self.error_class(['Old password do not match.'])
		if new_password != confirm_password:
			self._errors['new_password'] =self.error_class(['Passwords do not match.'])
		return self.cleaned_data