"""tanzhou URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from users.views import IndexView,LoginView,LogoutView,RegisterView,ActiveUserView,ResetView,ForgetPwdView,ModifyPwdView
from django.views.static import serve
from tanzhou.settings import MEDIA_ROOT
urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^$',IndexView.as_view(),name='index'),
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^logout/$',LogoutView.as_view(),name='logout'),
    #验证码
    url(r'^captcha/', include('captcha.urls')),
    #注册
    url(r'^register/$',RegisterView.as_view(),name='register'),
    #激活页面
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name='active_code'),
    #找回密码
    url(r'^reset/(?P<reset_code>.*)/$',ResetView.as_view(),name='reset_pwd'),
    #修改密码
    url(r'^modify_pwd/$',ModifyPwdView.as_view(),name='modify_pwd'),
    #忘记密码
    url(r'^forget_pwd/$',ForgetPwdView.as_view(),name='forget_pwd'),
    #关于用户
    url(r'i/',include('users.urls',namespace='i')),
    #关于课程
    url(r'^course/',include('course.urls',namespace='course')),

    #配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$',serve,{'document_root':MEDIA_ROOT}),

]
