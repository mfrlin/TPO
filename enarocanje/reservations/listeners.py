from django.db.models.signals import post_save
from .models import Reservation
from .tasks import send_reminder


def reservation_handler(sender, instance, **kwargs):
    send_reminder.apply_async(eta=instance.datetime, kwargs={'pk': instance.pk})

post_save.connect(reservation_handler, sender=Reservation)
