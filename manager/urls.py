
from django.urls import path
from django import views
from . import views
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns=[
    path('',views.home,name='dashboard'),
    path('company',views.company,name='company'),
    path('prime/membership',Prime.as_view(),name='prime'),
    path('elite/membership',views.elite,name='elite'),
    path('apply/<str:loanid>',ApplySpecific.as_view(),name='apply specific'),
    path('edit/profile',EditProfile.as_view(),name='edit profile'),
    path('payment/status',views.payment,name='payment status'),
    path('suggestion',Suggestion.as_view(),name='suggestion'),
    path('check/eligibility/<str:loanid>',Eligibility.as_view(),name='check eligibilty'),
    path('check/eligibility/step2/<str:loanid>',stepTwo.as_view(),name='step2'),
    path('check/eligibility/step3/<str:loanid>',stepThree.as_view(),name='step3'),
    path('finish/<str:loanid>',Finish.as_view(),name='step4'),
    path('digital/personal/loan',PersonalLoan.as_view(),name='personal loan'),
    path('<str:email>',Verification.as_view(),name='identity verification'),
    path('digital/business/loan',BussinessLoan.as_view(),name='bussiness loan'),
    path('contact/us',Contact.as_view(),name='contact us'),
    path('accounts/login',Login.as_view(),name='login'),
    path('accounts/change/password',UserChangePassword.as_view(),name='user change password'),
    path('accounts/logout',views.user_logout,name='logout'),
    path('raise/request',Request.as_view(),name='raise request'),
    path('terms/and/conditions',views.terms,name='terms and conditions'),
    path('privacy/policy',views.privacy,name='privacy policy'),
    path('view/suggestions',views.suggestions,name='view suggestions'),
    path('careers',views.careers,name='careers'),
    path('important/updates',views.updates,name='update'),
    path('faqs/',views.faqs,name='faqs'),
    path('return/fund/policy',views.returnFund,name='return fund policy'),
    path('disclaimer',views.disclaimer,name='disclaimer'),
    path('loan/calculator',views.loan_calculator,name='loan calculator'),
    path('accounts/reset_password',auth_views.PasswordResetView.as_view(form_class=UserResetPassword,template_name='manager/password_reset.html'),name='reset_password'),
    path('accounts/reset_password_done',auth_views.PasswordResetDoneView.as_view(template_name='manager/password_reset_done.html'),name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='manager/password_reset_confirm.html'),name='password_reset_confirm'),
    path('accounts/reset_password_complete',auth_views.PasswordResetCompleteView.as_view(template_name='manager/password_reset_complete.html'),name='password_reset_complete'),
]