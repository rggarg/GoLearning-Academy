from django.shortcuts import render
from .models import QuizQuestion
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.contrib import messages
from courses.models import Course
# Create your views here.


def take_quiz(request, slug):
    course = Course.objects.get(slug=slug)
    questions = QuizQuestion.objects.filter(course=course)
    context = {
        'course': course,
        'questions': questions
    }
    if request.method == 'GET':
        return render(request, 'quiz/take_quiz.html', context=context)
    if request.method == 'POST':
        data = request.POST
        print(data)
        score = 0
        correct = 0
        wrong = 0
        total = len(questions)
        for q in questions:
            if q.answer == request.POST.get(q.question):
                score += 1
                correct += 1
            else:
                wrong += 1
        percentage = (score/total)*100
        response = {
            'score': score,
            'correct': correct,
            'wrong': wrong,
            'total': total,
            'percentage': percentage
        }
        return render(request, 'quiz/result.html', context=response)


def add_question(request, slug):
    user = request.user
    course = Course.objects.get(slug=slug)
    context = {
        'slug': slug,
        'course': course
    }
    if request.method == "GET":
        return render(request, 'quiz/add_question.html', context=context)
    if request.method == "POST":
        question = request.POST['question']
        option1 = request.POST['option1']
        option2 = request.POST['option2']
        option3 = request.POST['option3']
        option4 = request.POST['option4']
        check = request.POST['radio']
        answer = request.POST[check]
        image = request.FILES.get('image')
        if image:
            resimage = cloudinary.uploader.upload(image)
            image_url = resimage['url']

        if not question or not option1 or not option2 or not option3 or not option4:
            messages.error(
                request, 'Some issue!!!Please fill all fields')
            return render(request, 'quiz/add_question.html', context=context)
        if not check:
            messages.error(
                request, 'Some issue!!!Please select any one option')
            return render(request, 'quiz/add_question.html', context=context)
        if not course:
            messages.error(
                request, 'Without refererncing any course you are not allowed to add question')
            return render(request, 'quiz/add_question.html', context=context)
        if not user:
            messages.error(
                request, 'Please login first!!')
            return render(request, 'quiz/add_question.html', context=context)

        if user and course:
            quizquestion = QuizQuestion()
            quizquestion.user = user
            quizquestion.question = question
            quizquestion.option1 = option1
            quizquestion.option2 = option2
            quizquestion.option3 = option3
            quizquestion.option4 = option4
            quizquestion.answer = answer
            quizquestion.course = course
            if image:
                quizquestion.image = image_url
            quizquestion.save()

            return render(request, 'quiz/add_question.html', context=context)
