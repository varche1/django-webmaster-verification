# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Verification(models.Model):
    GOOGLE = 1
    BING = 2
    YANDEX = 3
    MAJESTIC = 4
    ALEXA = 5

    PROVIDERS = (
        (GOOGLE, 'Google'),
        (BING, 'Bing'),
        (YANDEX, 'Yandex'),
        (MAJESTIC, 'Majestic'),
        (ALEXA, 'Alexa'),
    )

    code = models.CharField(_('Code'), max_length=250)
    provider = models.SmallIntegerField(_('Provider'), choices=PROVIDERS)
    subdomain = models.CharField(_('Subdomain'), max_length=250, blank=True, null=True)

    def __str__(self):
        return '%s: %s' % (self.get_provider_display(), self.code)

    class Meta:
        verbose_name = _('verification')
        verbose_name_plural = _('verifications')
        unique_together = ('code', 'provider', 'subdomain')
