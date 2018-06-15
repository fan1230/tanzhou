from django.contrib import admin
from course.models import Course,CourseClass,CourseSort,Chapter,Teacher

# Register your models here.

class CourseClassAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    class Meta:
        verbose_name=u'第一分类'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class CourseSortAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    class Meta:
        verbose_name=u'第二分类'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class CourseAdmin(admin.ModelAdmin):#superuser fan qwe123123
    list_display =['name','price','learn_time','nums']#显示字段
    list_filter = ['name','price','learn_time','nums']
    search_fields = ['name','price','learn_time','nums']

    class Meta:
        verbose_name=u'课程'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

class ChapterAdmin(admin.ModelAdmin):
    list_display = ['name','chapter_course','time']
    list_filter = ['name','chapter_course']
    search_fields = ['name','chapter_course']
    class Meta:
        verbose_name=u'章节'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher_course','teacher_name','teacher_des']
    list_filter = ['teacher_course','teacher_name','teacher_des']
    search_fields = ['teacher_course','teacher_name','teacher_des']
    class Meta:
        verbose_name=u'老师'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name



admin.site.register(CourseClass,CourseClassAdmin)
admin.site.register(CourseSort,CourseSortAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Chapter,ChapterAdmin)
admin.site.register(Teacher,TeacherAdmin)

#第二种注册方法
# @admin.register(Course) #推荐使用此方法
# class CourseAdmin(admin.ModelAdmin):#superuser fan qwe123123
#     list_display =['name','price','learn_time','nums']#显示字段
#     list_filter = ['name','price','learn_time','nums']
#     search_fields = ['name','price','learn_time','nums']
#
#     class Meta:
#         verbose_name=u'课程'
#         verbose_name_plural=verbose_name
#
#     def __str__(self):
#         return self.name