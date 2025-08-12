from django import forms
class LoginForm(forms.Form):
    username=forms.CharField(label='Admin_name',widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))


# class Hosteller_loginForm(forms.Form):
#     usermail=forms.CharField(label='Hosteller_id(email)',widget=forms.TextInput(attrs={'class':'form-control'}))
#     password=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
