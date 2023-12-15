from django.contrib import admin
from .models import *


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["dep_name"]


@admin.register(Profession)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ["user", "fullname", "department", "profession"]