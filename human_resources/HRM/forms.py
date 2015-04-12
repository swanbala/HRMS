from django import forms

# the form of login
class LoginForm(forms.Form):
    username = forms.IntegerField()
    password = forms.CharField()
    
    
class change_passwd_Form(forms.Form):
    old_passwd=forms.CharField()
    new_passwd=forms.CharField()
    
class bonusFrom(forms.Form):
    id=forms.IntegerField()
    bonus=forms.IntegerField()
    
class timeForm(forms.Form):
    level=forms.IntegerField()
    mor_in=forms.TimeField()
    
class deleteForm(forms.Form):
    id=forms.IntegerField()
    
class changeForm(forms.Form):
    name=forms.CharField()
    mail=forms.EmailField()
    tel=forms.IntegerField()
    password=forms.CharField()