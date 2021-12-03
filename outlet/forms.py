from django import forms
from django.db.models import fields
from .models import outletInfo, saleInform, posmInform, giftInform

class outletInfoForm(forms.ModelForm):
    class Meta:
        model = outletInfo
        fields = ("province","outletID","type","area", "outlet_address", "outlet_Name")

    def __init__(self, *args, **kwargs):
        self.is_salePerson = kwargs.pop('is_salePerson',None)
        super(outletInfoForm, self).__init__(*args, **kwargs)

class giftInformForm(forms.ModelForm):
    class Meta:
        model = giftInform
        fields = ("gift1_received", "gift2_received", "gift3_received", "gift1_given", "gift2_given", "gift3_given")
    def __init__(self, *args, **kwargs):
        self.is_salePerson = kwargs.pop('is_salePerson',None)
        super(giftInformForm, self).__init__(*args, **kwargs)

class saleInformForm(forms.ModelForm):
    class Meta:
        model = saleInform
        fields = ("brand_volume_sales","brand_table","other_HVS_table","total_table", "consumers_approach", "consumers_brough", "Total_Consumers")

    def __init__(self, *args, **kwargs):
        self.is_salePerson = kwargs.pop('is_salePerson',None)
        super(saleInformForm, self).__init__(*args, **kwargs)


