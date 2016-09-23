# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Verification(models.Model):
    PROVIDER_GOOGLE = 1
    PROVIDER_BING = 2
    PROVIDER_YANDEX = 3
    PROVIDER_MAJESTIC = 4
    PROVIDER_ALEXA = 5

    PROVIDERS = (
        (PROVIDER_GOOGLE, 'Google'),
        (PROVIDER_BING, 'Bing'),
        (PROVIDER_YANDEX, 'Yandex'),
        (PROVIDER_MAJESTIC, 'Majestic'),
        (PROVIDER_ALEXA, 'Alexa'),
    )

    code = models.CharField(_('Code'), max_length=250)
    provider = models.SmallIntegerField(_('Provider'), choices=PROVIDERS)
    subdomain = models.CharField(_('Subdomain'), max_length=250, blank=True, null=True, default='')

    def __str__(self):
        return '%s: %s' % (self.get_provider_display(), self.code)

    class Meta:
        verbose_name = _('verification')
        verbose_name_plural = _('verifications')
        unique_together = ('code', 'provider', 'subdomain')
