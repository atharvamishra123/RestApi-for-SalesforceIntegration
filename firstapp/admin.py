from django.contrib import admin
from firstapp.models import UserData


# Register your models here.
@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name', 'EmployeeNumber', 'Department', 'Email', 'City']
