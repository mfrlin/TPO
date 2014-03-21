from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.decorators import available_attrs

def for_service_providers(view_func):
	@wraps(view_func, assigned=available_attrs(view_func))
	def _wrapped_view(request, *args, **kwargs):
		if not request.user.has_service_provider():
			raise PermissionDenied
		return view_func(request, *args, **kwargs)
	return login_required(_wrapped_view)
