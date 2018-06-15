from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.
#个人信息类
class UserInfo(AbstractUser):#继承抽象类，数据库不生成对应字段
    nick_name =models.CharField(max_length=50,verbose_name=u'昵称')
    birthday=models.DateField(verbose_name=u'生日',null=True)
    gender=models.CharField(max_length=50,choices=(('male',u'男'),('female',u'女')),default='female')
    image=models.ImageField(upload_to='image/%Y/%m',default=u'',max_length=100)
    phone=models.TextField(null=True,blank=True,verbose_name=u'手机号码',max_length=11)
    qq=models.TextField(null=True,blank=True,verbose_name=u'qq')
    summary=models.CharField(max_length=100,verbose_name=u'用户简介',null=True,blank=True)

    class Meta:
        verbose_name=u'用户信息'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.username

#首页 轮播图
class Banner(models.Model):
    name=models.CharField(max_length=30,verbose_name=u'轮播图名')
    image=models.ImageField(upload_to='image/%Y/%m',default=u'',max_length=100)
    url=models.URLField(max_length=254,verbose_name=u'访问地址')
    index=models.IntegerField(default=0,verbose_name=u'索引顺序')
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'轮播图'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

#注册及找回密码
class EmailVerify(models.Model):
    chack_code=models.CharField(max_length=20,verbose_name=u'验证码')
    email=models.EmailField(max_length=25,verbose_name=u'邮箱')
    send_type=models.CharField(max_length=10,choices=(('register',u'注册'),('reset',u'找回密码')),verbose_name=u'类型')
    send_time=models.DateTimeField(default=datetime.now,verbose_name=u'发送时间')

    class Meta:
        verbose_name=u'轮播图'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.email