from django import forms
from django.db.models import fields
from .models import outletInfo, tableReport, posmReport, giftReport, report_sale

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

class reportSaleForm(forms.ModelForm):
    beer_brand = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *"}))
    beer_HVN = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *"}))
    beer_other = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *"}))

    class Meta:
        model = report_sale
        fields = ("beer_brand", "beer_HVN", "beer_other")
    
    def __init__(self, *args, **kwargs):
        self.is_salePerson = kwargs.pop('is_salePerson',None)
        super(reportSaleForm, self).__init__(*args, **kwargs)

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
    other_beer_table = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Điền số lượng *", 'id':'input_quality'})) 
    brand_table = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Điền số lượng *", 'id':'input_quality'}))
    other_table = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Điền số lượng *", 'id':'input_quality'}))
    HVN_table = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Điền số lượng *", 'id':'input_quality'}))
    total_table = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Điền số lượng *", 'id':'input_quality'}))
    class Meta:
        model = tableReport
        fields = (
            "other_beer_table","other_table",
            "brand_table","HVN_table", "total_table",
        )

    def __init__(self, *args, **kwargs):
        self.is_salePerson = kwargs.pop('is_salePerson',None)
        super(tableReportForm, self).__init__(*args, **kwargs)


