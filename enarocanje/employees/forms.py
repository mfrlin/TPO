from django.forms import ModelForm

from enarocanje.employees.models import Employee


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        exclude = ('employer', )

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
