from django.contrib import admin
from .models import outletInfo, giftInform, reportData, saleInform, posmInform
# Register your models here.

admin.site.register(giftInform),
admin.site.register(reportData),
admin.site.register(saleInform),
admin.site.register(posmInform),
admin.site.register(outletInfo),
