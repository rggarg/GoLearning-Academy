from django.shortcuts import render, redirect
from django.http import HttpResponse
from courses.models import Course, UserCourse, CourseRequest, Video
from quiz.models import QuizQuestion
from django.contrib.auth.models import User
import cloudinary
import cloudinary.uploader
import cloudinary.api
# Create your views here.


def dashboard(request):
    user = request.user
    courses = Course.objects.filter(owner=user)
    courserequests = []
    crs = None
    for course in courses:
        try:
            crs = CourseRequest.objects.filter(course=course.name)
        except Exception as e:
            print(e)

        if crs:
            for cr in crs:
                courserequest = []
                courserequest.append(cr.pk)
                courserequest.append(cr.name)
                courserequest.append(cr.email)
                courserequest.append(cr.roll_no)
                courserequest.append(cr.course)
                courserequest.append(cr.organization)
                courserequests.append(courserequest)
            crs = None
            # courserequest.clear()
    print(courserequests)
    quizes = QuizQuestion.objects.filter(user=user).order_by('course')
    user_courses = []
    for course in courses:
        uc = UserCourse.objects.filter(course=course)
        for i in range(len(uc)):
            a = str(uc[i]).split('-')
            user_courses.append(a)
    context = {
        'courses': courses,
        'user_courses': user_courses,
        'quizes': quizes,
        'course_requests': courserequests
    }
    return render(request, 'teacher/dashboard.html', context=context)


def quiz_details(request):
    user = request.user
    quizes = QuizQuestion.objects.filter(user=user).order_by('course')
    context = {
        'quizes': quizes
    }
    return render(request, 'teacher/quiz_details.html', context=context)


def course_details(request):
    user = request.user
    courses = Course.objects.filter(owner=user)
    context = {
        'courses': courses
    }
    return render(request, 'teacher/course_details.html', context=context)


def learner_details(request):
    user = request.user
    courses = Course.objects.filter(owner=user)
    user_courses = []
    for course in courses:
        uc = UserCourse.objects.filter(course=course)
        for i in range(len(uc)):
            a = str(uc[i]).split('-')
            user_courses.append(a)
    context = {
        'user_courses': user_courses
    }
    return render(request, 'teacher/learner_details.html', context=context)


def allow_user(request, id):
    print('id', id)
    cr = CourseRequest.objects.get(pk=id)
    user = User.objects.get(email=cr.email)
    course = Course.objects.get(name=cr.course)
    user_course = UserCourse.objects.get(user=user, course=course)
    user_course.is_active = True
    user_course.save()
    cr.delete()

    return redirect('dashboard')


def add_video(request, slug):
    course = Course.objects.get(slug=slug)
    video_count = Video.objects.filter(course=course).count()
    if request.method == 'POST':
        title = request.POST.get('title')
        serial_no = request.POST.get('serial_no')
        video = request.FILES.get('video')
        preview = request.POST.get('preview')
        if preview == 'preview':
            is_preview = True
        else:
            is_preview = False
        resVideo = cloudinary.uploader.upload(video, resource_type='video')
        video_url = resVideo['url']
        if title and serial_no and video:
            v = Video()
            v.course = course
            v.title = title
            v.video_id = video_url
            v.serial_number = serial_no
            v.is_preview = is_preview
            v.save()
            video_count = Video.objects.filter(course=course).count()
            print(video_count)
            if video_count >= 1:
                course.active = True
                course.save(update_fields=['active'])
        print('title', title, 'serial_no', serial_no,
              'video', video_url, 'preview', preview)
    context = {
        'course': course,
        'video_count': video_count + 1
    }
    return render(request, 'courses/add_video.html', context=context)
