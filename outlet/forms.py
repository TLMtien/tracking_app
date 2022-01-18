from django import forms
from django.db.models import fields
from .models import outletInfo, tableReport, posmReport, giftReport, report_sale, consumerApproachReport, search

class outletInfoForm(forms.ModelForm):
    outlet_Name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Tên outlet *", 'style':'font-size: 16px'}))
    #type = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Loại outlet *"}))
    outlet_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Địa chỉ outlet *", 'style':'font-size: 16px'}))
    ouletID = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"ID outlet *", 'style':'font-size: 16px'}), required=False)

    class Meta:
        model = outletInfo
        fields = ("outlet_address", 
                    "outlet_Name", "ouletID",
                 )

    def __init__(self, *args, **kwargs):
        self.is_salePerson = kwargs.pop('is_salePerson',None)
        super(outletInfoForm, self).__init__(*args, **kwargs)

class reportSaleForm(forms.ModelForm):
    beer_brand = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *", 'pattern':'[0-9]*', 'style':'font-size: 16px'}))
    beer_HVN = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *", 'pattern':'[0-9]*', 'style':'font-size: 16px'}))
    beer_other = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *", 'pattern':'[0-9]*', 'style':'font-size: 16px'}))

    class Meta:
        model = report_sale
        fields = ("beer_brand", "beer_HVN", "beer_other")
    
    def __init__(self, *args, **kwargs):
        self.is_salePerson = kwargs.pop('is_salePerson',None)
        super(reportSaleForm, self).__init__(*args, **kwargs)

class gift_ReceiveReportForm(forms.ModelForm):
    gift1_received = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *", 'pattern':'[0-9]*', 'style':'font-size: 16px'}))
    gift2_received = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *", 'pattern':'[0-9]*', 'style':'font-size: 16px'}))
    gift3_received = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *", 'pattern':'[0-9]*', 'style':'font-size: 16px'}))
    gift4_received = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *", 'pattern':'[0-9]*', 'style':'font-size: 16px'}))
    gift5_received = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *", 'pattern':'[0-9]*', 'style':'font-size: 16px'}), required=False)
    gift6_received = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *", 'pattern':'[0-9]*', 'style':'font-size: 16px'}), required=False)
    gift7_received = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *", 'pattern':'[0-9]*', 'style':'font-size: 16px'}), required=False)
    class Meta:
        model = giftReport
        fields = ("gift1_received", "gift2_received", 
                    "gift3_received", "gift4_received", "gift5_received", "gift6_received",
                 )
    def __init__(self, *args, **kwargs):
        self.is_salePerson = kwargs.pop('is_salePerson',None)
        super(gift_ReceiveReportForm, self).__init__(*args, **kwargs)

class gift_givenReportForm(forms.ModelForm):
    gift1_given = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *", 'pattern':'[0-9]*', 'style':'font-size: 16px'}))
    gift2_given = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *", 'pattern':'[0-9]*', 'style':'font-size: 16px'}))
    gift3_given = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *", 'pattern':'[0-9]*', 'style':'font-size: 16px'}))
    gift4_given = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *", 'pattern':'[0-9]*', 'style':'font-size: 16px'}))
    gift5_given = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *", 'pattern':'[0-9]*', 'style':'font-size: 16px'}), required=False)
    gift6_given = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *", 'pattern':'[0-9]*', 'style':'font-size: 16px'}), required=False)
    gift7_given = forms.CharField(widget=forms.TextInput(attrs={'id' :'input_quality','placeholder':"Điền số lượng *", 'pattern':'[0-9]*', 'style':'font-size: 16px'}), required=False)
    class Meta:
        model = giftReport
        fields = ("gift1_given", "gift2_given", 
                    "gift3_given", "gift4_given", "gift5_given", "gift6_given",
                 )
    def __init__(self, *args, **kwargs):
        self.is_salePerson = kwargs.pop('is_salePerson',None)
        super(gift_givenReportForm, self).__init__(*args, **kwargs)


class tableReportForm(forms.ModelForm):
    other_beer_table = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Điền số lượng *", 'id':'input_quality', 'pattern':'[0-9]*', 'style':'font-size: 16px'})) 
    brand_table = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Điền số lượng *", 'id':'input_quality', 'pattern':'[0-9]*', 'style':'font-size: 16px'}))
    other_table = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Điền số lượng *", 'id':'input_quality', 'pattern':'[0-9]*', 'style':'font-size: 16px'}))
    HVN_table = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Điền số lượng *", 'id':'input_quality', 'pattern':'[0-9]*', 'style':'font-size: 16px'}))
    
    class Meta:
        model = tableReport
        fields = (
            "other_beer_table","other_table",
            "brand_table","HVN_table", 
        )

    def __init__(self, *args, **kwargs):
        self.is_salePerson = kwargs.pop('is_salePerson',None)
        super(tableReportForm, self).__init__(*args, **kwargs)

class consumerApproachReportForm(forms.ModelForm):
    consumers_approach = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Điền số lượng *", 'id':'input_quality', 'pattern':'[0-9]*', 'style':'font-size: 16px'})) 
    consumers_brough = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Điền số lượng *", 'id':'input_quality', 'pattern':'[0-9]*', 'style':'font-size: 16px'}))
    Total_Consumers = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Điền số lượng *", 'id':'input_quality', 'pattern':'[0-9]*', 'style':'font-size: 16px'}))
   
    class Meta:
        model = tableReport
        fields = (
            "consumers_approach","consumers_brough",
            "Total_Consumers",
        )

    def __init__(self, *args, **kwargs):
        self.is_salePerson = kwargs.pop('is_salePerson',None)
        super(consumerApproachReportForm, self).__init__(*args, **kwargs)


class searchForm(forms.ModelForm):
    province = forms.CharField(widget=forms.TextInput(attrs={'class':"billing_address_1", 'name':'', 'value':'', 'style':'font-size: 16px'})) 
    district = forms.CharField(widget=forms.TextInput(attrs={'class':"billing_address_2", 'name':'', 'value':'', 'style':'font-size: 16px'})) 
    
    class Meta:
        model = search
        fields = ("province", "district")