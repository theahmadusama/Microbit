# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import GetAQuote, ExtraInfo, UserProfile
# Register your models here.
admin.site.register(GetAQuote)
admin.site.register(ExtraInfo)
admin.site.register(UserProfile)