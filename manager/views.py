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
from django.contrib.auth.hashers import make_password


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
class Prime(View):
    def get(self,request):
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
        form=UsersLoanForm()
        data={
            'title':'Digital Personal Loan',
            'obj':obj,
            'data':request.user,
            'form':form
        }
        return render(request,'manager/personal.html',context=data)
    def post(self,request):
        obj=SiteConstants.objects.all()[0]
        form=UsersLoanForm(request.POST or None)
        if form.is_valid():
            presaver=form.save(commit=False)
            otp=random.randint(999,999999)
            presaver.has_applied=True
            presaver.otp=otp
            presaver.save()
            data=LoanModel.objects.all().last()
            message={
                        'user':form.cleaned_data.get('name'),
                        'site_name':obj.site_name,
                        'site_url':obj.site_url,
                        'category':data.category,
                        'address':obj.address,
                        'phone':obj.phone,
                        'otp':otp,
                }
            subject='Application received successfully.'
            email=form.cleaned_data.get('email')
            template='emails/success.html'
            send_email(subject,email,message,template)
            return JsonResponse({'valid':True,'message':'Digital personal loan applied successfully!','email':form.cleaned_data.get('email')},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'form_errors':form.errors},content_type='application/json')

#'BussinessLoan
class BussinessLoan(View):
    def get(self,request):
        obj=SiteConstants.objects.count()
        if obj == 0:
                return redirect('/installation/')
        obj=SiteConstants.objects.all()[0]
        form=UsersLoanForm()
        data={
            'title':'Digital Bussiness Loan',
            'obj':obj,
            'data':request.user,
            'form':form,
        }
        return render(request,'manager/digital.html',context=data)
    def post(self,request):
        obj=SiteConstants.objects.all()[0]
        form=UsersLoanForm(request.POST or None)
        if form.is_valid():
            presaver=form.save(commit=False)
            otp=random.randint(999,999999)
            presaver.has_applied=True
            presaver.otp=otp
            presaver.save()
            data=LoanModel.objects.all().last()
            message={
                        'user':form.cleaned_data.get('name'),
                        'site_name':obj.site_name,
                        'site_url':obj.site_url,
                        'category':data.category,
                        'address':obj.address,
                        'phone':obj.phone,
                        'otp':otp,
                }
            subject='Application received successfully.'
            email=form.cleaned_data.get('email')
            template='emails/success.html'
            send_email(subject,email,message,template)
            return JsonResponse({'valid':True,'message':'Digital bussiness loan applied successfully!','email':form.cleaned_data.get('email')},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'form_errors':form.errors},content_type='application/json')

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
        form=UsersContactForm()
        data={
            'title':'Contact Us',
            'obj':obj,
            'data':request.user,
            'form':form,
        }
        return render(request,'manager/contact.html',context=data)
    def post(self,request):
        form=UsersContactForm(request.POST or None)
        if form.is_valid():
            form.save()
            return JsonResponse({'valid':True,'message':'Message sent!'},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'form_errors':form.errors},content_type='application/json')

#Login
@method_decorator(unauthenticated_user,name='dispatch')
class Login(View):
    def get(self,request):
        obj=SiteConstants.objects.count()
        if obj == 0:
                return redirect('/installation/')
        obj=SiteConstants.objects.all()[0]
        form=UserLoginForm()
        data={
            'title':'Login',
            'obj':obj,
            'data':request.user,
            'form':form,
        }
        return render(request,'manager/login.html',context=data)
    def post(self,request):
        form=UserLoginForm(request.POST or None)
        if form.is_valid():
            user=authenticate(username=form.cleaned_data.get('username'),password=form.cleaned_data.get('password'))
            if user is not None:
                if 'remember' in request.POST:
                   request.session.set_expiry(1209600) #two weeeks
                else:
                   request.session.set_expiry(0) 
                login(request,user)
                return JsonResponse({'valid':True,'message':'logged in  successfully!','home':True},content_type='application/json')
            form_errors={"password": ["Password is incorrect or inactive account."]}
            return JsonResponse({'valid':False,'form_errors':form_errors},content_type="application/json")
        else:
            return JsonResponse({'valid':False,'form_errors':form.errors},content_type='application/json')


#logout
def user_logout(request):
    logout(request)
    return redirect('/accounts/login')

#Request
class Request(View):
    def get(self,request):
        obj=SiteConstants.objects.count()
        if obj == 0:
                return redirect('/installation/')
        obj=SiteConstants.objects.all()[0]
        form=UsersRequestForm()
        data={
            'title':'Raise A Request',
            'obj':obj,
            'data':request.user,
            'form':form
        }
        return render(request,'manager/request.html',context=data)
    def post(self,request):
        form=UsersRequestForm(request.POST or None)
        if form.is_valid():
            form.save()
            return JsonResponse({'valid':True,'message':'Request submitted successfully!'},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'form_errors':form.errors},content_type='application/json')

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

def generate_username():
    return get_random_string(6,'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKMNOPQRSTUVWXYZ0123456789')

def generate_password():
    return get_random_string(12,'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKMNOPQRSTUVWXYZ0123456789')

class Verification(View):
    def get(self,request,email):
        obj=SiteConstants.objects.count()
        if obj == 0:
                return redirect('/installation/')
        obj=SiteConstants.objects.all()[0]
        form=UsersOTPForm()
        otp_flag=request.GET.get('otp_resend')
        if  otp_flag:
            presaver=LoanModel.objects.filter(email=email).last()
            if presaver.is_verfied:
                otpmessage='Sorry,this email is already been verified.'
                flag=False
            else:
                otpmessage='OTP number sent successfully!'
                otp=random.randint(999,999999)
                presaver.otp=otp
                presaver.save()
                message={
                            'user':presaver.name,
                            'site_name':obj.site_name,
                            'site_url':obj.site_url,
                            'category':presaver.category,
                            'address':obj.address,
                            'phone':obj.phone,
                            'otp':otp,
                    }
                subject='OTP Resent!.'
                flag=True
                template='emails/success.html'
                send_email(subject,email,message,template)
            data={
                'title':'Verify email address',
                'obj':obj,
                'data':request.user,
                'email':email,
                'form':form,
                'flag':flag,
                'message':otpmessage
            }
            return render(request,'manager/verify.html',context=data)
        else:
            data={
                'title':'Verify email address',
                'obj':obj,
                'data':request.user,
                'email':email,
                'form':form,
            }
            return render(request,'manager/verify.html',context=data)
    def post(self,request,email):
        obj=SiteConstants.objects.all()[0]
        data=LoanModel.objects.filter(email=email).last()
        form=UsersOTPForm(request.POST or None,instance=data)
        if form.is_valid():
            username=generate_username()
            password=generate_password()
            preserver=form.save(commit=False)
            preserver.is_verfied=True
            preserver.save()
            if not User.objects.filter(email=email).exists():
                userdata=User.objects.create(first_name=data.name.split(" ")[0],last_name=data.name.split(" ")[1],email=email,username=username,password=make_password(password))
                ty=userdata.save(commit=False)
                ty.is_active=True
                ty.save()
                message={
                            'user':data.name,
                            'site_name':obj.site_name,
                            'site_url':obj.site_url,
                            'category':data.category,
                            'address':obj.address,
                            'phone':obj.phone,
                            'username':username,
                            'password':password,
                    }
            message={
                        'user':request.user.get_full_name,
                        'site_name':obj.site_name,
                        'site_url':obj.site_url,
                        'category':data.category,
                        'address':obj.address,
                        'phone':obj.phone,
                        'username':request.user.username,
                        'password':'******** your account password',
                }
            subject='Temporary Logging Details.'
            template='emails/success.html'
            send_email(subject,email,message,template)
            return JsonResponse({'valid':True,'message':'Email verified.We have sent a temporary logging password to your email address.','login':True},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'form_errors':form.errors},content_type='application/json')



#Onbording
@method_decorator(login_required(login_url='/accounts/login'),name='dispatch')
class Onbording(View):
    def get(self,request):
        obj=SiteConstants.objects.count()
        if obj == 0:
                return redirect('/installation/')
        obj=SiteConstants.objects.all()[0]
        data=LoanModel.objects.filter(email=request.user.email).order_by("-id")
        paginator=Paginator(data,10)
        page_num=request.GET.get('page')
        loans=paginator.get_page(page_num)
        data={
            'title':'Onbording',
            'obj':obj,
            'data':request.user,
            'loans':loans,
            'count':paginator.count,
        }
        return render(request,'manager/onbording.html',context=data)
    def post(self,request):
        form=UsersRequestForm(request.POST or None)
        if form.is_valid():
            form.save()
            return JsonResponse({'valid':True,'message':'Request submitted successfully!'},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'form_errors':form.errors},content_type='application/json')


#Apply
@method_decorator(login_required(login_url='/accounts/login'),name='dispatch')
class ApplySpecific(View):
    def get(self,request,loanid):
        obj=SiteConstants.objects.count()
        if obj == 0:
                return redirect('/installation/')
        obj=SiteConstants.objects.all()[0]
        form=UsersTotalLoanApplyForm()
        data={
            'title':'Apply for loan',
            'obj':obj,
            'data':request.user,
            'form':form
        }
        return render(request,'manager/apply.html',context=data)
    def post(self,request,loanid):
        data=LoanModel.objects.get(loanid=loanid)
        form=UsersLoanApplyForm(request.POST or None,instance=data)
        if form.is_valid():
            form.save()
            return JsonResponse({'valid':True,'message':'Loan application submitted successfully!'},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'form_errors':form.errors},content_type='application/json')


#Apply
class Apply(View):
    def get(self,request):
        obj=SiteConstants.objects.count()
        if obj == 0:
                return redirect('/installation/')
        obj=SiteConstants.objects.all()[0]
        form=UsersTotalLoanApplyForm()
        data={
            'title':'Apply for loan',
            'obj':obj,
            'data':request.user,
            'form':form,
        }
        return render(request,'manager/apply.html',context=data)
    def post(self,request):
        form=UsersTotalLoanApplyForm(request.POST or None)
        if form.is_valid():
            form.save()
            return JsonResponse({'valid':True,'message':'Request submitted successfully!'},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'form_errors':form.errors},content_type='application/json')

#suggestion
class Suggestion(View):
    def get(self,request):
        obj=SiteConstants.objects.count()
        if obj == 0:
                return redirect('/installation')
        obj=SiteConstants.objects.all()[0]
        form=UsersSuggestionForm()
        data={
            'title':'Add suggestion',
            'obj':obj,
            'data':request.user,
            'form':form,
        }
        return render(request,'manager/suggestion.html',context=data)
    def post(self,request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form=UsersSuggestionForm(request.POST or None)
            if form.is_valid():
                form.save()
                return JsonResponse({'valid':True,'message':'Suggestion posted successfully'},content_type="application/json")
            else:
                return JsonResponse({'valid':False,'form_errors':form.errors},content_type="application/json")


#suggestions
def suggestions(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
        return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    data=SuggestionForm.objects.all().order_by("-id")
    paginator=Paginator(data,20)
    page_num=request.GET.get('page')
    suggestions=paginator.get_page(page_num)
    data={
        'title':'View Suggestions',
        'obj':obj,
        'data':request.user,
        'suggestions':suggestions,
        'count':paginator.count,
    }
    return render(request,'manager/view_suggestions.html',context=data)
