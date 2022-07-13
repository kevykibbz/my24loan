from django.shortcuts import render
from django.http import HttpResponse
from installation.models import SiteConstants
from django.shortcuts import redirect
from .decorators import unauthenticated_user,allowed_users
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User,Group,Permission
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse,HttpResponse
import re
from .forms import *
import json
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from manager.models import *
from manager.addons import send_email
import urllib

@login_required(login_url='accounts/login/')
@allowed_users(allowed_roles=['admins'])
def dashboard(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
        return redirect('/installation')
    else:
        obj=SiteConstants.objects.all()[0]
        queries=RequestModel.objects.all().count()
        queries_answered=RequestModel.objects.filter(answer__isnull=False).count()
        queries_unaswered=RequestModel.objects.filter(answer__isnull=True).count()
        message_count=ContactModel.objects.filter(reply__isnull=True).count()
        admins=User.objects.filter(extendedauthuser__role='Admin').count()
        employees=User.objects.filter(extendedauthuser__role='Employee').count()
        suggestions=SuggestionForm.objects.count()
        applications=LoanModel.objects.all().count()
        data={
                'title':f'Welcome {request.user.first_name}',
                'obj':obj,
                'data':request.user,
                'queries':queries,
                'admins':admins,
                'employees':employees,
                'applications':applications,
                'queries_unaswered':queries_unaswered,
                'queries_answered':queries_answered,
                'message_count':message_count,
                'suggestions':suggestions,
            }
        return render(request,'panel/index.html',context=data)

#logout
def user_logout(request):
    logout(request)
    return redirect('/panel/accounts/login')


@method_decorator(unauthenticated_user,name='dispatch')
class LoginView(View):
    def get(self,request):
        obj=SiteConstants.objects.all()[0]
        data={
            'title':'Login',
            'obj':obj
        }
        return render(request,'panel/login.html',context=data)
    def post(self,request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            key=request.POST['username']
            password=request.POST['password']
            if key:
                if password:
                    regex=re.compile(r'([A-Za-z0-9+[.-_]])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
                    if re.fullmatch(regex,key):
                        #email address
                        if User.objects.filter(email=key).exists():
                            data=User.objects.get(email=key)
                            user=authenticate(username=data.username,password=password)
                        else:
                            form_errors={"username": ["Invalid email address."]}
                            return JsonResponse({'valid':False,'form_errors':form_errors},content_type="application/json")
                    else:
                        #username
                        if User.objects.filter(username=key).exists():
                            user=authenticate(username=key,password=password)
                        else:
                            form_errors={"username": ["Invalid username."]}
                            return JsonResponse({'valid':False,'form_errors':form_errors},content_type="application/json")
                        
                    if user is not None:
                        if 'remember' in request.POST:
                           request.session.set_expiry(1209600) #two weeeks
                        else:
                           request.session.set_expiry(0) 
                        login(request,user)
                        return JsonResponse({'valid':True,'feedback':'success:login successfully.'},content_type="application/json")
                    form_errors={"password": ["Password is incorrect or inactive account."]}
                    return JsonResponse({'valid':False,'form_errors':form_errors},content_type="application/json")
                else:
                    form_errors={"password": ["Password is required."]}
                    return JsonResponse({'valid':False,'form_errors':form_errors},content_type="application/json")
            else:
                form_errors={"username": ["Username is required."]}
                return JsonResponse({'valid':False,'form_errors':form_errors},content_type="application/json")
        

#SiteSettings
@method_decorator(login_required(login_url='/panel/accounts/login'),name='dispatch')
@method_decorator(allowed_users(allowed_roles=['admins']),name='dispatch')
class SiteSettings(View):
    def get(self,request):
        obj=SiteConstants.objects.all()[0]
        form1=SiteForm(instance=obj)
        form2=AddressConfigForm(instance=obj)
        form3=UserSocialForm(instance=obj)
        form4=WorkingConfigForm(instance=obj)
        message_count=ContactModel.objects.filter(reply__isnull=True).count()
        data={
            'title':'Site Settings',
            'obj':obj,
            'data':request.user,
            'form1':form1,
            'form2':form2,
            'form3':form3,
            'form4':form4,
            'message_count':message_count,
        }
        return render(request,'panel/site_settings.html',context=data)
    def post(self,request,*args , **kwargs):
        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            instance_data=SiteConstants.objects.all().first()
            form=SiteForm(request.POST or None , instance=instance_data)
            if form.is_valid():
                form.save()
                return JsonResponse({'valid':True,'form_errors':'','message':'data saved successfully.'},status=200,content_type='application/json')
            else:
                return JsonResponse({'valid':False,'form_errors':form.errors},status=200,content_type='application/json')
    
#siteContact
@login_required(login_url='accounts/login/')
@allowed_users(allowed_roles=['admins'])
def siteContact(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        instance_data=SiteConstants.objects.all().first()
        form=AddressConfigForm(request.POST or None , instance=instance_data)
        if form.is_valid():
            form.save()
            return JsonResponse({'valid':True,'form_errors':'','message':'data saved successfully.'},status=200,content_type='application/json')
        else:
            return JsonResponse({'valid':False,'form_errors':form.errors},status=200,content_type='application/json')

#siteContact
@login_required(login_url='accounts/login/')
@allowed_users(allowed_roles=['admins'])
def siteWorking(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        instance_data=SiteConstants.objects.all().first()
        form=WorkingConfigForm(request.POST, request.FILES or None , instance=instance_data)
        if form.is_valid():
            form.save()
            return JsonResponse({'valid':True,'form_errors':'','message':'data saved successfully.'},status=200,content_type='application/json')
        else:
            return JsonResponse({'valid':False,'form_errors':form.errors},status=200,content_type='application/json')


#siteContact
@login_required(login_url='accounts/login/')
@allowed_users(allowed_roles=['admins'])
def siteSocial(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        instance_data=SiteConstants.objects.all().first()
        form=UserSocialForm(request.POST or None , instance=instance_data)
        if form.is_valid():
            form.save()
            return JsonResponse({'valid':True,'form_errors':'','message':'data saved successfully.'},status=200,content_type='application/json')
        else:
            return JsonResponse({'valid':False,'form_errors':form.errors},status=200,content_type='application/json')

#admins
@login_required(login_url='accounts/login/')
@allowed_users(allowed_roles=['admins'])
def admins(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
        return redirect('/installation')
    else:
        obj=SiteConstants.objects.all()[0]
        data=User.objects.filter(extendedauthuser__role='Admin').order_by('-id')
        paginator=Paginator(data,10)
        page_num=request.GET.get('page')
        users=paginator.get_page(page_num)
        message_count=ContactModel.objects.filter(reply__isnull=True).count()
        data={
            'title':'View Admins',
            'obj':obj,
            'data':request.user,
            'admins':users,
            'count':paginator.count,
            'message_count':message_count
        }
        return render(request,'panel/admins.html',context=data)

#AddAdmins
@method_decorator(login_required(login_url='/panel/accounts/login'),name='dispatch')
@method_decorator(allowed_users(allowed_roles=['admins']),name='dispatch')
class AddAdmins(View):
    def get(self,request):
        obj=SiteConstants.objects.all()[0]
        form1=users_registerForm()
        form2=EProfileForm()
        message_count=ContactModel.objects.filter(reply__isnull=True).count()
        data={
            'title':'Add Admin',
            'obj':obj,
            'data':request.user,
            'form1':form1,
            'form2':form2,
            'message_count':message_count
        }
        return render(request,'panel/add_admins.html',context=data)
    def post(self,request,*args,**kwargs):
        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
                uform=users_registerForm(request.POST or None)
                eform=EProfileForm(request.POST , request.FILES or None)
                if uform.is_valid() and  eform.is_valid():
                    userme=uform.save(commit=False)
                    userme.is_active = True
                    userme.save()
                    extended=eform.save(commit=False)
                    extended.user=userme
                    extended.initials=uform.cleaned_data.get('first_name')[0].upper()+uform.cleaned_data.get('last_name')[0].upper()
                    extended.role='Admin'
                    extended.save()
                    return JsonResponse({'valid':True,'message':'user added successfully'},content_type="application/json")
                else:
                    return JsonResponse({'valid':False,'uform_errors':uform.errors,'eform_errors':eform.errors},content_type="application/json")

#EditAdmin
@method_decorator(login_required(login_url='/panel/accounts/login'),name='dispatch')
@method_decorator(allowed_users(allowed_roles=['admins']),name='dispatch')
class EditAdmin(View):
    def get(self,request,id):
        obj=SiteConstants.objects.all()[0]
        try:
            admin=User.objects.get(id=id)
            form1=CurrentUserProfileChangeForm(instance=admin)
            form2=CurrentExtendedUserProfileChangeForm(instance=admin.extendedauthuser)
            message_count=ContactModel.objects.filter(reply__isnull=True).count()
            data={
                'title':f'Edit {admin.get_full_name()}',
                'obj':obj,
                'data':request.user,
                'form1':form1,
                'form2':form2,
                'admin':admin,
                'message_count':message_count
            }
            return render(request,'panel/edit_admin.html',context=data)
        except User.DoesNotExist:
            data={
                'title':'Error | Page Not Found',
                'obj':obj
            }
            return render(request,'manager/404.html',context=data,status=404)
    def post(self,request,id):
        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
                admin=User.objects.get(id=id)
                uform=CurrentUserProfileChangeForm(request.POST or None , instance=admin)
                eform=CurrentExtendedUserProfileChangeForm(request.POST , request.FILES or None , instance=admin.extendedauthuser)
                if uform.is_valid() and  eform.is_valid():
                    uform.save()
                    eform.save()
                    return JsonResponse({'valid':True,'message':'admin updated successfully'},content_type="application/json")
                else:
                    return JsonResponse({'valid':False,'uform_errors':uform.errors,'eform_errors':eform.errors},content_type="application/json")

#deleteAdmin
@login_required(login_url='/panel/accounts/login')
@allowed_users(allowed_roles=['admins'])
def deleteAdmin(request,id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            obj=User.objects.get(id=id)
            obj.delete() 
            return JsonResponse({'valid':False,'message':'User deleted successfully.','id':id},content_type='application/json')       
        except User.DoesNotExist:
            return JsonResponse({'valid':True,'message':'User does not exist'},content_type='application/json')

#employees
@login_required(login_url='accounts/login/')
@allowed_users(allowed_roles=['admins'])
def employees(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
        return redirect('/installation')
    else:
        obj=SiteConstants.objects.all()[0]
        data=User.objects.filter(extendedauthuser__role='Employee').order_by('-id')
        paginator=Paginator(data,10)
        page_num=request.GET.get('page')
        users=paginator.get_page(page_num)
        message_count=ContactModel.objects.filter(reply__isnull=True).count()
        data={
            'title':'View Employees',
            'obj':obj,
            'data':request.user,
            'employees':users,
            'count':paginator.count,
            'message_count':message_count
        }
        return render(request,'panel/employees.html',context=data)

#AddEmployees
@method_decorator(login_required(login_url='/panel/accounts/login'),name='dispatch')
@method_decorator(allowed_users(allowed_roles=['admins']),name='dispatch')
class AddEmployees(View):
    def get(self,request):
        obj=SiteConstants.objects.all()[0]
        form1=users_registerForm()
        form2=EProfileForm()
        message_count=ContactModel.objects.filter(reply__isnull=True).count()
        data={
            'title':'Add Employee',
            'obj':obj,
            'data':request.user,
            'form1':form1,
            'form2':form2,
            'message_count':message_count

        }
        return render(request,'panel/add_employee.html',context=data)
    def post(self,request,*args,**kwargs):
        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
                uform=users_registerForm(request.POST or None)
                eform=EProfileForm(request.POST , request.FILES or None)
                if uform.is_valid() and  eform.is_valid():
                    userme=uform.save(commit=False)
                    userme.is_active = True
                    userme.save()
                    extended=eform.save(commit=False)
                    extended.user=userme
                    extended.initials=uform.cleaned_data.get('first_name')[0].upper()+uform.cleaned_data.get('last_name')[0].upper()
                    extended.role='Employee'
                    extended.save()
                    return JsonResponse({'valid':True,'message':'user added successfully'},content_type="application/json")
                else:
                    return JsonResponse({'valid':False,'uform_errors':uform.errors,'eform_errors':eform.errors},content_type="application/json")

#EditEmployee
@method_decorator(login_required(login_url='/panel/accounts/login'),name='dispatch')
@method_decorator(allowed_users(allowed_roles=['admins']),name='dispatch')
class EditEmployee(View):
    def get(self,request,id):
        obj=SiteConstants.objects.all()[0]
        try:
            employee=User.objects.get(id=id)
            form1=CurrentUserProfileChangeForm(instance=employee)
            form2=CurrentExtendedUserProfileChangeForm(instance=employee.extendedauthuser)
            message_count=ContactModel.objects.filter(reply__isnull=True).count()
            data={
                'title':f'Edit {employee.get_full_name()}',
                'obj':obj,
                'data':request.user,
                'form1':form1,
                'form2':form2,
                'employee':employee,
                'message_count':message_count
            }
            return render(request,'panel/edit_employee.html',context=data)
        except User.DoesNotExist:
            data={
                'title':'Error | Page Not Found',
                'obj':obj
            }
            return render(request,'manager/404.html',context=data,status=404)
    def post(self,request,id):
        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
                admin=User.objects.get(id=id)
                uform=CurrentUserProfileChangeForm(request.POST or None , instance=admin)
                eform=CurrentExtendedUserProfileChangeForm(request.POST , request.FILES or None , instance=admin.extendedauthuser)
                if uform.is_valid() and  eform.is_valid():
                    uform.save()
                    eform.save()
                    return JsonResponse({'valid':True,'message':'admin updated successfully'},content_type="application/json")
                else:
                    return JsonResponse({'valid':False,'uform_errors':uform.errors,'eform_errors':eform.errors},content_type="application/json")

#deleteEmployee
@login_required(login_url='/panel/accounts/login')
@allowed_users(allowed_roles=['admins'])
def deleteEmployee(request,id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            obj=User.objects.get(id=id)
            obj.delete() 
            return JsonResponse({'valid':False,'message':'User deleted successfully.','id':id},content_type='application/json')       
        except User.DoesNotExist:
            return JsonResponse({'valid':True,'message':'User does not exist'},content_type='application/json')

#ProfilerView
@method_decorator(login_required(login_url='/panel/accounts/login'),name='dispatch')
class ProfilerView(View):
    def get(self,request,username):
        obj=SiteConstants.objects.count()
        if obj == 0:
            return redirect('/installation')
        else:
            obj=SiteConstants.objects.all()[0]
            form1=CurrentUserProfileChangeForm1(instance=request.user)
            form2=CurrentExtendedUserProfileChangeForm1(instance=request.user.extendedauthuser)
            form3=UserPasswordChangeForm()
            form4=ProfilePicChangeForm()
            message_count=ContactModel.objects.filter(reply__isnull=True).count()
            data={
                    'title':f'{request.user.first_name} profile',
                    'obj':obj,
                    'data':request.user,
                    'form1':form1,
                    'form2':form2,
                    'form3':form3,
                    'form4':form4,
                    'message_count':message_count
                }
            return render(request,'panel/profile.html',context=data)

    def post(self,request,username):
        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
                uform=CurrentUserProfileChangeForm1(request.POST or None , instance=request.user)
                eform=CurrentExtendedUserProfileChangeForm1(request.POST , request.FILES or None , instance=request.user.extendedauthuser)
                if uform.is_valid() and  eform.is_valid():
                    if uform.has_changed() or eform.has_changed():
                        uform.save()
                        eform.save()
                        return JsonResponse({'valid':True,'message':'data updated successfully'},content_type="application/json")
                    else:
                        return JsonResponse({'valid':False,'error':'No changes made'},content_type='application/json')
                else:
                    return JsonResponse({'valid':False,'uform_errors':uform.errors,'eform_errors':eform.errors},content_type="application/json")

#passwordChange
@login_required(login_url='/panel/accounts/login')
def passwordChange(request):
    if request.method=='POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        passform=UserPasswordChangeForm(request.POST or None,instance=request.user)
        if passform.is_valid():
            user=User.objects.get(username__exact=request.user.username)
            user.password=make_password(passform.cleaned_data.get('password1'))
            user.save()
            update_session_auth_hash(request,request.user)
            return JsonResponse({'valid':True,'message':'data saved'},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'uform_errors':passform.errors},content_type='application/json')

#profilePic
@login_required(login_url='/panel/accounts/login')
def profilePic(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        uform=ProfilePicChangeForm(request.POST, request.FILES or None , instance=request.user.extendedauthuser)
        if uform.is_valid():
            if uform.has_changed():
                uform.save()
                return JsonResponse({'valid':True,'message':'profile picture updated successfully'},content_type="application/json")
            else:
                return JsonResponse({'valid':False,'error':'No changes made'},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'uform_errors':uform.errors},content_type="application/json")


#applications
@login_required(login_url='/panel/accounts/login')
@allowed_users(allowed_roles=['admins'])
def applications(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
        return redirect('/installation')
    else:
        obj=SiteConstants.objects.all()[0]
        message_count=ContactModel.objects.filter(reply__isnull=True).count()
        datefilter=request.GET.get('datefilter')
        if datefilter:
            dataset=urllib.parse.unquote(datefilter)
            startdate=dataset.split('to')[0]
            enddate=dataset.split('to')[1]
            totallength=len(startdate)+len(enddate)
            if totallength == 20:
                data=LoanModel.objects.filter(created_on__gte=startdate,created_on__lte=enddate).order_by('-id')
                paginator=Paginator(data,30)
                page_num=request.GET.get('page')
                applications=paginator.get_page(page_num)
                data={
                        'title':'Loan applications',
                        'obj':obj,
                        'data':request.user,
                        'applications':applications,
                        'count':paginator.count,
                        'message_count':message_count
                }
                return render(request,'panel/applications.html',context=data)
            else:
                data=LoanModel.objects.all().order_by('-id')
                paginator=Paginator(data,30)
                page_num=request.GET.get('page')
                applications=paginator.get_page(page_num)
                data={
                        'title':'Loan applications',
                        'obj':obj,
                        'data':request.user,
                        'applications':applications,
                        'count':paginator.count,
                        'message_count':message_count
                }
                return render(request,'panel/applications.html',context=data)
        else:
            data=LoanModel.objects.all().order_by('-id')
            paginator=Paginator(data,30)
            page_num=request.GET.get('page')
            applications=paginator.get_page(page_num)
            data={
                    'title':'Loan applications',
                    'obj':obj,
                    'data':request.user,
                    'applications':applications,
                    'count':paginator.count,
                    'message_count':message_count
                }
            return render(request,'panel/applications.html',context=data)

#queries
@login_required(login_url='/panel/accounts/login')
@allowed_users(allowed_roles=['admins'])
def queries(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
        return redirect('/installation')
    else:
        obj=SiteConstants.objects.all()[0]
        data=RequestModel.objects.all().order_by('-id')
        paginator=Paginator(data,30)
        page_num=request.GET.get('page')
        queries=paginator.get_page(page_num)
        message_count=ContactModel.objects.filter(reply__isnull=True).count()
        data={
            'title':'Customer queries',
            'obj':obj,
            'data':request.user,
            'queries':queries,
            'count':paginator.count,
            'message_count':message_count,
        }
        return render(request,'panel/queries.html',context=data)
#EditQuery
@method_decorator(login_required(login_url='/panel/accounts/login'),name='dispatch')
@method_decorator(allowed_users(allowed_roles=['admins']),name='dispatch')
class EditQuery(View):
    def get(self,request,id):
        obj=SiteConstants.objects.all()[0]
        try:
            query=RequestModel.objects.get(id=id)
            form=UsersQueryForm(instance=query)
            message_count=ContactModel.objects.filter(reply__isnull=True).count()
            data={
                'title':f'Answer {query.query}',
                'obj':obj,
                'data':request.user,
                'form':form,
                'query':query,
                'message_count':message_count
            }
            return render(request,'panel/edit_query.html',context=data)
        except RequestModel.DoesNotExist:
            data={
                'title':'Error | Page Not Found',
                'obj':obj
            }
            return render(request,'manager/404.html',context=data,status=404)
    def post(self,request,id):
        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            query=RequestModel.objects.get(id=id)
            form=UsersQueryForm(request.POST or None , instance=query)
            if form.is_valid():
                form.save()
                return JsonResponse({'valid':True,'message':'Query answered successfully'},content_type="application/json")
            else:
                return JsonResponse({'valid':False,'uform_errors':form.errors},content_type="application/json")

#deleteQuery
@login_required(login_url='/panel/accounts/login')
@allowed_users(allowed_roles=['admins'])
def deleteQuery(request,id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            obj=RequestModel.objects.get(id=id)
            obj.delete() 
            return JsonResponse({'valid':False,'message':'Query deleted successfully.','id':id},content_type='application/json')       
        except RequestModel.DoesNotExist:
            return JsonResponse({'valid':True,'message':'Query does not exist'},content_type='application/json')

#suggestions
@login_required(login_url='/panel/accounts/login')
@allowed_users(allowed_roles=['admins'])
def suggestions(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
        return redirect('/installation')
    else:
        obj=SiteConstants.objects.all()[0]
        data=SuggestionForm.objects.all().order_by('-id')
        paginator=Paginator(data,30)
        page_num=request.GET.get('page')
        suggestions=paginator.get_page(page_num)
        message_count=ContactModel.objects.filter(reply__isnull=True).count()
        data={
            'title':'Customer suggestions',
            'obj':obj,
            'data':request.user,
            'suggestions':suggestions,
            'count':paginator.count,
            'message_count':message_count
        }
        return render(request,'panel/suggestions.html',context=data)

#deleteSuggestion
@login_required(login_url='/panel/accounts/login')
@allowed_users(allowed_roles=['admins'])
def deleteSuggestion(request,id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            obj=SuggestionForm.objects.get(id=id)
            obj.delete() 
            return JsonResponse({'valid':False,'message':'Suggestion deleted successfully.','id':id},content_type='application/json')       
        except SuggestionForm.DoesNotExist:
            return JsonResponse({'valid':True,'message':'Suggestion does not exist'},content_type='application/json')

#customerMessages
@login_required(login_url='/panel/accounts/login')
@allowed_users(allowed_roles=['admins'])
def customerMessages(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
        return redirect('/installation')
    else:
        obj=SiteConstants.objects.all()[0]
        data=ContactModel.objects.all().order_by('-id')
        paginator=Paginator(data,30)
        page_num=request.GET.get('page')
        messages=paginator.get_page(page_num)
        message_count=ContactModel.objects.filter(reply__isnull=True).count()
        data={
            'title':'Customer messages',
            'obj':obj,
            'data':request.user,
            'messages':messages,
            'count':paginator.count,
            'message_count':message_count,
        }
        return render(request,'panel/messages.html',context=data)



#ViewMessage
@method_decorator(login_required(login_url='/panel/accounts/login'),name='dispatch')
@method_decorator(allowed_users(allowed_roles=['admins']),name='dispatch')
class ViewMessage(View):
    def get(self,request,id):
        obj=SiteConstants.objects.all()[0]
        try:
            message=ContactModel.objects.get(id=id)
            form=UsersReplyForm(instance=message)
            message_count=ContactModel.objects.filter(reply__isnull=True).count()
            data={
                'title':f'Viewing {message.name} message',
                'obj':obj,
                'data':request.user,
                'form':form,
                'message':message,
                'message_count':message_count,
            }
            return render(request,'panel/view_message.html',context=data)
        except ContactModel.DoesNotExist:
            data={
                'title':'Error | Page Not Found',
                'obj':obj
            }
            return render(request,'manager/404.html',context=data,status=404)
    def post(self,request,id):
        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            obj=SiteConstants.objects.all()[0]
            message=ContactModel.objects.get(id=id)
            form=UsersReplyForm(request.POST or None , instance=message)
            email=request.POST['email']
            subject=request.POST['subject']
            if form.is_valid():
                t=form.save(commit=False)
                t.isread=True
                t.save()
                message={
                        'user':email.split('@')[0],
                        'site_name':obj.site_name,
                        'site_url':obj.site_url,
                        'message':form.cleaned_data.get('reply')
                    }
                template='emails/reply.html'
                send_email(subject,email,message,template)
                return JsonResponse({'valid':True,'message':'Message replied successfully'},content_type="application/json")
            else:
                return JsonResponse({'valid':False,'uform_errors':form.errors},content_type="application/json")


#delLoan
@login_required(login_url='/panel/accounts/login')
def delLoan(request,loanid):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            obj=LoanModel.objects.get(loanid=loanid)
            obj.delete() 
            return JsonResponse({'valid':False,'message':'Loan item deleted successfully.','loanid':loanid},content_type='application/json')       
        except RequestModel.DoesNotExist:
            return JsonResponse({'valid':True,'message':'Query does not exist'},content_type='application/json')


#Editloan
@method_decorator(login_required(login_url='/panel/accounts/login'),name='dispatch')
@method_decorator(allowed_users(allowed_roles=['admins']),name='dispatch')
class Editloan(View):
    def get(self,request,loanid):
        obj=SiteConstants.objects.all()[0]
        try:
            loan=LoanModel.objects.get(loanid=loanid)
            form=UsersQueryForm(instance=loan)
            data={
                'title':'Edit loan item',
                'obj':obj,
                'data':request.user,
                'form':form,
                'loan':loan,
            }
            return render(request,'panel/edit_loan.html',context=data)
        except LoanModel.DoesNotExist:
            data={
                'title':'Error | Page Not Found',
                'obj':obj
            }
            return render(request,'manager/404.html',context=data,status=404)

    def post(self,request,loanid):
        status=request.POST['action']
        loan=LoanModel.objects.get(loanid=loanid)
        loan.status=status
        loan.save()
        return JsonResponse({'valid':True,'message':'Data saved successfully.'},content_type='application/json')       


#CardConfig
@method_decorator(login_required(login_url='/panel/accounts/login'),name='dispatch')
@method_decorator(allowed_users(allowed_roles=['admins']),name='dispatch')
class CardConfig(View):
    def get(self,request):
        obj=SiteConstants.objects.all()[0]
        form=CardConfigForm()
        data={
            'title':'Card configuration settings',
            'obj':obj,
            'data':request.user,
            'form':form,
        }
        return render(request,'panel/card_config.html',context=data)

    def post(self,request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form=CardConfigForm(request.POST or None)
            if form.is_valid():
                form.save()
                return JsonResponse({'valid':True,'message':'data saved'},content_type='application/json')
            else:
                return JsonResponse({'valid':False,'uform_errors':form.errors},content_type='application/json')

#cards
@login_required(login_url='/panel/accounts/login')
@allowed_users(allowed_roles=['admins'])
def cards(request):
    obj=SiteConstants.objects.all()[0]
    cards=CardModel.objects.all().order_by('-id')
    data={
        'title':'View available cards',
        'obj':obj,
        'data':request.user,
        'cards':cards,
    }
    return render(request,'panel/card.html',context=data)

#DeleteCard
@login_required(login_url='/panel/accounts/login')
@allowed_users(allowed_roles=['admins'])
def DeleteCard(request,cardid):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            obj=CardModel.objects.get(config_id=cardid)
            obj.delete() 
            return JsonResponse({'valid':False,'message':'Card deleted successfully.','id':id},content_type='application/json')       
        except CardModel.DoesNotExist:
            return JsonResponse({'valid':True,'message':'Card does not exist'},content_type='application/json')


#Editcard
@method_decorator(login_required(login_url='/panel/accounts/login'),name='dispatch')
@method_decorator(allowed_users(allowed_roles=['admins']),name='dispatch')
class Editcard(View):
    def get(self,request,cardid):
        obj=SiteConstants.objects.all()[0]
        try:
            card=CardModel.objects.get(config_id=cardid)
            form=CardConfigEditForm(instance=card)
            data={
                'title':f'Edit {card.card_type} card',
                'obj':obj,
                'data':request.user,
                'form':form,
            }
            return render(request,'panel/card_config.html',context=data)
        except CardModel.DoesNotExist:
            data={
                'title':'Error | Page Not Found',
                'obj':obj
            }
            return render(request,'manager/404.html',context=data,status=404)

    def post(self,request,cardid):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            card=CardModel.objects.get(config_id=cardid)
            form=CardConfigEditForm(request.POST or None,instance=card)
            if form.is_valid():
                form.save()
                return JsonResponse({'valid':True,'message':'Card details updated successfully'},content_type='application/json')
            else:
                return JsonResponse({'valid':False,'uform_errors':form.errors},content_type='application/json')