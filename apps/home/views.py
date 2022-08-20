# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password

from django.views.generic import View
stripe.api_key = settings.STRIPE_SECRET_KEY

# This is your test secret API key.


from .models import GetAQuote , UserProfile
from .forms import ExtraInfoForm, UserProfileForm
from .forms import GetAQuoteForm as AdminGetAQuoteForm
from ..frontend.forms import GetAQuoteForm
import requests
import json

def insert_records(contactdictionary):

    url = 'https://www.zohoapis.eu/crm/v2/Contacts'

    refresh_token_url = "https://accounts.zoho.eu/oauth/v2/token?refresh_token=1000.8c4f9be7573406922dfd070d8e86bbc5.1e52c25b30123921a44c2e8721daaa3c&client_id=1000.8UGRH65GX6NNI8X0KD2736XCWGZVMR&client_secret=0bbfbbf864fb1fc47ae3690f49c613909cadd4c3d5&grant_type=refresh_token"
    response = requests.post(url=refresh_token_url)
    response_data = response.json()
    new_auth_token = response_data['access_token']

    headers = {
        'Authorization': 'Zoho-oauthtoken 1000.f9b5a427ac5d2ae4aafd254a888641cc.c1d66d606d2704aae05cdba72c850d34',
    }
    headers['Authorization'] = f'Zoho-oauthtoken {new_auth_token}'

    request_body = dict()
    record_list = list()
    print(contactdictionary)

    contactdictionary['Last_Name'] = contactdictionary.pop('last_name')
    contactdictionary['First_Name'] = contactdictionary.pop('first_name')
    contactdictionary['state'] = contactdictionary.pop('country')
    contactdictionary['Email'] = contactdictionary.pop('email')
    contactdictionary['phone'] = contactdictionary.pop('phone_number')
    contactdictionary['Mailing_Street'] = contactdictionary.pop('company_address_1')
    contactdictionary['Other_Street'] = contactdictionary.pop('company_address_2')
    contactdictionary['Mailing_City'] = contactdictionary.pop('town')
    contactdictionary['Mailing_Zip'] = contactdictionary.pop('postal_code')
    contactdictionary['Mailing_Country'] = contactdictionary.pop('state')
    contactdictionary['Title'] = contactdictionary.pop('company_role')
    contactdictionary['Account_Name'] = contactdictionary.pop('company_name')
    contactdictionary['Lead_Source'] = "Microbritt Web Application"
    # contactdictionary['Vendor_Name'] = contactdictionary.pop('company_name')
    # contactdictionary['Vendor_Name'] = "1231231231"
    # contactdictionary['Last_Name'] = contactdictionary.pop('last_name')
    # del contactdictionary[last_name]

    record_list.append(contactdictionary)
    request_body['data'] = record_list

    trigger = [
        'approval',
        'workflow',
        'blueprint'
    ]

    request_body['trigger'] = trigger

    response = requests.post(url=url, headers=headers, data=json.dumps(request_body).encode('utf-8'))

    if response is not None:
        print("HTTP Status Code : " + str(response.status_code))

        print(response.json())

def create_deal(request, id):

    url = 'https://www.zohoapis.eu/crm/v2/Deals'
    refresh_token_url = "https://accounts.zoho.eu/oauth/v2/token?refresh_token=1000.8c4f9be7573406922dfd070d8e86bbc5.1e52c25b30123921a44c2e8721daaa3c&client_id=1000.8UGRH65GX6NNI8X0KD2736XCWGZVMR&client_secret=0bbfbbf864fb1fc47ae3690f49c613909cadd4c3d5&grant_type=refresh_token"
    response = requests.post(url=refresh_token_url)
    response_data = response.json()
    new_auth_token = response_data['access_token']

    headers = {
        'Authorization': 'Zoho-oauthtoken 1000.f9b5a427ac5d2ae4aafd254a888641cc.c1d66d606d2704aae05cdba72c850d34',
    }
    headers['Authorization'] = f'Zoho-oauthtoken {new_auth_token}'
    quote = GetAQuote.objects.filter(id=id).first()

    deal = {}
    deal['Account_Name'] = str(quote.user)
    deal['Amount'] = str(quote.price)
    deal['Stage'] = '60%'
    deal['Lead_Source'] = 'Microbrit Web Application'
    # deal['Contact_Name'] = "Haris Malang"
    deal['Deal_Name'] = str(quote.user) + "Deal"

    request_body = dict()
    record_list = list()
    record_list.append(deal)
    request_body['data'] = record_list

    trigger = [
        'approval',
        'workflow',
        'blueprint'
    ]
    request_body['trigger'] = trigger
    response = requests.post(url=url, headers=headers, data=json.dumps(request_body).encode('utf-8'))

    if response is not None:
        print("HTTP Status Code : " + str(response.status_code))

        print(response.json())

    return redirect("/dashboard/")



def send_email(email,extra_info, subject):
    subject = subject
    # subject = 'Please provide extra info'
    message =  extra_info
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail( subject, message, email_from, recipient_list )
    return True

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    form = GetAQuoteForm(request.POST, request.FILES)
    context['form'] = form
    if request.user.is_staff:
        # deals_dictionary = {
        #     "Deal_Name": 'Haris Testing Deal',
        #     "Amount": 12314
        # }
        # insert_deals(deals_dictionary)
        quotes = GetAQuote.objects.all()
        context['quotes'] = quotes
        #search code
        if request.method == "POST":
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            customer = request.POST['user']
            # customer_name = ProjectName.objects.get(id=projectname_id)
            jobstatus = request.POST['order_status']


            quotes = GetAQuote.objects.filter(created_time__range=[fromdate, todate]).filter(
                order_status=jobstatus).filter(user=customer)

            context['quotes'] = quotes
            html_template = loader.get_template('staff/index.html')
            return HttpResponse(html_template.render(context, request))
        #end Search Code
        html_template = loader.get_template('staff/index.html')
        return HttpResponse(html_template.render(context, request))
    else:
        return redirect('/dashboard/customer/')

@login_required(login_url="/login/")
def customer(request):
    context = {'segment': 'index'}
    quotes = GetAQuote.objects.filter(user=request.user.id)
    context['quotes'] = quotes
    html_template = loader.get_template('customer/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def customer_duplicate_quote(request,id):
    context = {'segment': 'index'}
    oldquote = GetAQuote.objects.get(pk=id)
    oldquote.pk = None
    oldquote.price = 0
    oldquote.amount_paid = 0
    oldquote.save()
    quotes = GetAQuote.objects.filter(user=request.user.id)
    context['quotes'] = quotes
    extra_info = f'Microbit Received a Duplicate Quote Request From : ' + str(oldquote.user)
    subject = "Duplicate Quote Request : Microbit"
    adminemail = settings.ADMIN_EMAIL_FOR_RECEIVING_EMAILS
    send_email(adminemail, extra_info, subject)

    html_template = loader.get_template('customer/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def customer_qoute_detail(request,id):
    context = {'segment': 'index'}
    quote = GetAQuote.objects.filter(id=id).first()
    context['quote'] = quote
    remaining_amount = quote.price - quote.amount_paid

    context['remaining_amount'] = remaining_amount
    context['quote25percent']=remaining_amount/4
    context['quote50percent']=remaining_amount/2
    context['quote75percent']=(remaining_amount/4)*3

    html_template = loader.get_template('customer/extra-info.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def create_checkout_session(request):
    host = request.get_host()
    price1 = request.POST['payamount']
    price = int(float(price1))
    quoteid = request.POST['quoteid']
    # username = request.user.username
    useremail = request.user.email
    checkout_session = stripe.checkout.Session.create(
    customer_email=useremail,

    line_items=[
            {
                'price_data': {
                    'currency':'USD',
                    'unit_amount': price * 100,
                    'product_data':{
                        'name': quoteid,
                    },
                },
                'quantity':1,
            },
        ],
        mode='payment',
        success_url= "http://{}{}".format(host,reverse('home:payment-success')),
        cancel_url= "http://{}{}".format(host,reverse('home:payment-cancel')),
    )
    return redirect(checkout_session.url, code=303)

@login_required(login_url="/login/")
def paymentSuccess(request, *args, **kwargs):

    context = {
        'payment_status':'Payment Successfully Proccessed'
    }
    html_template = loader.get_template('customer/success.html')
    return HttpResponse(html_template.render(context, request))

@csrf_exempt
def my_webhook_view(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = "whsec_73199faea66057cdc3bb3b6797976dfff6d331d2f43075a7b1cd1575cf23ad1c"
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        line_item = session.list_line_items(session.id, limit=1).data[0]
        quote_id = line_item['description']
        amount_paid = line_item['amount_total'] / 100
        # Fulfill the purchase...
        fulfill_order(quote_id, amount_paid)


    return HttpResponse(status=200)

def fulfill_order(quote_id, amount_paidstripe):
    quote = GetAQuote.objects.get(id=quote_id)
    quote.amount_paid = quote.amount_paid + amount_paidstripe
    quote.save()
    extra_info = f'Microbit Received a Stripe Payment : ' + quote.user.username
    subject = "Payment Received : Microbit"
    adminemail = settings.ADMIN_EMAIL_FOR_RECEIVING_EMAILS
    send_email(adminemail, extra_info, subject)

    print(quote_id, quote.amount_paid)
    print("Fulfilling order")
    print("Payment was successful Congragulation Haris")

@login_required(login_url="/login/")
def paymentCancel(request):

    context = {
        'payment_status': 'cancel'
    }
    html_template = loader.get_template('customer/cancel.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def detail_quote(request,id):
    context = {'segment': 'detail-quote'}
    quote = GetAQuote.objects.filter(id=id).first()
    form = AdminGetAQuoteForm(instance=quote)

    if request.method == "POST":
        order_status_before = quote.order_status
        quoteuser = quote.user
        form = AdminGetAQuoteForm(request.POST, instance=quote)
        # quote.save(commit=False)
        # quote.user = quoteuser
        # quote.save()
        if form.is_valid():
            if request.POST['order_status'] == order_status_before:
                # form.save(commit=False)
                # form.user = quoteuser
                form.save()


            elif request.POST['order_status'] != order_status_before:
                form.save()
                extra_info = f'Order Status Changed To ' + str(quote.order_status)
                subject = "Order Status Changed: Microbit"
                send_email(request.POST['email'], extra_info,subject)

    context['quote'] = quote
    context['form'] = form
    context['remaining_amount'] = quote.price - quote.amount_paid

    html_template = loader.get_template('shared/detail-quote.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def delete_quote(request,id):
    context = {'segment': 'detail-quote'}
    quote = GetAQuote.objects.filter(id=id).delete()
    return redirect("/dashboard/")

@login_required(login_url="/login/")
def extra_info(request,id):
    context = {'segment': 'detail-quote'}
    quote = GetAQuote.objects.filter(id=id).first()
    context['quote'] = quote
    form = ExtraInfoForm()
    if request.method == "POST":
        dashboard_url = request.build_absolute_uri('/dashboard/')
        user = User.objects.filter(Q(username=request.POST['email']) | Q(email=request.POST['email'])).first()
        quotedprice = request.POST['price']
        quote.price = quotedprice
        quote.save()
        # if user.has_usable_password():
        if user.password !="":
            extra_info = f'Please login to your account and provide below info \r' + \
                         request.POST[
                             'request_for_quote'] + f'\r\r Dashboard Link: {dashboard_url} \r\r Total Price: {quotedprice}'

        else:
            my_password = User.objects.make_random_password()
            user.set_password(my_password)
            user.save()
            extra_info = f'Please login to your account and provide below info \r' + \
                         request.POST[
                             'request_for_quote'] + f'\r\r Dashboard Link: {dashboard_url} \r\r Total Price: {quotedprice} \r\r Password {my_password}'

        subject = "Please provide extra info : Microbit"
        send_email(request.POST['email'],extra_info,subject)

        redirect('/dashboard/')
    context['form'] = form
    html_template = loader.get_template('staff/ask-extra-info-email.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def ask_for_payment(request,id):
    context = {'segment': 'detail-quote'}
    quote = GetAQuote.objects.filter(id=id).first()
    context['quote'] = quote
    form = ExtraInfoForm()
    context['remaining_amount'] = quote.price - quote.amount_paid
    remaining_payment = quote.price - quote.amount_paid
    if request.method == "POST":
        # user_exist = User.objects.filter(email=request.POST['email'])
        dashboard_url = request.build_absolute_uri('/dashboard/')
        # if not user_exist:
        #     user_obj = User(username=request.POST['email'],email=request.POST['email'])
        #     user_obj.save()
        #     my_password = User.objects.make_random_password()
        #     user_obj.set_password(my_password)
        #     user_obj.save()
        #     getaqoute = GetAQuote.objects.filter(email=request.POST['email']).update(user=user_obj)
        #     quotedprice = request.POST['price']
        #     GetAQuote.objects.filter(email=request.POST['email']).update(price=quotedprice)
        #     extra_info = f'Please login to your account and Pay the Remaining Dues \r Email: {user_obj.email} \r Password: {my_password} \r' + f'\r\r Dashboard Link: {dashboard_url} \r\r Remaining Amount: {remaining_payment}'
        # else:
            # user = User.objects.filter(Q(username=request.POST['email']) | Q(email=request.POST['email'])).first()
            # getaqoute = GetAQuote.objects.filter(email=request.POST['email']).update(user=user)
        # quotedprice = request.POST['price']
        # GetAQuote.objects.filter(email=request.POST['email']).update(price=quotedprice)
        extra_info = f'Please login to your account and Pay the Remaining Dues \r'  + f'\r\r Dashboard Link: {dashboard_url} \r\r Remaining Amount: {remaining_payment}'
        subject = "Please Pay The Remaining Amount : Microbit"
        send_email(request.POST['email'],extra_info,subject)

        redirect('/dashboard/')
    context['form'] = form
    html_template = loader.get_template('staff/ask-for-payment.html')
    return HttpResponse(html_template.render(context, request))


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

@login_required(login_url="/login/")
def create_quote_staff(request):
    if request.user.is_staff:
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
                #zoho CRM Contact Creation
                contact_dic = form2.cleaned_data
                insert_records(contact_dic)

                extra_info = f'Microbit Admin Created A New Quote Request For : ' + formuser.company_name
                subject = "New Quote Created By Microbrit"
                adminemail = settings.ADMIN_EMAIL_FOR_RECEIVING_EMAILS
                send_email(adminemail, extra_info, subject)
                return redirect('/')
        context['form'] = form
        context['form2'] = form2
        html_template = loader.get_template('staff/create-a-quote-staff.html')
        return HttpResponse(html_template.render(context, request))
    else:
        return redirect("/dashboard/")


@login_required(login_url="/login/")
def create_quote_customer(request):
    context = {'segment': 'index'}
    form = GetAQuoteForm()
    context['user']=request.user
    userid = request.user.id
    userprofilemodeldata = UserProfile.objects.get(id=userid)
    if request.method == 'POST':
        form = GetAQuoteForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = userprofilemodeldata
            form.save()
            extra_info = f'Microbit Received a New Quote Request From : ' + request.user.username
            subject = "New Quote Request"
            adminemail = settings.ADMIN_EMAIL_FOR_RECEIVING_EMAILS
            send_email(adminemail, extra_info, subject)
            return redirect('/dashboard')
        else:
            pass
    context['form'] = form
    html_template = loader.get_template('customer/create-quote-customer.html')
    return HttpResponse(html_template.render(context, request))
