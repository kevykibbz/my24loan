from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import *
from django import forms
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.forms import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.hashers import check_password
from django.core.validators import FileExtensionValidator,URLValidator
from installation.models import SiteConstants
from django.contrib.auth import authenticate

class UserResetPassword(PasswordResetForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter email address'}),error_messages={'required':'Email address is required'})

    def clean_email(self):
        email=self.cleaned_data['email']
        if  not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email address does not exist')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError('Invalid email address')
        return email


class UsersContactForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Full name','aria-label':'name'}),error_messages={'required':'Full name is required'})
    phone=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'aria-required':'true','class':'form-control','type':'tel','aria-label':'phone','placeholder':'Phone'},initial="IN"),error_messages={'required':'Phone number is required'})
    email=forms.EmailField(widget=forms.EmailInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Email address','aria-label':'email'}),error_messages={'required':'Email address is required'})
    subject=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'subject ','aria-label':'subject'}),error_messages={'required':'Subject is required'})
    message=forms.CharField(widget=forms.Textarea(attrs={'rows':5,'aria-required':'true','class':'form-control','placeholder':'Message','aria-label':'message'}),error_messages={'required':'Message is required','min_length':'enter atleast 6 characters long'})

    class Meta:
        model=ContactModel
        fields=['name','phone','email','subject','message',]


    def clean_name(self):
        name=self.cleaned_data['name']
        if len(name.split(" ")) > 1:
            first_name=name.split(" ")[0]
            last_name=name.split(" ")[1]
            if not str(first_name).isalpha():
                raise forms.ValidationError('only characters are allowed')
            elif not str(last_name).isalpha():
                raise forms.ValidationError('only characters are allowed')
        return name

           

    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            validate_email(email)
        except ValidationError as e:
            raise forms.ValidationError('invalid email address')
        return email

class UsersLoanForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Full name','aria-label':'name'}),error_messages={'required':'Full name is required'})
    email=forms.EmailField(widget=forms.EmailInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Email address','aria-label':'email'}),error_messages={'required':'Email id is required'})
    phone=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'aria-required':'true','class':'form-control','type':'tel','aria-label':'phone','placeholder':'Bank registered phone number'},initial="IN") ,error_messages={'required':'Phone number is required'})
    category=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','aria-label':'category'}),error_messages={'required':'Category is required'})

    class Meta:
        model=LoanModel
        fields=['name','phone','category','email',]


    def clean_name(self):
        name=self.cleaned_data['name']
        if len(name.split(" ")) > 1:
            first_name=name.split(" ")[0]
            last_name=name.split(" ")[1]
            if not str(first_name).isalpha():
                raise forms.ValidationError('only characters are allowed')
            elif not str(last_name).isalpha():
                raise forms.ValidationError('only characters are allowed')
        return name

    def clean_email(self):
        email=self.cleaned_data['email']
        if LoanModel.objects.filter(email=email).exists():
            data=LoanModel.objects.filter(email=email).last()
            if data.has_applied:
                link=''
                if data.page =='2':
                    link="/"+data.email
                elif data.page == '3':
                    link="/apply/"+data.loanid
                elif data.page == '4':
                    link="/check/eligibility/"+data.loanidel
                elif data.page == '5':
                    link="/check/eligibility/step2/"+data.loanid
                elif data.page == '6':
                    link="/check/eligibility/step3/"+data.loanid
                else:
                    link="/finish/"+data.loanid
                raise forms.ValidationError('Sorry your application is still active. Click <a href="'+link+'">here</a> to continue.')
            else:
                return email
        try:
            validate_email(email)
        except ValidationError as e:
            raise forms.ValidationError('invalid email address')
        return email

    def clean_phone(self):
        phone=self.cleaned_data['phone']
        if LoanModel.objects.filter(phone=phone).exists():
            data=LoanModel.objects.filter(phone=phone).last()
            if data.has_applied:
                link=''
                if data.page =='2':
                    link="/"+data.email
                elif data.page == '3':
                    link="/apply/"+data.loanid
                elif data.page == '4':
                    link="/check/eligibility/"+data.loanidel
                elif data.page == '5':
                    link="/check/eligibility/step2/"+data.loanid
                elif data.page == '6':
                    link="/check/eligibility/step3/"+data.loanid
                else:
                    link="/finish/"+data.loanid
                raise forms.ValidationError('Sorry your application is still active. Click <a href="'+link+'">finish/<str:loanid></a> to continue.')
class UsersOTPForm(forms.ModelForm):
    otp=forms.CharField(widget=forms.NumberInput(attrs={'maxlength':6, 'data-validation-regex':'[0-9]+','aria-required':'true','class':'form-control text-center','placeholder':'OTP number','aria-label':'otp'}),error_messages={'required':'OTP number is required','maxlength':'Minimum of six digits is required.'})
    class Meta:
        model=LoanModel
        fields=['otp',]

    def clean_otp(self):
        otp=self.cleaned_data['otp']
        if self.instance.otp == int(otp):
            data=LoanModel.objects.get(otp=otp)
            if data.is_verfied:
                raise forms.ValidationError('Sorry,this email is already been verified.')
            else:
                return otp
        else:
            raise forms.ValidationError('Wrong OTP Number.')


opts=[
        ('---Select issue---',
            (
                ('Service Problem','Service Problem'),
                ('Payment Issue','Payment Issue'),
                ('Technical Problem','Technical Problem'),
                ('Eligibility or Pre-Approval Query','Eligibility or Pre-Approval Query'),
                ('Other','Other'),
            )
        ),
]
class UsersRequestForm(forms.ModelForm):
    user=forms.ChoiceField(choices=[('customer','customer'),('guest user','guest user'),],widget=forms.RadioSelect(attrs={'class':'form-check-input','aria-label':'user'}),error_messages={'required':'User category is required'})
    phone=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'aria-required':'true','class':'form-control','type':'tel','aria-label':'phone','placeholder':'Bank registered phone number'},initial="IN") ,error_messages={'required':'Phone number is required'})
    name=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Full name','aria-label':'name'}),error_messages={'required':'Full name is required'})
    email=forms.EmailField(widget=forms.EmailInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Email address','aria-label':'email'}),error_messages={'required':'Email id is required'})
    card_number=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Card number','aria-label':'card_number'}),required=False)
    query=forms.ChoiceField(choices=opts,widget=forms.Select(attrs={'aria-required':'true','class':'form-control','placeholder':'Card number','aria-label':'card_number'}),required=False)
    message=forms.CharField(widget=forms.Textarea(attrs={'rows':5,'maxlength':60,'aria-required':'true','class':'form-control','placeholder':'Request message minimum of 60 characters','aria-label':'message'}),error_messages={'required':'Request message is required'})

    class Meta:
        model=RequestModel
        fields=['name','phone','user','email','card_number','query','message',]


    def clean_name(self):
        name=self.cleaned_data['name']
        if len(name.split(" ")) > 1:
            first_name=name.split(" ")[0]
            last_name=name.split(" ")[1]
            if not str(first_name).isalpha():
                raise forms.ValidationError('only characters are allowed')
            elif not str(last_name).isalpha():
                raise forms.ValidationError('only characters are allowed')
        return name

    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            validate_email(email)
        except ValidationError as e:
            raise forms.ValidationError('invalid email address')
        return email


class UserLoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Username ','aria-label':'username'}),error_messages={'required':'Username  is required'})
    password=forms.CharField(widget=forms.PasswordInput(attrs={'aria-required':'true','class':'form-control login-password','placeholder':'Password','aria-label':'password'}),error_messages={'required':'Password is required'})

    class Meta:
        model=User
        fields=['username','password',]

    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            return username
        else:
            raise forms.ValidationError('invalid username')



#sugggestion form
class UsersSuggestionForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Enter name','aria-label':'name'}),error_messages={'required':'Name is required'})
    subject=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Subject','aria-label':'subject'}),error_messages={'required':'Subject is required'})
    city=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Enter city','aria-label':'city'}),error_messages={'required':'City is required'})
    state=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Enter state','aria-label':'state'}),error_messages={'required':'State is required'})
    email=forms.EmailField(widget=forms.EmailInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Enter email address','aria-label':'email'}),error_messages={'required':'Email address is required'})
    suggestion=forms.CharField(min_length=10,widget=forms.Textarea(attrs={'aria-required':'true','class':'form-control','placeholder':'Post your suggestion today','rows':6,'aria-label':'suggestion'}),error_messages={'required':'Suggestion is required','min_length':'enter atleast 10 characters long message'})
    class Meta:
        model=SuggestionForm
        fields=['name','email','suggestion','city','state','subject',]
    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            validate_email(email)
        except ValidationError as e:
            raise forms.ValidationError('invalid email address')
        return email

class UsersLoanApplyForm(forms.ModelForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Enter email address','aria-label':'email'}),error_messages={'required':'Email address is required'})
    bank_email=forms.EmailField(widget=forms.EmailInput(attrs={'aria-required':'true','class':'form-control','aria-label':'bank_email'}),error_messages={'required':'Registered bank email address is required'})
    user_type=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Enter User type','aria-label':'user_type'}),error_messages={'required':'User type  is required'})
    amount=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Loan amount','aria-label':'amount'}),error_messages={'required':'Loan amount is required'})

    class Meta:
        model=LoanModel
        fields=['amount','user_type','email','bank_email']

    def clean(self):
        cleaned_data=super().clean()
        email=cleaned_data.get('email')
        if LoanModel.objects.filter(email=email).exists():
            data=LoanModel.objects.filter(email=email).last()
            if data.has_applied:
                link=''
                page_no=int(data.page)
                if page_no > 3:
                    if page_no == 4:
                        link="/check/eligibility/"+data.loanid
                    elif page_no == 5:
                        link="/check/eligibility/step2/"+data.loanid
                    elif page_no == 6:
                        link="/check/eligibility/step3/"+data.loanid
                    else:
                        link="/finish/"+data.loanid
                    self.add_error('amount','Sorry your application is still active. Click <a href="'+link+'">here</a> to continue.')
            else:
                return email



class UsersTotalLoanApplyForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Full name','aria-label':'name'}),error_messages={'required':'Full name is required'})
    email=forms.EmailField(widget=forms.EmailInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Email address','aria-label':'email'}),error_messages={'required':'Email id is required'})
    category=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','aria-label':'category'}),error_messages={'required':'Category is required'})
    user_type=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Enter User type','aria-label':'user_type'}),error_messages={'required':'User type  is required'})
    amount=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Loan amount','aria-label':'amount'}),error_messages={'required':'Loan amount is required'})
    class Meta:
        model=LoanModel
        fields=['name','category','email','user_type','amount',]

#UsersEditForm
class UsersEditForm(UserChangeForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'First name','aria-label':'first_name'}),error_messages={'required':'First name is required'})
    last_name=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','aria-label':'last_name','placeholder':'Last name'}),error_messages={'required':'Last name is required'})
    username=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','aria-label':'username','placeholder':'Username'}),error_messages={'required':'Username is required'})
    email=forms.EmailField(widget=forms.EmailInput(attrs={'aria-required':'true','class':'form-control','aria-label':'email','placeholder':'Email'}),error_messages={'required':'Email address is required'})
    class Meta:
        model=User
        fields=['first_name','last_name','email','username',]


    def clean_first_name(self):
        first_name=self.cleaned_data['first_name']
        if not str(first_name).isalpha():
                raise forms.ValidationError('only characters are allowed.')
        return first_name
    
    def clean_last_name(self):
        last_name=self.cleaned_data['last_name']
        if not str(last_name).isalpha():
                raise forms.ValidationError('only characters are allowed.')
        return last_name

    def clean_email(self):
        email=self.cleaned_data['email']
        if email != self.instance.email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('A user with this email already exists.')
            try:
                validate_email(email)
            except ValidationError as e:
                raise forms.ValidationError('Invalid email address.')
            return email
        else:
           return email

    def clean_username(self):
        username=self.cleaned_data['username']
        if username != self.instance.username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('A user with this username already exists.')
        else:
           return username

class UserPasswordChangeForm(UserCreationForm):
    oldpassword=forms.CharField(widget=forms.PasswordInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Old password','aria-label':'oldpassword'}),error_messages={'required':'Old password is required','min_length':'enter atleast 6 characters long'})
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'aria-required':'true','class':'form-control','placeholder':'New password Eg Example12','aria-label':'password1'}),error_messages={'required':'New password is required','min_length':'enter atleast 6 characters long'})
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Confirm new password','aria-label':'password2'}),error_messages={'required':'Confirm new password is required'})

    class Meta:
        model=User
        fields=['password1','password2']
    
    def clean_oldpassword(self):
        oldpassword=self.cleaned_data['oldpassword']
        if not self.instance.check_password(oldpassword):
            raise forms.ValidationError('Wrong old password.')
        else:
           return oldpassword 
class UsersEligibilityForm(forms.ModelForm):
    cibil_score=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Cibil score','aria-label':'cibil_score'}),error_messages={'required':'Cibil score is required'})
    loanid=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','aria-label':'loanid'}),error_messages={'required':'Loan id is required'})
    loan_purpose=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','aria-label':'loan_purpose'}),error_messages={'required':'Loan purpose is required'})
    monthly_income=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Monthly income','aria-label':'monthly_income'}),error_messages={'required':'Monthly income is required'})
    city=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'City','aria-label':'city'}),error_messages={'required':'City is required'})
    monthly_emi=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Monthly EMI','aria-label':'monthly_emi'}),error_messages={'required':'Monthly EMI is required'})
    state=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','aria-label':'state'}),error_messages={'required':'State is required'})

    class Meta:
        model=LoanModel
        fields=['cibil_score','loan_purpose','monthly_income','city','monthly_emi','state',]

    def clean(self):
        cleaned_data=super().clean()
        loanid=cleaned_data.get('loanid')
        url=cleaned_data.get('url')
        if LoanModel.objects.filter(loanid=loanid).exists():
            data=LoanModel.objects.filter(loanid=loanid).last()
            if data.has_applied:
                link=''
                page_no=int(data.page)
                if page_no > 4:
                    if page_no == 5:
                        link="/check/eligibility/step2/"+data.loanid
                    elif page_no == 6:
                        link="/check/eligibility/step3/"+data.loanid
                    else:
                        link="/finish/"+data.loanid
                    self.add_error('state','Sorry your application is still active. Click <a href="'+link+'">here</a> to continue.')
            else:
                return email

tenatre_opts=[
    ('12','12f Months'),
    ('36','36 Months'),
    ('48','48 Months'),
    ('60','60 Months'),
]
class UsersTenatureForm(forms.ModelForm):
    loanid=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','aria-label':'loanid'}),error_messages={'required':'Loan id is required'})
    tenature=forms.ChoiceField(choices=tenatre_opts,widget=forms.RadioSelect(attrs={'aria-required':'true','class':'form-control','aria-label':'tenature'}),error_messages={'required':'Tenature  is required'})
    emi=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','aria-label':'emi'}),error_messages={'required':'EMI is required'})

    class Meta:
        model=LoanModel
        fields=['tenature','emi']
    def clean(self):
        cleaned_data=super().clean()
        loanid=cleaned_data.get('loanid')
        url=cleaned_data.get('url')
        if LoanModel.objects.filter(loanid=loanid).exists():
            data=LoanModel.objects.filter(loanid=loanid).last()
            if data.has_applied:
                link=''
                page_no=int(data.page)
                if page_no > 5:
                    if page_no == 6:
                        link="/check/eligibility/step3/"+data.loanid
                    else:
                        link="/finish/"+data.loanid
                    self.add_error('tenature','Sorry your application is still active. Click <a href="'+link+'">here</a> to continue.')
            else:
                return email