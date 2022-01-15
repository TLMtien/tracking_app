from django.contrib import admin
from django.db import models
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from . models import NewUser, HVN_vip, HVN, SalePerson
# Register your models here.

class UserAdminConfig(UserAdmin):
    model = NewUser
   
    list_display = ('id', 'user_name', 'is_active', 'is_staff', 'is_salePerson', 'is_HVN', 'is_HVNVip', 'is_region', 'is_agency')
    ordering = ('-start_date',)
    fieldsets = (
        (None, {'fields': ('user_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_salePerson', 'is_HVN', 'is_HVNVip', 'is_region', 'is_agency')}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_salePerson', 'is_HVN', 'is_HVNVip', 'is_region', 'is_agency')}
         ),
    )


admin.site.register(NewUser, UserAdminConfig)
admin.site.register(SalePerson),
admin.site.register(HVN),
admin.site.register(HVN_vip),


