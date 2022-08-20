# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import View
from django.contrib import messages
from .forms import GetAQuoteForm
from ..home.forms import UserProfileForm
from ..authentication.forms import *
from django.conf import settings
from django.shortcuts import render, redirect
from ..home.views import send_email, insert_records
from ..home.models import *
from django.contrib.auth.hashers import make_password


def index(request):
    if not request.user.is_authenticated:
        context = {'segment': 'index'}
        form = GetAQuoteForm()
        form2 = UserProfileForm()
        if request.method == 'POST':
            form = GetAQuoteForm(request.POST, request.FILES)
            form2 = UserProfileForm(request.POST, request.FILES)
            if form.is_valid() and form2.is_valid():
                form = form.save(commit=False)
                formsave = form2.save(commit=False)
                formsave.username = form2.data['email']
                formsave.save()
                formuser = UserProfile.objects.latest('id')
                form.user = formuser
                form.save()
                # zoho CRM Contact Creation
                contact_dic = form2.cleaned_data
                insert_records(contact_dic)

                extra_info = f'Microbit Received a New Quote Request From : ' + request.user.username
                subject = "New Quote Request"
                adminemail = settings.ADMIN_EMAIL_FOR_RECEIVING_EMAILS
                send_email(adminemail, extra_info, subject)
                return redirect('/')
        context['form'] = form
        context['form2'] = form2
        html_template = loader.get_template('frontend/index.html')
        return HttpResponse(html_template.render(context, request))
    else:
        return redirect("/dashboard/")


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# @login_required(login_url="/login/")
class SettingsView(View):

    def get(self, request):

        context = {'segment': 'index'}
        context['user'] = request.user
        userid = request.user.id
        if request.user.is_staff:
            context['user'] = request.user
            context['user_name'] = request.user.username
            context['user_email'] = request.user.email
        else:
            context['user'] = UserProfile.objects.get(id=userid)
        # context['user'] = request.user


        return render(request, 'shared/settings.html', context)

    def post(self, request):
        user = request.user
        user = User.objects.get(id=user.id)
        currentpassword = request.POST['password'].strip()
        newpass1 = request.POST['password1'].strip()
        newpass2 = request.POST['password2'].strip()
        currentpasswordcheck = user.check_password(currentpassword)
        if currentpasswordcheck and newpass1 and newpass1 == newpass2:
            # if user.check_password(currentpassword):
            user.set_password(newpass1)
            user.save()
            extra_info = f'Password Changed for your Microbit Account By : ' + request.user.username
            subject = "Password Changed : Microbit"
            adminemail = settings.ADMIN_EMAIL_FOR_RECEIVING_EMAILS
            send_email(adminemail, extra_info, subject)
            messages.success(request, 'Password Changed Successfully')
        else:
            messages.error(request, 'Something is Wrong with your Passwords')
        return redirect("/dashboard/")
        # return render(request, 'shared/settings.html')

# @login_required(login_url="/login/")
def Profile_Update(request):
    if request.method == 'POST':
        user = request.user
        a = UserProfile.objects.get(id=user.id)
        form = UserProfileForm(request.POST, instance=a)

        if user.is_staff:
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            return redirect("settings")

        else:
            if form.is_valid():
                form.save()
            # return redirect("settings")
    return redirect("settings")

class QuotesView(View):
    model = GetAQuote
    template = "shared/quotes.html"

    def get(self, request):
        context = {'segment': 'index'}
        form = GetAQuoteForm(request.POST, request.FILES)
        quotes = GetAQuote.objects.filter(user=request.user.id)
        context['form'] = form
        context['quotes'] = quotes
        if request.user.is_staff:
            quotes = GetAQuote.objects.all()
            context['staff'] = request.user.is_staff
            context['quotes'] = quotes
            html_template = loader.get_template('shared/quotes.html')
            return HttpResponse(html_template.render(context, request))
        else:
            html_template = loader.get_template('shared/quotes.html')
            return HttpResponse(html_template.render(context, request))

    def post(self, request):
        form = GetAQuoteForm()
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        customer = request.POST['user']
        jobstatus = request.POST['order_status']
        staff = request.user.is_staff
        quotes = GetAQuote.objects.filter(created_time__range=[fromdate, todate]).filter(
            order_status=jobstatus).filter(user=customer)

        return render(request, 'shared/quotes.html', {'quotes':quotes, 'form':form, 'staff':staff})



class QuoteView(View):

    def get(self, request):
        return render(request, 'customer/extra-info.html')


class StatsView(View):

    def get(self, request):
        return render(request, 'staff/index.html')
