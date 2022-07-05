from django.shortcuts import render
from manager.decorators import unauthenticated_user,allowed_users
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import ExtendedAuthUser
from django.contrib.auth.models import User,Group,Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render,get_object_or_404
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse,HttpResponse
from installation.models import SiteConstants
from django.shortcuts import redirect
from .forms import *
from django.core.paginator import Paginator
from django.contrib.sites.shortcuts import get_current_site
from .addons import send_email,getSiteData
import json
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
import re
import datetime
from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.defaulttags import register
import math
from django.utils.crypto import get_random_string
from manager.addons import send_email
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import csv
from django.templatetags.static import static
from installation.models import SiteConstants
import os


# Create your views here.
def home(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    data={
        'title':f'Welcome to {obj.site_name}',
        'obj':obj,
        'data':request.user,
    }
    return render(request,'manager/index.html',context=data)

#company
def company(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    data={
        'title':'company',
        'obj':obj,
        'data':request.user,
    }
    return render(request,'manager/company.html',context=data)


#prime
def prime(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    data={
        'title':'Prime Membership',
        'obj':obj,
        'data':request.user,
    }
    return render(request,'manager/prime.html',context=data)

#elite
def elite(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    data={
        'title':'Elite Membership',
        'obj':obj,
        'data':request.user,
    }
    return render(request,'manager/elite.html',context=data)

#PersonalLoan
class PersonalLoan(View):
	def get(self,request):
		obj=SiteConstants.objects.count()
		if obj == 0:
		        return redirect('/installation/')
		obj=SiteConstants.objects.all()[0]
		data={
		    'title':'Digital Personal Loan',
		    'obj':obj,
		    'data':request.user,
		}
		return render(request,'manager/personal.html',context=data)

#'BussinessLoan
class BussinessLoan(View):
	def get(self,request):
		obj=SiteConstants.objects.count()
		if obj == 0:
		        return redirect('/installation/')
		obj=SiteConstants.objects.all()[0]
		data={
		    'title':'Digital Bussiness Loan',
		    'obj':obj,
		    'data':request.user,
		}
		return render(request,'manager/digital.html',context=data)

#terms and conditions
def terms(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    data={
        'title':'Terms And Conditions',
        'obj':obj,
        'data':request.user,
    }
    return render(request,'manager/terms.html',context=data)

#privacy policy
def privacy(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    data={
        'title':'Privacy Policy',
        'obj':obj,
        'data':request.user,
    }
    return render(request,'manager/privacy.html',context=data)


#Contact
class Contact(View):
	def get(self,request):
		obj=SiteConstants.objects.count()
		if obj == 0:
		        return redirect('/installation/')
		obj=SiteConstants.objects.all()[0]
		data={
		    'title':'Contact Us',
		    'obj':obj,
		    'data':request.user,
		}
		return render(request,'manager/contact.html',context=data)

#Login
class Login(View):
	def get(self,request):
		obj=SiteConstants.objects.count()
		if obj == 0:
		        return redirect('/installation/')
		obj=SiteConstants.objects.all()[0]
		data={
		    'title':'Login',
		    'obj':obj,
		    'data':request.user,
		}
		return render(request,'manager/login.html',context=data)

#Request
class Request(View):
	def get(self,request):
		obj=SiteConstants.objects.count()
		if obj == 0:
		        return redirect('/installation/')
		obj=SiteConstants.objects.all()[0]
		data={
		    'title':'Raise A Request',
		    'obj':obj,
		    'data':request.user,
		}
		return render(request,'manager/request.html',context=data)

#careers
def careers(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    data={
        'title':'Careers',
        'obj':obj,
        'data':request.user,
    }
    return render(request,'manager/careers.html',context=data)

#updates
def updates(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    data={
        'title':'Important Updates',
        'obj':obj,
        'data':request.user,
    }
    return render(request,'manager/updates.html',context=data)

#faqs
def faqs(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    data={
        'title':'FAQS',
        'obj':obj,
        'data':request.user,
    }
    return render(request,'manager/faqs.html',context=data)

#returnFund
def returnFund(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    data={
        'title':'Return Fund Policy',
        'obj':obj,
        'data':request.user,
    }
    return render(request,'manager/return_fund.html',context=data)

#disclaimer
def disclaimer(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    data={
        'title':'Disclaimer',
        'obj':obj,
        'data':request.user,
    }
    return render(request,'manager/disclaimer.html',context=data)


#loan_calculator
def loan_calculator(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    data={
        'title':'Loan Calculator',
        'obj':obj,
        'data':request.user,
    }
    return render(request,'manager/loan_calculator.html',context=data)