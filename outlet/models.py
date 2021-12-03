from django.db import models
from django.conf import settings

# Create your models here.
def deduct(a,b):
    return str(int(a)-int(b))

def upload_to(instance, filename):
    return 'salePerson/{filename}'.format(filename=filename)

def report(instance, filename):
    return 'report/{filename}'.format(filename=filename)

class outletInfo(models.Model): 
    date = models.DateField(auto_now_add=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    outletID = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    outlet_address = models.CharField(max_length=255)
    outlet_Name = models.CharField(max_length=255)

    def __str__(self):
        return "{} - {}".format(self.area, self.outletID)

class posmInform(models.Model):
    image = models.ImageField(upload_to=upload_to)

class saleInform(models.Model):
    brand_volume_sales = models.IntegerField(default=0)
    brand_table =  models.IntegerField(default=0)
    other_HVS_table = models.IntegerField(default=0)
    total_table = models.IntegerField(default=0)
    consumers_approach = models.CharField(max_length=255)
    consumers_brough = models.CharField(max_length=255)
    Total_Consumers =  models.CharField(max_length=255)
    

class giftInform(models.Model):
    gift1_received =  models.IntegerField(default=0)
    gift2_received =  models.IntegerField(default=0)
    gift3_received =  models.IntegerField(default=0)

    gift1_given = models.IntegerField(default=0)
    gift2_given = models.IntegerField(default=0)
    gift3_given = models.IntegerField(default=0)

    total_survive_gift1 = models.CharField(max_length=50, null=True, blank=True)
    total_survive_gift2 = models.CharField(max_length=50, null=True, blank=True)
    total_survive_gift3 = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_survive_gift1 = deduct(self.gift1_received , self.gift1_given)
        self.total_survive_gift2 = deduct(self.gift2_received , self.gift2_given)
        self.total_survive_gift3 = deduct(self.gift3_received , self.gift3_given)
        super(giftInform, self).save(*args, **kwargs)
    
    def __str__(self):
         return "gift1{} - gift2{} - gift3{}".format(self.total_survive_gift1, self.total_survive_gift2, self.total_survive_gift3)


class reportData(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posmReport = models.ForeignKey(posmInform, on_delete=models.CASCADE)
    saleReport = models.ForeignKey(saleInform, on_delete=models.CASCADE)
    gift = models.ForeignKey(giftInform, on_delete=models.ForeignKey)
    confirm = models.ImageField(upload_to=report)  #checkout



    
