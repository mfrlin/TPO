from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from enarocanje.employees.models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'phone', 'employer')


admin.site.register(Employee, EmployeeAdmin)
