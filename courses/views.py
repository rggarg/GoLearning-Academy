from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from authentication.models import CustomUser
from courses.models import Course, CourseRequest, Video, Payment, UserCourse, DoubtQuestion, DoubtAnswer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from codeWithRG.settings import *
from time import time
import razorpay
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.http import JsonResponse
from django.core import serializers


client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


def home(request):
    user = request.user
    user_details = None
    try:
        user_details = CustomUser.objects.get(user=user)
        print(user_details.organization)
    except:
        pass
    courses = Course.objects.filter(active=True)
    user_courses = []
    if user.is_authenticated:
        print(user)
        uc = UserCourse.objects.filter(user=request.user, is_active=True)
        print('uvc', uc)
        for i in range(len(uc)):
            a = str(uc[i]).split('-')
            user_courses.append(a[1].strip())
    print(user_courses)
    context = {
        'courses': courses,
        'user_details': user_details,
        'user': user,
        'user_courses': user_courses
    }
    if request.method == "GET":
        return render(request, 'courses/home.html', context=context)
    if request.method == "POST":
        data = request.POST
        print(data)
        roll_no = request.POST['roll']
        name = request.POST['name']
        organization = request.POST['organization']
        if user and roll_no and name and organization:
            customuser = CustomUser()
            customuser.user = user
            customuser.roll_no = roll_no
            customuser.name = name
            customuser.organization = organization
            customuser.save()
        return render(request, 'courses/home.html', context=context)


def coursePage(request, slug):
    course = Course.objects.get(slug=slug)
    active_course = None
    try:
        active_course = UserCourse.objects.filter(
            user=request.user, course=course, is_active=True)
    except:
        pass
    active = False
    if active_course:
        active = True
    print(active)
    serial_number = request.GET.get('lecture')
    videos = course.video_set.all().order_by('serial_number')
    if serial_number is None:
        serial_number = 1
    video = Video.objects.get(serial_number=serial_number, course=course)
    questions = DoubtQuestion.objects.filter(course=course)
    answers = DoubtAnswer.objects.filter(course=course)
    abuse_words = ['fuck', 'fuckyou', 'shit', 'piss', 'dick ahead', 'asshole', 'bitch', 'bastard', 'damm',
                   'bugger', 'bloody', 'rubbish', 'dumb', 'stupid', 'idiot', 'fool', 'loser', 'creepy', 'hell', 'kiss', ]

    context = {'course': course, 'video': video,
               'videos': videos, 'slug': slug, 'questions': questions, 'answers': answers, 'active_course': active}

    if request.method == 'GET':
        if(video.is_preview is False):
            if(request.user.is_authenticated is False):
                return redirect('login')
            else:
                user = request.user
                try:
                    user_course = UserCourse.objects.get(
                        user=user, course=course)
                except:
                    return redirect('checkout', slug=course.slug)
        return render(request, template_name='courses/course_page.html', context=context)
    if request.method == "POST":
        doubt_question = request.POST.get('doubt_question')
        doubt_answer = request.POST.get('doubt_answer')
        dbans = DoubtAnswer.objects.filter(answer=doubt_answer)
        dbques = DoubtQuestion.objects.filter(question=doubt_question)

        if doubt_question and not dbques:
            for word in abuse_words:
                if word in doubt_question:
                    messages.error(
                        request, 'Sorry you are not allowed to ask this!!')
                    return render(request, template_name='courses/course_page.html', context=context)
            dq = DoubtQuestion()
            dq.user = request.user
            dq.course = course
            dq.question = doubt_question
            dq.save()
        elif doubt_answer and not dbans:
            for word in abuse_words:
                if word in doubt_answer:
                    messages.error(
                        request, 'Sorry you are not allowed to submit this!!')
                    return render(request, template_name='courses/course_page.html', context=context)
            doubt_aq = request.POST.get('doubt_aq')
            ques = DoubtQuestion.objects.get(pk=doubt_aq)
            da = DoubtAnswer()
            da.user = request.user
            da.course = course
            da.answer = doubt_answer
            da.question = ques
            da.save()
            value = ''
            context['value'] = value
        return render(request, template_name='courses/course_page.html', context=context)


def get_answers(request, id):
    ques = DoubtQuestion.objects.get(pk=id)
    ans = DoubtAnswer.objects.filter(question=ques)
    answers = serializers.serialize('json', ans)
    return JsonResponse({"answers": answers})

    # return answers


def checkout(request, slug):
    course = Course.objects.get(slug=slug)
    user = None
    user_details = None
    if (request.user.is_authenticated is False):
        return redirect('login')
    user = request.user
    courserequest = CourseRequest.objects.filter(
        user=user.username).filter(course=course.name)
    if courserequest:
        messages.info(
            request, 'Your request already sent.Please wait for response of teacher')
        return redirect('home')
    try:
        user_details = CustomUser.objects.get(user=user)
    except:
        print('user details dont exist.Please set them first')
    if user_details is None:
        messages.error(request, 'Please fill the details first in profile ')
        return redirect('home')

    if user_details:
        if user and course:
            uc = UserCourse.objects.filter(user=user, course=course)
            if not uc:
                usercourse = UserCourse()
                usercourse.user = user
                usercourse.course = course
                usercourse.is_active = False
                usercourse.save()
                courserequest = CourseRequest()
                courserequest.user = user.username
                courserequest.course = course.name
                courserequest.name = user_details.name
                courserequest.roll_no = user_details.roll_no
                courserequest.email = user.email
                courserequest.organization = user_details.organization
                courserequest.save()
        messages.success(
            request, 'Your enrollment request sent.Please wait for teacher response')
    return redirect('home')


# def checkout(request, slug):
#     course = Course.objects.get(slug=slug)
#     user = None
#     if(request.user.is_authenticated is False):
#         return redirect('login')
#     user = request.user
#     action = request.GET.get('action')
#     order = None
#     payment = None
#     error = None
#     if(action == 'create_payment'):
#         try:
#             user_course = UserCourse.objects.get(user=user, course=course)
#             error = 'You are already enrolled in this course'
#         except:
#             pass

#         if(error is None):
#             amount = (int(course.price - (course.price*course.discount*0.01)))*100
#             currency = 'INR'
#             notes = {
#                 'email': user.email,
#                 'name': f'{user.first_name} {user.last_name}'
#             }
#             receipt = f'codeWithRG-{int(time())}'

#             order = client.order.create(
#                 {
#                     'amount': amount,
#                     'currency': currency,
#                     'receipt': receipt,
#                     'notes': notes
#                 }
#             )
#             payment = Payment()
#             payment.user = user
#             payment.course = course
#             payment.order_id = order.get('id')
#             payment.save()

#     context = {'course': course, 'order': order,
#                'payment': payment, 'user': user, 'error': error}
#     return render(request, template_name='courses/check_out.html', context=context)


# @csrf_exempt
# def verifyPayment(request):
#     if(request.method == 'POST'):
#         data = request.POST
#         try:
#             client.utility.verify_payment_signature(data)
#             print(data)
#             razorpay_order_id = data['razorpay_order_id']
#             razorpay_payment_id = data['razorpay_payment_id']
#             payment = Payment.objects.get(order_id=razorpay_order_id)
#             payment.payment_id = razorpay_payment_id
#             payment.status = True
#             userCourse = UserCourse(user=payment.user, course=payment.course)
#             userCourse.save()
#             payment.user_course = userCourse
#             payment.save()
#             return redirect('my_courses')
#         except:
#             return HttpResponse('invalid payment details')


@login_required(login_url='login')
def my_courses(request):
    user = request.user
    user_courses = UserCourse.objects.filter(user=user, is_active=True)
    context = {
        'user_course': user_courses
    }
    return render(request, 'courses/my_courses.html', context=context)


def add_course(request):
    if(request.method == 'GET'):
        return render(request, 'courses/add_course.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        length = request.POST.get('length')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        thumbnail = request.FILES.get('thumbnail')
        resource = request.FILES.get('file')
        resThumbnail = cloudinary.uploader.upload(thumbnail)
        thumbnail_url = resThumbnail['url']
        resResource = cloudinary.uploader.upload(resource)
        resource_url = resResource['url']
        course = Course()
        course.owner = request.user
        course.name = name
        course.slug = slug
        course.description = description
        course.length = length
        course.price = price
        course.discount = discount
        course.thumbnail = thumbnail_url
        course.resource = resource_url
        course.save()
        return render(request, 'courses/add_course.html')
