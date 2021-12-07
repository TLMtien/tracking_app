from django.contrib import admin
from .models import outletInfo, giftReport, overallReport, tableReport, posmReport, consumerApproachReport,  Campain, report_sale
# Register your models here.

admin.site.register(giftReport),
admin.site.register(overallReport),
admin.site.register(tableReport),
admin.site.register(posmReport),
admin.site.register(outletInfo),
admin.site.register(consumerApproachReport),
admin.site.register(Campain),
admin.site.register(report_sale),