from django.shortcuts import render
from django.views import View
from .forms import LoginForm,RegisterForm,ForgetPwdForm,ModifyPwdForm,ChangePwdForm,UploadImageForm,UploadInfoForm
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from users.models import UserInfo
from django.db.models import Q#或操作
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from .models import EmailVerify
from utils.mixin_utils import LoginRequiredMixin   #重写LoginRequiredMixin
# from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user=UserInfo.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
#首页
class IndexView(View):
    def get(self,request):
        return render(request, 'index.html', {})

#登录页面
class LoginView(View):
    def get(self,request):
        return render(request,'login.html',{})

    def post(self,request):
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            user_name=request.POST.get('username')
            pass_word=request.POST.get('password')
            user=authenticate(username=user_name,password=pass_word)#数据验证
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('index'))#验证合法 跳转到首页
                else:
                    return render(request, 'login.html', {'msg': '用户未激活','username':user_name})
            else:
                return render(request, 'login.html', {'msg': '账号密码有误','username':user_name})
        return render(request, 'login.html', {'login_form':login_form})

#退出
class LogoutView(View):
    def get(self,request):
        logout(request)
        return render(request, 'index.html', {})

#注册
class RegisterView(View):
    def get(self,request):
        register_form=RegisterForm()
        return render(request,'register.html',{'register_form':register_form})

    def post(self,request):
        #获取前端数据
        register_form=RegisterForm(request.POST)
        if register_form.is_valid():
            #验证表单是否合法
            email=request.POST.get('email','')
            if UserInfo.objects.filter(email=email):
                return render(request,'register.html',{
                    'register_form':register_form,
                    'msg':'用户已经存在!'
                })
            password=request.POST.get('password','')

            #实例化UserProfile字段
            user_profile=UserInfo()
            user_profile.username=email
            user_profile.email=email
            user_profile.is_active=False
            user_profile.password=make_password(password)
            user_profile.save()
            #发送邮箱
            send_register_email(email,'register')
            return HttpResponseRedirect(reverse('login'))
        else:
            return render(request,'register.html',{'register_form':register_form})


#激活
class ActiveUserView(View):
    def get(self,request,active_code):
        all_records=EmailVerify.objects.filter(chack_code=active_code)
        if all_records:
            for record in all_records:
                email=record.email
                user=UserInfo.objects.get(email=email)
                user.is_active=True
                user.save()
                return render(request,'success_active.html')
            return render(request,'login.html')


#忘记密码
class ForgetPwdView(View):
    def get(self,request):
        forget_form=ForgetPwdForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form=ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email=request.POST.get('email','')
            if UserInfo.objects.filter(email=email):
                if forget_form.is_valid():
                    send_register_email(email,'forget')
                return render(request,'success_reset.html',{'email':email})
            return render(request,'forgetpwd.html',{'msg':u'用户不存在!!',
                                                    'forget_form': forget_form})#回填
        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})

#修改密码
class ResetView(View):
    def get(self,request,reset_code):
        all_records=EmailVerify.objects.filter(chack_code=reset_code)
        if all_records:
            for record in all_records:
                email=record.email
                return render(request,'password_reset.html',{'email':email})

#确认修改密码
class ModifyPwdView(View):
    def post(self,request):
        modify_form=ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get('password1')
            pwd2=request.POST.get('password2')
            email=request.POST.get('email')
            if pwd1 != pwd2:
                return render(request,'password_reset.html',{'email':email,
                                                             'msg':u'两次密码输入不一致!'})
            user=UserInfo.objects.get(email=email)
            user.password=make_password(pwd2)
            user.save()
            return render(request,'reset_success.html')
        else:
            email=request.POST.get('email')
            return render(request,'password_reset.html',{'email':email,'modify_form':modify_form})


#关于用户的信息
class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):
        page_name = 'info'
        return render(request,'my_info.html',{'page_name':page_name})

    def post(self,request):
        info_form=UploadInfoForm(request.POST,instance=request.user)
        if info_form.is_valid():
            info_form.save()
            return HttpResponseRedirect(reverse('i:info'))
        else:
            return render(request,'my_info.html',{'info_form':info_form})

# 关于用户密码修改
class ChangePwdView(LoginRequiredMixin,View):
    def get(self,request):
        email=request.user.email
        return render(request,'my_password.html',{'email':email})

    def post(self,request):
        change_form=ChangePwdForm(request.POST)
        email = request.user.email

        if change_form.is_valid():
            pwdold=request.POST.get('passwordold')
            email= request.POST.get('email','')
            user = authenticate(username=email, password=pwdold)
            if user is not None:
                pwd1=request.POST.get('password1')
                pwd2=request.POST.get('password2')
                if pwd1!=pwd2:
                    return render(request,'my_password.html',{'email':email,'msg':u'两次输入密码不一致!'})
                user=UserInfo.objects.get(email=email)
                user.password=make_password(pwd2)
                user.save()
                return render(request,'reset_success.html')
            else:
                return render(request,'my_password.html',{'email':email,'msg':u'旧密码不对'})
        return render(request,'my_password.html',{'change_form':change_form,'email':email})#数据回填

#用户修改头像
class UploadImageView(LoginRequiredMixin,View):
    # #常规方法
    # def post(self,request):
    #     #获取前端数据
    #     image_form=UploadImageForm(request.POST,request.FILES)
    #     if image_form.is_valid():
    #         image=image_form.cleaned_data['image']
    #         request.user.image=image
    #         request.user.save()
    #         return HttpResponseRedirect(reverse('i:info'))
    #     else:
    #         return render(request,'my_info.html',{'image_form':image_form})

    #直接实例化
    def post(self,request):
        image_form=UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponseRedirect(reverse('i:info'))
        else:
            return render(request,'my_info.html')

#用户订单
class UserOrderView(LoginRequiredMixin,View):
    def get(self,request):
        page_name='order'
        return render(request,'my_order.html',{'page_name':page_name})

#用户作业
class UserWorkView(LoginRequiredMixin,View):
    def get(self,request):
        page_name='homework'
        return render(request,'my_homework.html',{'page_name':page_name})

#用户课程
class UserCourseView(LoginRequiredMixin,View):
    def get(self,request):
        page_name='course'
        return render(request,'my_course.html',{'page_name':page_name})








