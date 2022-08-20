# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views

urlpatterns = [

    # The home page
    path('', views.index, name='index'),
    path('quotes', views.QuotesView.as_view(), name='quotes'),
    path('quote', views.QuoteView.as_view(), name='quote'),
    path('settings', views.SettingsView.as_view(), name='settings'),
    path('profile-update', views.Profile_Update, name='profile-update'),
    path('stats', views.StatsView.as_view(), name='stats'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
