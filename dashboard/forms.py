from django import forms
from .models import KPI
class TimeReportForm(forms.Form):
    from_date = forms.DateField(input_formats=["%d/%m/%Y", ])
    to_date = forms.DateField(input_formats=["%d/%m/%Y", ])

class TimeDashBoard(forms.Form):
    from_month =  forms.DateField(input_formats=["%m/", ])
    from_date = forms.DateField(input_formats=["%d/", ])

class KPIForm(forms.ModelForm):
    #start_day = forms.DateField(input_formats=["%d/%m/%Y", ])
    class Meta:
        model = KPI
        fields = ("volume_achieved", "table_share", 
                    "consumer_reached", "conversion",
                 )

class unlock_password(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'unlock-box', 'name': 'password',
													'placeholder':"Enter Your Password"}), required=True)
    class Meta:
        fields = ("password",
                 )
    