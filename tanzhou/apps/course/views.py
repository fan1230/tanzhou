from django.shortcuts import render
from django.views import View
from .models import CourseClass,CourseSort,Course,Teacher,Chapter
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.

class CourseList(View):
    def get(self,request):
        #取出第一分类
        course_class=CourseClass.objects.all()
        course_sort=CourseSort.objects.all()
        all_course=Course.objects.all()

        #取出热门课程
        hot_course=all_course.order_by('-click_num')[:3]

        #取出第一分类的id
        class_id=request.GET.get('class_id','')
        if class_id:
            course_class=course_class.filter(id=int(class_id))#一级筛选 --->1,2
            course_sort=course_sort.filter(classes_id=int(class_id))
            all_course=all_course.filter(sort__classes_id=int(class_id))

        #取出第二分类的id
        sort_id=request.GET.get('sort_id','')
        if sort_id:
            all_course=Course.objects.filter(sort_id=int(sort_id))

        price=request.GET.get('price','')
        if price:
            if price=='0':
                all_course=all_course.filter(price=0)
            else:
                all_course=all_course.filter(price__gt=0)

        #分页操作
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        #obj-->all_course  3-->分页显示数值
        p=Paginator(all_course,6,request=request)
        all_course=p.page(page)#--->筛选后的course 前端要取全部course 用all_course.object_list

        # all_course=Course.objects.all()
        # return render(request,'course_list.html',{'course_class':course_class,
        #                                           'course_sort':course_sort,
        #                                           'all_course':all_course,
        #                                           })
        # for course in all_course.object_list:
        #     print(course.price,type(course.price))

        return render(request,'course_list.html',{"course_class": course_class,
                                                   "course_sort": course_sort,
                                                   "all_course": all_course,
                                                   "sort_id": sort_id,
                                                   "class_id": class_id,
                                                   "hot_course": hot_course,
                                                   "price": price,})






    # p=Paginator(all_course,1,request=request)
    # all_course=p.page(page)

class CourseDetailView(View):
    def get(self,request,course_id):
        course=Course.objects.get(id=int(course_id))
        #点击次数统计
        course.click_num+=1
        course.save()

        teacher=Teacher.objects.get(teacher_course_id=int(course_id))
        if teacher:
            return render(request,'course_detail.html',{'course':course,
                                                    'teacher':teacher})
        else:
            return render(request,'course_detail.html',{'course':course,})

class LessonDetailView(View):
    def get(self,request,course_id):
        if course_id:
            course=Course.objects.filter(id=int(course_id))[0]#转为字符串,保存值
            lessons=Chapter.objects.filter(chapter_course_id=course_id)
            teacher=Teacher.objects.filter(teacher_course_id=course_id)[0]
            return render(request,'course_lesson.html',locals())


