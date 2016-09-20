# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Verification


@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'provider', 'subdomain')
    list_display_links = ('code',)
    list_filter = ('provider',)
    search_fields = ('code', 'subdomain')
