from django import forms
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm , UsernameField , PasswordChangeForm , PasswordResetForm , SetPasswordForm
from django.contrib.auth.models import User
from . models import Customer

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
)
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm-Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','email','password1', 'password2']

class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].label = 'Old Password'
        self.fields['old_password'].widget = forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password','class':'form-control'})
        self.fields['new_password1'].label = 'New Password'
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'})
        self.fields['new_password2'].label = 'Confirm Password'
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'})

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].label = 'New Password'
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'})
        self.fields['new_password2'].label = 'Confirm Password'
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'})

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields=['name','locality', 'city','mobile','state','zipcode']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
        }
    