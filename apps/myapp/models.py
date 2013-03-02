from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models
import getpaid

class Order(models.Model):
    STATUS_CHOICES = {
        'W': _('Waiting for payment'),
        'P': _('Payment complete')
    }
    name = models.CharField(max_length=100)
    total = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    currency = models.CharField(max_length=3, default='EUR')
    status = models.CharField(max_length=1, blank=True, default='W', choices=STATUS_CHOICES.items())
    user = models.ForeignKey(User)

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})

    def amount(self):
        return u"%s %s" % (self.total, self.currency)

    @property
    def get_status(self):
        return self.STATUS_CHOICES[self.status]

    def __unicode__(self):
        return self.name

getpaid.register_to_payment(Order, unique=False, related_name='payments')

import listeners