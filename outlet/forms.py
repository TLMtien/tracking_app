from django import forms
from django.db.models import fields
from .models import outletInfo, tableReport, posmReport, giftReport

class outletInfoForm(forms.ModelForm):
    outlet_Name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Tên outlet *"}))
    type = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Loại outlet *"}))
    outlet_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Địa chỉ outlet *"}))

    class Meta:
        model = outletInfo
        fields = ("type", "outlet_address", 
                    "outlet_Name",
                 )

    def __init__(self, *args, **kwargs):
        self.is_salePerson = kwargs.pop('is_salePerson',None)
        super(outletInfoForm, self).__init__(*args, **kwargs)

class giftReportForm(forms.ModelForm):
    class Meta:
        model = giftReport
        fields = ("gift1_received", "gift2_received", "gift3_received", 
                  "gift4_received", "gift5_received", "gift1_given", 
                  "gift2_given", "gift3_given", "gift4_given" , 
                  "gift5_given",
                  )
    def __init__(self, *args, **kwargs):
        self.is_salePerson = kwargs.pop('is_salePerson',None)
        super(giftReportForm, self).__init__(*args, **kwargs)

class tableReportForm(forms.ModelForm):
    class Meta:
        model = tableReport
        fields = (
            "other_table","other_beer_table",
            "brand_table","HVN_table",
            "total_table"
        )

    def __init__(self, *args, **kwargs):
        self.is_salePerson = kwargs.pop('is_salePerson',None)
        super(tableReportForm, self).__init__(*args, **kwargs)


