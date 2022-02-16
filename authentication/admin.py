from django.contrib import admin
from .models import CustomUser
# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['roll_no', 'user', 'name', 'organization']
    list_filter = ['roll_no', 'organization']


admin.site.register(CustomUser, CustomUserAdmin)
