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
from django import template
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
from django_otp.oath import hotp


# Create your views here.
def home(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    initials='AU'
    if request.user.is_authenticated:
       initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
    data={
        'title':f'Welcome to {obj.site_name}',
        'obj':obj,
        'data':request.user,
        'initials':initials
    }
    return render(request,'manager/index.html',context=data)



#company
def company(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    initials='AU'
    if request.user.is_authenticated:
       initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
    data={
        'title':'company',
        'obj':obj,
        'data':request.user,
        'initials':initials
    }
    return render(request,'manager/company.html',context=data)


#prime
class Prime(View):
    def get(self,request):
        obj=SiteConstants.objects.count()
        if obj == 0:
                return redirect('/installation/')
        obj=SiteConstants.objects.all()[0]
        initials='AU'
        if request.user.is_authenticated:
            initials=request.user.first_name[0].upper()+request.user.last_name[0].upper() 
        card=CardModel.objects.filter(card_type__icontains='prime membership').last()       
        data={
            'title':'Prime Membership',
            'obj':obj,
            'data':request.user,
            'card':card,
            'initials':initials
        }
        return render(request,'manager/prime.html',context=data)

#elite
def elite(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    initials='AU'
    if request.user.is_authenticated:
       initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
    card=CardModel.objects.filter(card_type__icontains='elite membership').last()
    data={
        'title':'Elite Membership',
        'obj':obj,
        'data':request.user,
        'card':card,
        'initials':initials,
    }
    return render(request,'manager/elite.html',context=data)

def create_otp(n):
    range_start=10**(n-1)
    range_end=(10**n)-1
    return random.randint(range_start,range_end)


#PersonalLoan
class PersonalLoan(View):
    def get(self,request):
        obj=SiteConstants.objects.count()
        if obj == 0:
                return redirect('/installation/')
        obj=SiteConstants.objects.all()[0]
        initials='AU'
        if request.user.is_authenticated:
           initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
        form=UsersLoanForm()
        card=CardModel.objects.filter(card_type__icontains='prime membership').last()
        data={
            'title':'Digital Personal Loan',
            'obj':obj,
            'data':request.user,
            'form':form,
            'card':card,
            'initials':initials,
        }
        return render(request,'manager/personal.html',context=data)
    def post(self,request):
        obj=SiteConstants.objects.all()[0]
        form=UsersLoanForm(request.POST or None)
        if form.is_valid():
            presaver=form.save(commit=False)
            otp=create_otp(6)
            presaver.has_applied=True
            presaver.otp=otp
            presaver.page='2'
            presaver.page_status=True
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
        initials='AU'
        if request.user.is_authenticated:
           initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
        form=UsersLoanForm()
        data={
            'title':'Digital Bussiness Loan',
            'obj':obj,
            'data':request.user,
            'form':form,
            'initials':initials,
        }
        return render(request,'manager/digital.html',context=data)
    def post(self,request):
        obj=SiteConstants.objects.all()[0]
        form=UsersLoanForm(request.POST or None)
        if form.is_valid():
            presaver=form.save(commit=False)
            otp=create_otp(6)
            presaver.has_applied=True
            presaver.otp=otp
            presaver.page='2'
            presaver.page_status=True
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
    initials='AU'
    if request.user.is_authenticated:
       initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
    data={
        'title':'Terms And Conditions',
        'obj':obj,
        'data':request.user,
        'initials':initials
    }
    return render(request,'manager/terms.html',context=data)

#privacy policy
def privacy(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    initials='AU'
    if request.user.is_authenticated:
       initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
    data={
        'title':'Privacy Policy',
        'obj':obj,
        'data':request.user,
        'initials':initials
    }
    return render(request,'manager/privacy.html',context=data)


#Contact
class Contact(View):
    def get(self,request):
        obj=SiteConstants.objects.count()
        if obj == 0:
            return redirect('/installation/')              
        obj=SiteConstants.objects.all()[0]
        initials='AU'
        if request.user.is_authenticated:
           initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
        form=UsersContactForm()
        data={
            'title':'Contact Us',
            'obj':obj,
            'data':request.user,
            'form':form,
            'initials':initials
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
        initials='AU'
        if request.user.is_authenticated:
           initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
        form=UserLoginForm()
        data={
            'title':'Login',
            'obj':obj,
            'data':request.user,
            'form':form,
            'initials':initials
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
            form_errors={"password": ["Password is incorrect."]}
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
        initials='AU'
        if request.user.is_authenticated:
           initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
        form=UsersRequestForm()
        data={
            'title':'Raise A Request',
            'obj':obj,
            'data':request.user,
            'form':form,
            'initials':initials
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
    initials='AU'
    if request.user.is_authenticated:
       initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
    data={
        'title':'Careers',
        'obj':obj,
        'data':request.user,
        'initials':initials
    }
    return render(request,'manager/careers.html',context=data)

#updates
def updates(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    initials='AU'
    if request.user.is_authenticated:
        initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
    data={
        'title':'Important Updates',
        'obj':obj,
        'data':request.user,
        'initials':initials
    }
    return render(request,'manager/updates.html',context=data)

#faqs
def faqs(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    initials='AU'
    if request.user.is_authenticated:
        initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
    data={
        'title':'FAQS',
        'obj':obj,
        'data':request.user,
        'initials':initials
    }
    return render(request,'manager/faqs.html',context=data)

#returnFund
def returnFund(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    initials='AU'
    if request.user.is_authenticated:
        initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
    data={
        'title':'Return Fund Policy',
        'obj':obj,
        'data':request.user,
        'initials':initials
    }
    return render(request,'manager/return_fund.html',context=data)

#disclaimer
def disclaimer(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    initials='AU'
    if request.user.is_authenticated:
        initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
    data={
        'title':'Disclaimer',
        'obj':obj,
        'data':request.user,
        'initials':initials
    }
    return render(request,'manager/disclaimer.html',context=data)


#loan_calculator
def loan_calculator(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    initials='AU'
    if request.user.is_authenticated:
        initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
    data={
        'title':'Loan Calculator',
        'obj':obj,
        'data':request.user,
        'initials':initials
    }
    return render(request,'manager/loan_calculator.html',context=data)

def generate_username():
    return get_random_string(6,'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKMNOPQRSTUVWXYZ0123456789')

def generate_password():
    return get_random_string(8,'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKMNOPQRSTUVWXYZ0123456789')

class Verification(View):
    def get(self,request,email):
        obj=SiteConstants.objects.all()[0]
        if LoanModel.objects.filter(email=email).exists():
            initials='AU'
            if request.user.is_authenticated:
                initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
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
                    'message':otpmessage,
                    'initials':initials
                }
                return render(request,'manager/verify.html',context=data)
            else:
                data={
                    'title':'Verify email address',
                    'obj':obj,
                    'data':request.user,
                    'email':email,
                    'form':form,
                    'initials':initials
                }
                return render(request,'manager/verify.html',context=data)
        else:
            data={
                'title':'Error | Page Not Found',
                'obj':obj
            }
            return render(request,'manager/404.html',context=data,status=404)  
    def post(self,request,email):
        data=LoanModel.objects.filter(email=email).last()
        form=UsersOTPForm(request.POST or None,instance=data)
        if form.is_valid():
            preserver=form.save(commit=False)
            preserver.is_verfied=True
            preserver.page='3'
            preserver.page_status=True
            preserver.save()
            return JsonResponse({'valid':True,'message':'Email verified.','loanid':data.loanid},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'form_errors':form.errors},content_type='application/json')





#Apply
class ApplySpecific(View):
    def get(self,request,loanid):
        obj=SiteConstants.objects.all()[0]
        try:
            loan=LoanModel.objects.get(loanid=loanid)
            initials='AU'
            if request.user.is_authenticated:
                initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
            form=UsersTotalLoanApplyForm()
            data={
                'title':'Apply for loan',
                'obj':obj,
                'data':request.user,
                'form':form,
                'loan':loan,
                'loanid':loanid,
                'initials':initials
            }
            return render(request,'manager/apply.html',context=data)
        except LoanModel.DoesNotExist:
            data={
                'title':'Error | Page Not Found',
                'obj':obj
            }
            return render(request,'manager/404.html',context=data,status=404)
    def post(self,request,loanid):
        data=LoanModel.objects.get(loanid=loanid)
        form=UsersLoanApplyForm(request.POST or None,instance=data)
        if form.is_valid():
            t=form.save(commit=False)
            t.page='4'
            t.page_status=True
            t.save()
            return JsonResponse({'valid':True,'message':'Loan application submitted successfully!','eligible':True,'loanid':loanid},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'form_errors':form.errors},content_type='application/json')


#suggestion
class Suggestion(View):
    def get(self,request):
        obj=SiteConstants.objects.count()
        if obj == 0:
                return redirect('/installation')
        obj=SiteConstants.objects.all()[0]
        initials='AU'
        if request.user.is_authenticated:
            initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
        form=UsersSuggestionForm()
        data={
            'title':'Add suggestion',
            'obj':obj,
            'data':request.user,
            'form':form,
            'initials':initials
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
    initials='AU'
    if request.user.is_authenticated:
        initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
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
        'initials':initials,
    }
    return render(request,'manager/view_suggestions.html',context=data)


#EditProfile
@method_decorator(login_required(login_url='/accounts/login'),name='dispatch')
class EditProfile(View):
    def get(self,request):
        obj=SiteConstants.objects.count()
        if obj == 0:
                return redirect('/installation')
        obj=SiteConstants.objects.all()[0]
        initials='AU'
        if request.user.is_authenticated:
           initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
        form=UsersEditForm(instance=request.user)
        data={
            'title':'Edit Profile',
            'obj':obj,
            'data':request.user,
            'form':form,
            'initials':initials
        }
        return render(request,'manager/edit_profile.html',context=data)
    def post(self,request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form=UsersEditForm(request.POST or None,instance=request.user)
            if form.is_valid():
                form.save()
                return JsonResponse({'valid':True,'message':'Profile changed successfully'},content_type="application/json")
            else:
                return JsonResponse({'valid':False,'form_errors':form.errors},content_type="application/json")

#UserChangePassword
@method_decorator(login_required(login_url='/accounts/login'),name='dispatch')
class UserChangePassword(View):
    def get(self,request):
        obj=SiteConstants.objects.count()
        if obj == 0:
                return redirect('/installation')
        obj=SiteConstants.objects.all()[0]
        initials='AU'
        if request.user.is_authenticated:
           initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()      
        form=UserPasswordChangeForm()
        data={
            'title':'Change Password',
            'obj':obj,
            'data':request.user,
            'form':form,
            'initials':initials
        }
        return render(request,'manager/change_password.html',context=data)
    def post(self,request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form=UserPasswordChangeForm(request.POST or None,instance=request.user)
            if form.is_valid():
                form.save()
                return JsonResponse({'valid':True,'message':'Password changed successfully'},content_type="application/json")
            else:
                return JsonResponse({'valid':False,'form_errors':form.errors},content_type="application/json")

#Eligibility
class Eligibility(View):
    def get(self,request,loanid):
        obj=SiteConstants.objects.all()[0]
        try:
            initials='AU'
            if request.user.is_authenticated:
                initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()      
            form=UsersEligibilityForm()
            loan=LoanModel.objects.get(loanid=loanid)
            data={
                'title':'Checking eligibilty',
                'obj':obj,
                'data':request.user,
                'form':form,
                'loanid':loanid,
                'loan':loan,
                'initials':initials,
                'step1':True,
            }
            return render(request,'manager/eligibilty.html',context=data)
        except LoanModel.DoesNotExist:
            data={
                'title':'Error | Page Not Found',
                'obj':obj
            }
            return render(request,'manager/404.html',context=data,status=404)
    def post(self,request,loanid):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data=LoanModel.objects.get(loanid=loanid)
            form=UsersEligibilityForm(request.POST or None,instance=data)
            if form.is_valid():
                t=form.save(commit=False)
                t.eligible_amount=1.8*int(data.amount)+1.3*int(form.cleaned_data.get('monthly_income'))
                t.page='5'
                t.page_status=True
                t.save()
                return JsonResponse({'valid':True,'message':'Data submitted successfully','step2':True,'loanid':loanid},content_type="application/json")
            else:
                return JsonResponse({'valid':False,'form_errors':form.errors},content_type="application/json")



#generate card number
def generate_card_number():
    return get_random_string(16,'0123456789')


#stepTwo
class stepTwo(View):
    def get(self,request,loanid):
        obj=SiteConstants.objects.all()[0]
        try:
            initials='AU'
            if request.user.is_authenticated:
                initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()      
            loan=LoanModel.objects.get(loanid=loanid)
            cardconfig=CardModel.objects.filter(loan_type__icontains=loan.category).last()
            r=int(cardconfig.interest)/100
            first=round(int(loan.eligible_amount.split(".")[0])*(r*(1+r)**12)/(((1+r)**12)-1))
            second=round(int(loan.eligible_amount.split(".")[0])*(r*(1+r)**36)/(((1+r)**36)-1))
            third=round(int(loan.eligible_amount.split(".")[0])*(r*(1+r)**48)/(((1+r)**48)-1))
            fourth=round(int(loan.eligible_amount.split(".")[0])*(r*(1+r)**60)/(((1+r)**60)-1))
            data={
                'title':'Checking eligibilty | step two',
                'obj':obj,
                'data':request.user,
                'loanid':loanid,
                'loan':loan,
                'initials':initials,
                'step2':True,
                'first':first,
                'second':second,
                'third':third,
                'fourth':fourth,
            }
            return render(request,'manager/eligibilty.html',context=data)
        except LoanModel.DoesNotExist:
            data={
                'title':'Error | Page Not Found',
                'obj':obj
            }
            return render(request,'manager/404.html',context=data,status=404)
    def post(self,request,loanid):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data=LoanModel.objects.get(loanid=loanid)
            form=UsersTenatureForm(request.POST or None,instance=data)
            if form.is_valid():
                udata=form.save(commit=False)
                udata.card_number=generate_card_number()
                udata.page='6'
                udata.page_status=True
                udata.save()
                return JsonResponse({'valid':True,'message':'Data submitted successfully','step3':True,'loanid':loanid},content_type="application/json")
            else:
                return JsonResponse({'valid':False,'form_errors':form.errors},content_type="application/json")






#stepThree
class stepThree(View):
    def get(self,request,loanid):
        obj=SiteConstants.objects.all()[0]
        try:
            initials='AU'
            if request.user.is_authenticated:
                initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()      
            loan=LoanModel.objects.get(loanid=loanid)
            card=CardModel.objects.filter(loan_type__icontains=loan.category).last()
            data={
                'title':'Checking eligibilty | step four',
                'obj':obj,
                'data':request.user,
                'loanid':loanid,
                'loan':loan,
                'initials':initials,
                'card':card,
                'card_number':loan.card_number[-4:],
                'step3':True,
            }
            return render(request,'manager/eligibilty.html',context=data)
        except LoanModel.DoesNotExist:
            data={
                'title':'Error | Page Not Found',
                'obj':obj
            }
            return render(request,'manager/404.html',context=data,status=404)
    def post(self,request,loanid):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data=LoanModel.objects.get(loanid=loanid)
            form=UsersTenatureForm(request.POST or None,instance=data)
            if form.is_valid():
                udata=form.save(commit=False)
                udata.page='7'
                udata.page_status=True
                udata.save()
                return JsonResponse({'valid':True,'message':'Data submitted successfully','step4':True,'loanid':loanid},content_type="application/json")
            else:
                return JsonResponse({'valid':False,'form_errors':form.errors},content_type="application/json")

#Finish
class Finish(View):
    def get(self,request,loanid):
        obj=SiteConstants.objects.all()[0]
        try:
            initials='AU'
            if request.user.is_authenticated:
                initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()      
            loan=LoanModel.objects.get(loanid=loanid)
            card=CardModel.objects.filter(loan_type__icontains=loan.category).last()
            data={
                'title':'Finishing...',
                'obj':obj,
                'data':request.user,
                'loanid':loanid,
                'loan':loan,
                'card':card,
                'initials':initials,
                'step4':True,
            }
            return render(request,'manager/finish.html',context=data)
        except LoanModel.DoesNotExist:
            data={
                'title':'Error | Page Not Found',
                'obj':obj
            }
            return render(request,'manager/404.html',context=data,status=404)

#payment
def payment(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
            return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    initials='AU'
    if request.user.is_authenticated:
        initials=request.user.first_name[0].upper()+request.user.last_name[0].upper()
    data={
        'title':'Payment status',
        'obj':obj,
        'data':request.user,
        'initials':initials
    }
    return render(request,'manager/payment.html',context=data)