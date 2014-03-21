from django.utils import timezone

def add_timezone(dt, tz=None):
	"""Adds timezone to datetime object"""
	if not tz:
		tz = timezone.get_default_timezone()
	return dt.replace(tzinfo=tz) - tz.dst(dt)

def to_timezone(dt, tz=None):
	"""Convert datetime to given timezone"""
	if not tz:
		tz = timezone.get_default_timezone()
	return dt.astimezone(tz)

def datetime_to_url_format(dt):
	dt -= timezone.get_default_timezone().utcoffset(dt)
	return ''.join(c for c in dt.isoformat('T') if c.isalnum() or c == 'T') + 'Z'

def is_overlapping(StartA, EndA, StartB, EndB):
	return (StartA < EndB) and (EndA > StartB)
