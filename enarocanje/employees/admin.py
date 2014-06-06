from django.contrib import admin

from enarocanje.employees.models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'phone', 'employer')


admin.site.register(Employee, EmployeeAdmin)
