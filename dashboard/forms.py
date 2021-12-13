from django import forms

class TimeReportForm(forms.Form):
    from_date = forms.DateField(input_formats=["%d/%m/%Y", ])
    to_date = forms.DateField(input_formats=["%d/%m/%Y", ])

class TimeDashBoard(forms.Form):
    from_month =  forms.DateField(input_formats=["%m/", ])
    from_date = forms.DateField(input_formats=["%d/", ])