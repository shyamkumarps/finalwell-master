from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.


model_list=[Account,project,CustomGroup,project_detail]
admin.site.register(model_list)



# class AccountAdmin(UserAdmin):
#     model=Account
#     list_display = ('email')
#     list_filter = ('email')
#     fieldsets = (
#         (None, {
#             "fields": (
#                 'email','username','date_joined','Company_Name','Company_ID','Number_of_Users','License_Start_Date','License_End_Date'
#             )
#         }),
#         ('Permissions',{'fields':('groups','user_permissions')})
#     )





