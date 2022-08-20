# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

# Create your models here.

class UserProfile(User):
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_address_1 = models.CharField(max_length=255, null=True, blank=True)
    company_address_2 = models.CharField(max_length=255, null=True, blank=True)
    town = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    company_vat_number = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.IntegerField(blank=True, null=True)
    company_role = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.company_name


class GetAQuote(models.Model):
    ORDER_STATUS_CHOICES = (
        ('received', 'Order Received'),
        ('pending', 'Order Pending'),
        ('shipped', 'Order Shipped'),
        ('completed', 'Order Completed'),
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    order_status = models.CharField(max_length=300, null=True, blank=True, choices=ORDER_STATUS_CHOICES)
    request_for_quote = models.CharField(max_length=255 , null=True, blank=True)
    upload_design = models.FileField(upload_to='designs/', validators=[FileExtensionValidator(['pdf'])])
    health_safety = models.FileField(upload_to='health_safety/',null=True,blank=True)
    quantity = models.CharField(max_length=255,null=True,blank=True)
    material_size = models.CharField(max_length=255, null=True, blank=True)
    material_other_details = models.CharField(max_length=255, null=True, blank=True)
    material_type = models.CharField(max_length=255, null=True, blank=True)
    material = models.CharField(max_length=255, null=True, blank=True)
    delivery_date = models.CharField(max_length=255,null=True,blank=True)
    custom_info = models.CharField(max_length=255,null=True,blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(max_length=65, blank=True, null=True, default=0)
    amount_paid = models.IntegerField(max_length=65, blank=True, null=True, default=0)

    def validate_file_extension(value):
        if not value.name.endswith('.pdf'):
            raise ValidationError(u'Error message')


class ExtraInfo(models.Model):
    email = models.ForeignKey(GetAQuote, on_delete=models.CASCADE, null=True, blank=True)
    request_for_quote = models.TextField(null=True, blank=True)

