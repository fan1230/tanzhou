# -*- coding: utf-8 -*-
from django import forms
from captcha.fields import CaptchaField
from users.models import UserInfo

class LoginForm(forms.Form):
    username=forms.CharField(required=True)
    password=forms.CharField(required=True,min_length=6)

class RegisterForm(forms.Form):
    email=forms.EmailField(required=True)
    password=forms.CharField(required=True,min_length=6)
    captcha=CaptchaField(error_messages={'invalid':u'验证码错误'})

class ForgetPwdForm(forms.Form):
    email=forms.EmailField(required=True)
    captcha=CaptchaField(error_messages={'invalid':u'验证码错误'})

#修改密码验证字段
class ModifyPwdForm(forms.Form):
    email=forms.EmailField(required=True)
    password1=forms.CharField(required=True,min_length=6)
    password2=forms.CharField(required=True,min_length=6)


#在我的中心中修改密码的验证字段
class ChangePwdForm(forms.Form):
    email = forms.EmailField(required=True)
    passwordold = forms.CharField(required=True,min_length=6)
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)

#上传图片
class UploadImageForm(forms.ModelForm):
    class Meta:
        #使用UserInfo模型下的image字段来限制
        model=UserInfo
        fields=['image']

class UploadInfoForm(forms.ModelForm):
    class Meta:
        model=UserInfo
        fields=['nick_name','phone','gender','qq','email']
