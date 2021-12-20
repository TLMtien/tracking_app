from django.db import models
from django.conf import settings
from django.shortcuts import reverse
#from users.models import SalePerson
from django.utils.translation import gettext_lazy as _

# Create your models here.



TIGER_TP= 'tigerTP'
TIGER_FA= 'tigerFA'
TIGER_HZA= 'tigerHZA'
HEINEKEN ='heineken'
HEINEKEN_HNK = 'heineken_hnk'


CHOICES_COMPAIN = [
    (TIGER_TP, 'TAB_TGR'),
    (TIGER_FA, 'FES_TGR'),
    (TIGER_HZA, 'HOT_TGR'),
    (HEINEKEN,'TAB_HNK'),
    (HEINEKEN_HNK, 'SPE_HNK'),
    ('STB', 'FES_SBW'),
    ('bivina', 'TAB_BVN'),
    ('Larue', 'TAB_LRE'),
    ('Larue_SPE','SPE_LRE'),
]

def deduct(a,b):
    return str(int(a)-int(b))

def sum(a,b,c,d):
    return  str(int(a)+int(b)+int(c)+int(d))

def upload_to(instance, filename):
    return 'salePerson/{filename}'.format(filename=filename)

def report(instance, filename):
    return 'report/{filename}'.format(filename=filename)


class Campain(models.Model):
    program = models.CharField(choices=CHOICES_COMPAIN, max_length=200)
    
    def __str__(self):
        return self.program

class outletInfo(models.Model): 
    compain = models.ManyToManyField(Campain)
    province = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    outlet_address = models.CharField(max_length=255)
    outlet_Name = models.CharField(max_length=255)
    #slug = models.SlugField()
    ouletID = models.CharField(max_length=255, blank=True, null=True, default='00')
    created = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now=True)
    created_by_HVN = models.BooleanField(default=False, blank=True)
    def __str__(self):
        return "{} - {}".format(self.area, self.outlet_Name)
    class Meta:
	    ordering = ["created"]
    
    # def get_absolute_url(self):   
    #     return reverse("", kwargs={
    #         'slug':self.slug
    #     })
class posmReport(models.Model):
    SP = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    outlet = models.ForeignKey(outletInfo, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to)
    created = models.DateField(auto_now_add=True)
    campain = models.ForeignKey(Campain, on_delete=models.CASCADE)
    #modified = models.DateTimeField(auto_now=True)

class tableReport(models.Model):
    SP = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    outlet = models.ForeignKey(outletInfo, on_delete=models.CASCADE)
    other_table = models.CharField(max_length=255, default='0')
    other_beer_table = models.CharField(max_length=255, default='0')
    campain = models.ForeignKey(Campain, on_delete=models.CASCADE)
    brand_table = models.CharField(max_length=255, default='0')
    HVN_table = models.CharField(max_length=255, default='0')
    total_table = models.CharField(max_length=255, default='0', blank=True)
    created = models.DateField(auto_now_add=True)

    


class consumerApproachReport(models.Model):
    SP = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    outlet = models.ForeignKey(outletInfo, on_delete=models.CASCADE)
    consumers_approach = models.CharField(max_length=255)
    consumers_brough = models.CharField(max_length=255)
    Total_Consumers =  models.CharField(max_length=255)
    campain = models.ForeignKey(Campain, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    
class report_sale(models.Model):
    SP = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    outlet = models.ForeignKey(outletInfo, on_delete=models.CASCADE)
    beer_brand = models.CharField(max_length=255, default='0')
    beer_HVN = models.CharField(max_length=255, default='0')
    beer_other = models.CharField(max_length=255, default='0')
    created = models.DateField(auto_now_add=True)
    campain = models.ForeignKey(Campain, on_delete=models.CASCADE)

class giftReport(models.Model):
    SP = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    campain = models.ForeignKey(Campain, on_delete=models.CASCADE)

    outlet = models.ForeignKey(outletInfo, on_delete=models.CASCADE)
    gift1_received =  models.CharField(max_length=255, default='0')
    gift2_received =  models.CharField(max_length=255, default='0')
    gift3_received =  models.CharField(max_length=255, default='0', blank=True)
    gift4_received =  models.CharField(max_length=255, default='0', blank=True, null=True)
    gift5_received =  models.CharField(max_length=255, default='0', blank=True, null=True)
    gift6_received =  models.CharField(max_length=255, default='0', blank=True, null=True)
    gift7_received =  models.CharField(max_length=255, default='0', blank=True, null=True)
    gift8_received =  models.CharField(max_length=255, default='0', blank=True, null=True)
    gift9_received =  models.CharField(max_length=255, default='0', blank=True, null=True)
    gift10_received =  models.CharField(max_length=255, default='0', blank=True, null=True)
    

    gift1_given = models.CharField(max_length=255, default='0', blank=True, null=True)
    gift2_given = models.CharField(max_length=255, default='0', blank=True, null=True)
    gift3_given = models.CharField(max_length=255, default='0', blank=True, null=True)
    gift4_given = models.CharField(max_length=255, default='0', blank=True, null=True)
    gift5_given = models.CharField(max_length=255, default='0', blank=True, null=True)
    gift6_given = models.CharField(max_length=255, default='0', blank=True, null=True)
    gift7_given = models.CharField(max_length=255, default='0', blank=True, null=True)
    gift8_given = models.CharField(max_length=255, default='0', blank=True, null=True)
    gift9_given = models.CharField(max_length=255, default='0', blank=True, null=True)
    gift10_given = models.CharField(max_length=255, default='0', blank=True, null=True)
    

    gift1_remaining = models.CharField(max_length=50, null=True, blank=True, default='0')
    gift2_remaining = models.CharField(max_length=50, null=True, blank=True, default='0')
    gift3_remaining = models.CharField(max_length=50, null=True, blank=True, default='0')
    gift4_remaining = models.CharField(max_length=50, null=True, blank=True, default='0')
    gift5_remaining = models.CharField(max_length=50, null=True, blank=True, default='0')
    gift6_remaining = models.CharField(max_length=50, null=True, blank=True, default='0')
    gift7_remaining = models.CharField(max_length=50, null=True, blank=True, default='0')
    gift8_remaining = models.CharField(max_length=50, null=True, blank=True, default='0')
    gift9_remaining = models.CharField(max_length=50, null=True, blank=True, default='0')
    gift10_remaining = models.CharField(max_length=50, null=True, blank=True, default='0')
    
    created = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.gift1_remaining = deduct(self.gift1_received , self.gift1_given)
        self.gift2_remaining = deduct(self.gift2_received , self.gift2_given)
        self.gift3_remaining = deduct(self.gift3_received , self.gift3_given)
        self.gift4_remaining = deduct(self.gift4_received , self.gift4_given)
        self.gift5_remaining = deduct(self.gift5_received , self.gift5_given)
        self.gift6_remaining = deduct(self.gift6_received , self.gift6_given)
        self.gift7_remaining = deduct(self.gift7_received , self.gift7_given)
        self.gift8_remaining = deduct(self.gift8_received , self.gift8_given)
        self.gift9_remaining = deduct(self.gift9_received , self.gift9_given)
        self.gift10_remaining = deduct(self.gift10_received , self.gift10_given)
        super(giftReport, self).save(*args, **kwargs)
    
    def __str__(self):
        return "{} - {} - {}- {}- {}- {}".format(self.gift1_remaining, self.gift2_remaining, 
            self.gift3_remaining, self.gift4_remaining, self.gift5_remaining, self.gift6_remaining)


class overallReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    outlet = models.ForeignKey(outletInfo, on_delete=models.CASCADE)
    posm_Report = models.ForeignKey(posmReport, on_delete=models.CASCADE)
    table_Report = models.ForeignKey(tableReport, on_delete=models.CASCADE)
    gift_report = models.ForeignKey(giftReport, on_delete=models.CASCADE)
    consumer_report = models.ForeignKey(consumerApproachReport, on_delete=models.CASCADE)
    campain = models.ForeignKey(Campain, on_delete=models.CASCADE)
    confirm = models.ImageField(upload_to=report)  
    created = models.DateField(auto_now_add=True)



class search(models.Model):
    province =  models.CharField(max_length=255)
    district =  models.CharField(max_length=255)