from django.db import models
from enarocanje.accountext.models import ServiceProvider

class Newsletter(models.Model):
    provider = models.ForeignKey(ServiceProvider)
    date_sent = models.DateTimeField('date sent')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    number_of_subscribers = models.IntegerField(default=0)

    def __unicode__(self):
        return self.subject