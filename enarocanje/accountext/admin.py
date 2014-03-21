from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.translation import ugettext_lazy as _

from forms import UserChangeForm
from models import User, ServiceProvider, Category

class UserAdmin(DefaultUserAdmin):
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		(_('Personal info'), {'fields': ('email', 'first_name', 'last_name', 'phone')}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
	)
	list_display = ('email', 'first_name', 'last_name', 'phone', 'is_staff', 'referral')
	form = UserChangeForm

admin.site.register(User, UserAdmin)
admin.site.register(ServiceProvider)
admin.site.register(Category)
