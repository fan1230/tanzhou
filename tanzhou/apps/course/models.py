from django.db import models
from datetime import datetime
from users.models import UserInfo
# Create your models here.
#课程大类 第一分类
class CourseClass(models.Model):
    name=models.CharField(choices=(('it',u'IT互联网'),('language',u'语言留学'),('design',u'设计'),('life',u'生活兴趣'),
                                   ('plant',u'生产种植'),('edu',u'升学考研'),('certificate',u'公培考证')),
                          max_length=15,verbose_name=u'分类')

    class Meta:
        verbose_name=u'第一分类'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

#第二分类
class CourseSort(models.Model):
    classes=models.ForeignKey(CourseClass,verbose_name=u'第一分类')
    name=models.CharField(max_length=50,verbose_name=u'第二分类')

    class Meta:
        verbose_name=u'第二分类'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

class Course(models.Model):
    sort=models.ForeignKey(CourseSort,verbose_name=u'分类')
    name=models.CharField(max_length=30,verbose_name=u'课程名称')
    price=models.IntegerField(max_length=10,verbose_name=u'价格')
    learn_time=models.CharField(max_length=6,verbose_name=u'学习时长')
    nums=models.IntegerField(default=0,verbose_name=u'购买人数')
    image=models.ImageField(upload_to='img/%Y/%m',verbose_name=u'封面图',null=True)
    describe=models.ImageField(upload_to='img/course/%Y/%m',verbose_name=u'描述',null=True)
    click_num=models.IntegerField(default=0,verbose_name=u'点击人数')

    class Meta:
        verbose_name=u'课程'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

class Chapter(models.Model):
    chapter_course=models.ForeignKey(Course,verbose_name=u'课程',related_name=u'课程')
    name=models.CharField(max_length=10,verbose_name=u'课程名')
    time=models.DateTimeField(default=datetime.now,verbose_name=u'课程时间')

    class Meta:
        verbose_name=u'章节'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

class Teacher(models.Model):
    teacher_course=models.ForeignKey(Course,verbose_name=u'课程')
    teacher_name=models.CharField(max_length=30,verbose_name=u'老师名')
    teacher_des=models.CharField(max_length=100,verbose_name=u'老师描述')
    teacher_img=models.ImageField(upload_to='img/%Y/%m',verbose_name=u'老师图')

    class Meta:
        verbose_name=u'老师'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.teacher_name


class Buy(models.Model):
    user=models.ForeignKey(UserInfo,verbose_name=u'用户')
    course=models.ForeignKey(Course,verbose_name=u'课程')
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'购买时间')

