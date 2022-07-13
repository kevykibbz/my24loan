
from django.urls import path
from django import views
from . import views
from .views import *
from .forms import UserResetPassword
from django.contrib.auth import views as auth_views
urlpatterns=[
    path('',views.dashboard,name='admin dashboard'),
    path('accounts/logout',views.user_logout,name='logout'),
    path('site/settings',SiteSettings.as_view(),name='site settings'),
    path('edit/card/<str:cardid>',Editcard.as_view(),name='edit card'),
    path('site/contact',views.siteContact,name='site contact'),
    path('view/cards',views.cards,name='view cards'),
    path('delete/card/<str:cardid>',views.DeleteCard,name='delete card'),
    path('site/working/days',views.siteWorking,name='site working days'),
    path('site/social/links',views.siteSocial,name='site social links'),
    path('accounts/login',LoginView.as_view(),name='login'),
    path('site/card/config',CardConfig.as_view(),name='card config'),
    path('accounts/reset/password',auth_views.PasswordResetView.as_view(form_class=UserResetPassword,template_name='panel/password_reset.html'),name='reset_password'),
    path('accounts/password/reset/link/sent',auth_views.PasswordResetDoneView.as_view(template_name='panel/password_reset_done.html'),name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='panel/password_reset_confirm.html'),name='password_reset_confirm'),
    path('accounts/password/reset/complete',auth_views.PasswordResetCompleteView.as_view(template_name='panel/password_reset_complete.html'),name='password_reset_complete'),
    path('site/admins',views.admins,name='site admins'),
    path('site/add/admins',AddAdmins.as_view(),name='add admins'),
    path('delete/loan/item/<str:loanid>',views.delLoan,name='delete loan'),
    path('site/edit/admin/<int:id>',EditAdmin.as_view(),name='edit admin'),
    path('site/delete/admin/<int:id>',views.deleteAdmin,name='delete admin'),
    path('site/employees',views.employees,name='site employees'),
    path('site/add/employee',AddEmployees.as_view(),name='add employees'),
    path('edit/loan/item/<str:loanid>',Editloan.as_view(),name='edit loan'),
    path('site/edit/employee/<int:id>',EditEmployee.as_view(),name='edit employee'),
    path('site/delete/employee/<int:id>',views.deleteEmployee,name='delete employee'),
    path('user/change/password',views.passwordChange,name='change password'),
    path('user/profile/pic',views.profilePic,name='profile pic'),
    path('<str:username>',ProfilerView.as_view(),name='profile'),
    path('loan/applications',views.applications,name='franchise applications'),
    path('customers/queries',views.queries,name='customers queries'),
    path('edit/query/<int:id>',EditQuery.as_view(),name='edit query'),
    path('delete/query/<int:id>',views.deleteQuery,name='delete query'),
    path('customer/suggestions',views.suggestions,name='customer suggestions'),
    path('delete/customer/suggestion/<int:id>',views.deleteSuggestion,name='delete suggestion'),
    path('customer/contact/messages',views.customerMessages,name='customers contacts'),
    path('view/message/<int:id>',ViewMessage.as_view(),name='view message'),


]