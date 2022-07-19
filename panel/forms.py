
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
import re
from urllib.parse import urlparse
from manager.models import ExtendedAuthUser
from manager.models import RequestModel,ContactModel,LoanModel,CardModel

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


class SiteForm(forms.ModelForm):
    site_name=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Site name'}),error_messages={'required':'Site Name is required'})
    description=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Site Description'}),error_messages={'required':'Site Description is required'})
    theme_color=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Site Theme Color eg #ff0000'}),required=False)
    key_words=forms.CharField(widget=forms.TextInput(attrs={'data-role':'tagsinput','class':'bs-input','placeholder':'Site Keywords'}),required=False)
    site_url=forms.URLField(widget=forms.URLInput(attrs={'class':'form-control','placeholder':'Site URL'}),error_messages={'required':'Site URL is required'})
    favicon=forms.ImageField(
                                widget=forms.FileInput(attrs={'class':'custom-file-input','id':'customFileInput','accept':'image/*','hidden':True}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','ico'],message="Invalid image extension",code="invalid_extension")]
                                )
    class Meta:
        model=SiteConstants
        fields=['site_name','theme_color','site_url','description','key_words','favicon',]
    
            
    def clean_theme_color(self):
        theme_color=self.cleaned_data['theme_color']
        match=re.search(r'^#(?:[0-9a-fA-F]{1,2}){3}$',theme_color)
        if not match:
            raise forms.ValidationError('Invalid color code given')
        else:
            return theme_color
            
    def clean_site_url(self):
        site_url=self.cleaned_data['site_url']
        if URLValidator(site_url):
            return site_url
        else:
            raise forms.ValidationError('Invalid url')

#AddressConfigForm
class AddressConfigForm(forms.ModelForm):
    site_email=forms.EmailField(widget=forms.EmailInput(attrs={'style':'text-transform:lowercase;','class':'form-control','placeholder':'Site Email Address'}),error_messages={'required':'Address is required'})
    site_email2=forms.EmailField(widget=forms.EmailInput(attrs={'style':'text-transform:lowercase;','class':'form-control','placeholder':'Site Additional Email Address'}),required=False)
    address=forms.CharField(widget=forms.TextInput(attrs={'style':'text-transform:lowercase;','class':'form-control'}),error_messages={'required':'Address is required'})
    location=forms.CharField(widget=forms.TextInput(attrs={'style':'text-transform:lowercase;','class':'form-control'}),error_messages={'required':'Location is required'})
    phone=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'style':'text-transform:lowercase;','class':'form-control'},initial='KE'),required=False)
    class Meta:
        model=SiteConstants
        fields=['address','location','phone','site_email','site_email2']
    
    def clean_site_email(self):
        email=self.cleaned_data['site_email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        try:
            validate_email(email)
        except ValidationError as e:
            raise forms.ValidationError('Invalid email address.')
        return email
    
    def clean_site_email2(self):
        email=self.cleaned_data['site_email2']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        try:
            validate_email(email)
        except ValidationError as e:
            raise forms.ValidationError('Invalid email address.')
        return email


#social form
class UserSocialForm(forms.ModelForm):
    facebook=forms.URLField(widget=forms.URLInput(attrs={'style':'text-transform:lowercase;','class':'form-control','placeholder':'Facebook Link'}),required=False)    
    twitter=forms.URLField(widget=forms.URLInput(attrs={'style':'text-transform:lowercase;','class':'form-control','placeholder':'Twitter Link'}),required=False)    
    github=forms.URLField(widget=forms.URLInput(attrs={'style':'text-transform:lowercase;','class':'form-control','placeholder':'Github Link'}),required=False)  
    instagram=forms.URLField(widget=forms.URLInput(attrs={'style':'text-transform:lowercase;','class':'form-control','placeholder':'Instagram Link'}),required=False)    
    linkedin=forms.URLField(widget=forms.URLInput(attrs={'style':'text-transform:lowercase;','class':'form-control','placeholder':'Linkedin Link'}),required=False)   
    youtube=forms.URLField(widget=forms.URLInput(attrs={'style':'text-transform:lowercase;','class':'form-control','placeholder':'Youtube Link'}),required=False)    
    whatsapp=forms.URLField(widget=forms.URLInput(attrs={'style':'text-transform:lowercase;','class':'form-control','placeholder':'Whats App'}),required=False)
    class Meta:
        model=SiteConstants
        fields=['facebook','twitter','linkedin','instagram','whatsapp','youtube','github',]

    def clean_facebook(self):
        facebook=self.cleaned_data['facebook']
        if URLValidator(facebook):
                output=urlparse(facebook)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Username parameter missing')
                else:
                    return [facebook,username]
        else:
            raise forms.ValidationError('Invalid url')
    
    def clean_twitter(self):
        twitter=self.cleaned_data['twitter']
        if URLValidator(twitter):
                output=urlparse(twitter)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Username parameter missing')
                else:
                    return [twitter,username]
        else:
            raise forms.ValidationError('Invalid url')
    

    def clean_github(self):
        github=self.cleaned_data['github']
        if URLValidator(github):
                output=urlparse(github)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Username parameter missing')
                else:
                    return [github,username]
        else:
            raise forms.ValidationError('Invalid url')
    def clean_instagram(self):
        instagram=self.cleaned_data['instagram']
        if URLValidator(instagram):
                output=urlparse(instagram)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Username parameter missing')
                else:
                    return [instagram,username]
        else:
            raise forms.ValidationError('Invalid url')
    
    def clean_linkedin(self):
        linkedin=self.cleaned_data['linkedin']
        if URLValidator(linkedin):
                output=urlparse(linkedin)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Username parameter missing')
                else:
                    return [linkedin,username]
        else:
            raise forms.ValidationError('Invalid url')
    
    def clean_youtube(self):
        youtube=self.cleaned_data['youtube']
        if URLValidator(youtube):
                output=urlparse(youtube)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Channel id parameter missing')
                else:
                    return [youtube,username]
        else:
            raise forms.ValidationError('Invalid url')
    def clean_whatsapp(self):
        whatsapp=self.cleaned_data['whatsapp']
        if URLValidator(whatsapp):
            output=urlparse(whatsapp)
            username=output.path.strip('/')
            if not username:
                raise forms.ValidationError('username parameter missing')
            else:
                return [whatsapp,username]
        else:
            raise forms.ValidationError('Invalid url')

#WorkingConfigForm
class WorkingConfigForm(forms.ModelForm):
    working_days=forms.CharField(widget=forms.TextInput(attrs={'style':'text-transform:lowercase;','class':'form-control'}),error_messages={'required':'Working days is required'})
    working_hours=forms.CharField(widget=forms.TextInput(attrs={'style':'text-transform:lowercase;','class':'form-control'}),error_messages={'required':'Working hours is required'})

    class Meta:
        model=SiteConstants
        fields=['working_days','working_hours',]


class users_registerForm(UserCreationForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First name','aria-label':'first_name'}),error_messages={'required':'First name is required'})
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last name','aria-label':'last_name'}),error_messages={'required':'Last name is required'})
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email address','aria-label':'email'}),error_messages={'required':'Email address is required'})
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username ','aria-label':'username'}),error_messages={'required':'Username is required'})
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password Eg Example12','aria-label':'password1'}),error_messages={'required':'Password is required','min_length':'enter atleast 6 characters long'})
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm password','aria-label':'password2'}),error_messages={'required':'Confirm password is required'})

    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password1','password2']


    def clean_first_name(self):
        first_name=self.cleaned_data['first_name']
        if not str(first_name).isalpha():
                raise forms.ValidationError('only characters are allowed')
        return first_name
    
    def clean_last_name(self):
        last_name=self.cleaned_data['last_name']
        if not str(last_name).isalpha():
                raise forms.ValidationError('only characters are allowed')
        return last_name
           

    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists')
        try:
            validate_email(email)
        except ValidationError as e:
            raise forms.ValidationError('invalid email address')
        return email
    
    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('A user with this username already exists')
        return username


class EProfileForm(forms.ModelForm):
    phone=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class':'form-control','type':'tel','aria-label':'phone','placeholder':'Phone'}),error_messages={'required':'Phone number is required'})
    role=forms.ChoiceField(required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Role'}))
    profile_pic=forms.ImageField(
                                widget=forms.FileInput(attrs={'class':'profile','accept':'image/*','hidden':True}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','gif'],message="Invalid image extension",code="invalid_extension")]
                                )
    class Meta:
        model=ExtendedAuthUser
        fields=['phone','role','profile_pic']

    
    def clean_phone(self):
        phone=self.cleaned_data['phone']
        if phone !='':
            if ExtendedAuthUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('A user with this phone number already exists.')
            else:
                return phone
        else:
            raise forms.ValidationError('Phone number is required')

class CurrentUserProfileChangeForm(UserChangeForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'style':'text-transform:lowercase;','class':'form-control'}),required=False)
    last_name=forms.CharField(widget=forms.TextInput(attrs={'style':'text-transform:lowercase;','class':'form-control','aria-label':'last_name'}),error_messages={'required':'Last name is required'})
    username=forms.CharField(widget=forms.TextInput(attrs={'style':'text-transform:lowercase;','class':'form-control','aria-label':'username'}),error_messages={'required':'Username is required'})
    email=forms.EmailField(widget=forms.EmailInput(attrs={'style':'text-transform:lowercase;','class':'form-control','aria-label':'email'}),error_messages={'required':'Email address is required'})
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
        else:
           return username

user_roles=[
        ('Admin','Admin'),
        ('Employee','Employee'),
        ('Other','Other'),
    ]
class CurrentExtendedUserProfileChangeForm(forms.ModelForm):
    phone=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class':'form-control','type':'tel','aria-label':'phone','placeholder':'Phone example +25479626...'}),error_messages={'required':'Phone number is required'})
    role=forms.ChoiceField(choices=user_roles, error_messages={'required':'Role is required','aria-label':'role'},widget=forms.Select(attrs={'class':'form-control','placeholder':'Role'}))
    profile_pic=forms.ImageField(
                                widget=forms.FileInput(attrs={'class':'profile','accept':'image/*','hidden':True}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','gif'],message="Invalid image extension",code="invalid_extension")]
                                )
    class Meta:
        model=ExtendedAuthUser
        fields=['phone','profile_pic','role',]

    
    def clean_phone(self):
        phone=self.cleaned_data['phone']
        if phone != self.instance.phone:
            if ExtendedAuthUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('A user with this phone number already exists.')
            else:
                return phone
        else:
           return phone 


class CurrentUserProfileChangeForm1(UserChangeForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'style':'text-transform:lowercase;','class':'form-control'}),required=False)
    last_name=forms.CharField(widget=forms.TextInput(attrs={'style':'text-transform:lowercase;','class':'form-control','aria-label':'last_name'}),error_messages={'required':'Last name is required'})
    username=forms.CharField(widget=forms.TextInput(attrs={'style':'text-transform:lowercase;','class':'form-control','aria-label':'username','readonly':True}),error_messages={'required':'Username is required'})
    email=forms.EmailField(widget=forms.EmailInput(attrs={'style':'text-transform:lowercase;','class':'form-control','aria-label':'email'}),error_messages={'required':'Email address is required'})
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
        else:
           return username

user_roles=[
        ('Admin','Admin'),
        ('Employee','Employee'),
        ('Other','Other'),
    ]
class CurrentExtendedUserProfileChangeForm1(forms.ModelForm):
    phone=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class':'form-control','type':'tel','aria-label':'phone','placeholder':'Phone example +25479626...'}),error_messages={'required':'Phone number is required'})
    profile_pic=forms.ImageField(
                                widget=forms.FileInput(attrs={'class':'profile','accept':'image/*','hidden':True}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','gif'],message="Invalid image extension",code="invalid_extension")]
                                )
    class Meta:
        model=ExtendedAuthUser
        fields=['phone','profile_pic',]

    
    def clean_phone(self):
        phone=self.cleaned_data['phone']
        if phone != self.instance.phone:
            if ExtendedAuthUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('A user with this phone number already exists.')
            else:
                return phone
        else:
           return phone 


class UserPasswordChangeForm(UserCreationForm):
    oldpassword=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Old password','aria-label':'oldpassword'}),error_messages={'required':'Old password is required','min_length':'enter atleast 6 characters long'})
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'New password Eg Example12','aria-label':'password1'}),error_messages={'required':'New password is required','min_length':'enter atleast 6 characters long'})
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm new password','aria-label':'password2'}),error_messages={'required':'Confirm new password is required'})

    class Meta:
        model=User
        fields=['password1','password2']
    
    def clean_oldpassword(self):
        oldpassword=self.cleaned_data['oldpassword']
        if not self.instance.check_password(oldpassword):
            raise forms.ValidationError('Wrong old password.')
        else:
           return oldpassword 

#profileForm
class ProfilePicChangeForm(forms.ModelForm):
    profile_pic=forms.ImageField(
                                widget=forms.FileInput(attrs={'class':'profile','accept':'image/*','hidden':True}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','gif'],message="Invalid image extension",code="invalid_extension")]
                                )
    class Meta:
        model=ExtendedAuthUser
        fields=['profile_pic',]


#query form
class UsersQueryForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter name','aria-label':'name','readonly':True}),error_messages={'required':'Name is required'})
    user=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter category','aria-label':'category','readonly':True}),error_messages={'required':'category is required'})
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter email address','aria-label':'email','readonly':True}),error_messages={'required':'Email address is required'})
    query=forms.CharField(min_length=10,widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Post your query today','rows':6,'aria-label':'query'}),error_messages={'required':'Query is required','min_length':'enter atleast 10 characters long message'})
    answer=forms.CharField(min_length=10,widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Answer...','rows':6,'aria-label':'answer'}),error_messages={'required':'Answer is required'})
    class Meta:
        model=RequestModel
        fields=['name','user','email','query','answer',]

    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            validate_email(email)
        except ValidationError as e:
            raise forms.ValidationError('invalid email address')
        return email
           

#UsersReplyForm
class UsersReplyForm(forms.ModelForm):
    reply=forms.CharField(min_length=10,widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Reply to this message','rows':6,'aria-label':'reply'}),error_messages={'required':'Feedback is required'})
    class Meta:
        model=ContactModel
        fields=['reply',]

class CardConfigForm(forms.ModelForm):
    card_type=forms.ChoiceField(choices=[('prime membership','Prime membership'),('elite membership','Elie membership')],widget=forms.Select(attrs={'class':'form-control','aria-label':'card_type'}),error_messages={'required':'Card type is required'})
    loan_type=forms.ChoiceField(choices=[('personal loan','Personal loan'),('business loan','Bussiness loan')],widget=forms.Select(attrs={'class':'form-control','aria-label':'loan_type'}),error_messages={'required':'Loan type is required'})
    interest=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Interest p.a','aria-label':'interest'}),error_messages={'required':'Interest value  is required'})
    start_date=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Start date','aria-label':'start_date'}),error_messages={'required':'Start date  is required'})
    end_date=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'End date','aria-label':'end_date'}),error_messages={'required':'End date  is required'})
    prev_price=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Previous price','aria-label':'prev_price'}),error_messages={'required':'Previous price  is required'})
    now_price=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Current price','aria-label':'now_price'}),error_messages={'required':'Current price  is required'})
    class Meta:
        model=CardModel
        fields=['card_type','interest','start_date','end_date','prev_price','now_price','loan_type',]

    def clean_loan_type(self):
        loan_type=self.cleaned_data.get('loan_type')
        if CardModel.objects.filter(loan_type__icontains=loan_type):
            raise forms.ValidationError('Loan type infomation already exists')
        else:
            return loan_type

    def clean_card_type(self):
        card_type=self.cleaned_data.get('card_type')
        if CardModel.objects.filter(card_type__icontains=card_type):
            raise forms.ValidationError('Card type infomation already exists')
        else:
            return card_type


class CardConfigEditForm(forms.ModelForm):
    card_type=forms.ChoiceField(choices=[('prime membership','Prime membership'),('elite membership','Elite membership')],widget=forms.Select(attrs={'class':'form-control','aria-label':'card_type'}),error_messages={'required':'Card type is required'})
    loan_type=forms.ChoiceField(choices=[('personal loan','Personal loan'),('bussiness loan','Bussiness loan')],widget=forms.Select(attrs={'class':'form-control','aria-label':'loan_type'}),error_messages={'required':'Loan type is required'})
    interest=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Interest p.a','aria-label':'interest'}),error_messages={'required':'Interest value  is required'})
    start_date=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Start date','aria-label':'start_date'}),error_messages={'required':'Start date  is required'})
    end_date=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'End date','aria-label':'end_date'}),error_messages={'required':'End date  is required'})
    prev_price=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Previous price','aria-label':'prev_price'}),error_messages={'required':'Previous price  is required'})
    now_price=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Current price','aria-label':'now_price'}),error_messages={'required':'Current price  is required'})
    class Meta:
        model=CardModel
        fields=['card_type','interest','start_date','end_date','prev_price','now_price','loan_type',]