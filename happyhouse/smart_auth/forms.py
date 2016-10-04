#encoding=utf-8
from django import forms
from django.contrib.auth.models import User as DjangoUser, Group, Permission

    
    
class UserChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=32)
    new_password = forms.CharField(max_length=32)
    new_password1 = forms.CharField(max_length=32)
    

class GroupPermissionUpdateForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects)
    permission = forms.ModelChoiceField(queryset=Permission.objects)
    
    
class GroupUserUpdateForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects)
    user = forms.ModelChoiceField(queryset=DjangoUser.objects)
    