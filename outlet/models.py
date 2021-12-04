from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# Create your models here.
def deduct(a,b):
    return str(int(a)-int(b))

def upload_to(instance, filename):
    return 'salePerson/{filename}'.format(filename=filename)

def report(instance, filename):
    return 'report/{filename}'.format(filename=filename)

class outletInfo(models.Model): 
    SP = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    outletID = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    outlet_address = models.CharField(max_length=255)
    outlet_Name = models.CharField(max_length=255)

    def __str__(self):
        return "{} - {}".format(self.area, self.outletID)

class posmReport(models.Model):
    SP = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to)

class tableReport(models.Model):
    SP = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    other_table = models.IntegerField(default=0)
    other_beer_table = models.IntegerField(default=0)
    brand_table =  models.IntegerField(default=0)
    HVN_table = models.IntegerField(default=0)
    total_table = models.IntegerField(default=0)

class consumerApproachReport(models.Model):
    SP = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    consumers_approach = models.CharField(max_length=255)
    consumers_brough = models.CharField(max_length=255)
    Total_Consumers =  models.CharField(max_length=255)
    

class giftReport(models.Model):
    SP = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gift1_received =  models.IntegerField(default=0)
    gift2_received =  models.IntegerField(default=0)
    gift3_received =  models.IntegerField(default=0)
    gift4_received =  models.IntegerField(default=0)
    gift5_received =  models.IntegerField(default=0)

    gift1_given = models.IntegerField(default=0)
    gift2_given = models.IntegerField(default=0)
    gift3_given = models.IntegerField(default=0)
    gift4_given = models.IntegerField(default=0)
    gift5_given = models.IntegerField(default=0)

    gift1_remaining = models.CharField(max_length=50, null=True, blank=True)
    gift2_remaining = models.CharField(max_length=50, null=True, blank=True)
    gift3_remaining = models.CharField(max_length=50, null=True, blank=True)
    gift4_remaining = models.CharField(max_length=50, null=True, blank=True)
    gift5_remaining = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.gift1_remaining = deduct(self.gift1_received , self.gift1_given)
        self.gift2_remaining = deduct(self.gift2_received , self.gift2_given)
        self.gift3_remaining = deduct(self.gift3_received , self.gift3_given)
        self.gift4_remaining = deduct(self.gift4_received , self.gift4_given)
        self.gift5_remaining = deduct(self.gift5_received , self.gift5_given)
        super(giftReport, self).save(*args, **kwargs)
    
    def __str__(self):
        return "gift1{} - gift2{} - gift3{} - gift4{} - gift{}".format(self.gift1_remaining, self.gift2_remaining, self.gift3_remaining, self.gift4_remaining, self.gift5_remaining)


class overallReport(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posmReport = models.ForeignKey(posmReport, on_delete=models.CASCADE)
    saleReport = models.ForeignKey(tableReport, on_delete=models.CASCADE)
    gift = models.ForeignKey(giftReport, on_delete=models.ForeignKey)
    confirm = models.ImageField(upload_to=report)  



    