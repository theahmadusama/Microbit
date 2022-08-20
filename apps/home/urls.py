# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
app_name="home"
urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('detail-quote/<int:id>', views.detail_quote, name='detail-quote'),
    path('delete-quote/<int:id>', views.delete_quote, name='delete-quote'),
    path('extra-info/<int:id>', views.extra_info, name='extra-info'),
    path('create-deal/<int:id>', views.create_deal, name='create-deal'),
    path('ask-for-payment/<int:id>', views.ask_for_payment, name='ask-for-payment'),
    path('customer/', views.customer, name='customer'),
    path('customer-duplicate-quote/<int:id>', views.customer_duplicate_quote, name='customer-duplicate-quote'),
    path('customer-provide-extra-info/<int:id>', views.customer_qoute_detail, name='customer_quote_detail_info'),
    path('create-quote-staff', views.create_quote_staff, name='create-quote-staff'),
    path('create-quote-customer', views.create_quote_customer, name='create-quote-customer'),

    #Stripe Payment
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('success/', views.paymentSuccess, name='payment-success'),
    path('cancelled/', views.paymentCancel, name='payment-cancel'),
    path('webhook/stripe', views.my_webhook_view, name='webhook-stripe'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
