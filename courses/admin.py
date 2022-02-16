from django.contrib import admin
from courses.models import Course, Tag, Prerequisite, Learning, Video, UserCourse, Payment, DoubtAnswer, DoubtQuestion, CourseRequest
from django.utils.html import format_html


class TagAdmin(admin.TabularInline):
    model = Tag


class VideoAdmin(admin.TabularInline):
    model = Video


class PrerequisiteAdmin(admin.TabularInline):
    model = Prerequisite


class LearningAdmin(admin.TabularInline):
    model = Learning


class CourseAdmin(admin.ModelAdmin):
    inlines = [TagAdmin, PrerequisiteAdmin, LearningAdmin, VideoAdmin]
    list_display = ['name', 'owner', 'get_price', 'get_discount', 'active']
    list_filter = ['discount', 'active']

    def get_discount(self, course):
        return f'{course.discount}%'

    def get_price(self, course):
        return f'₹ {course.price}'

    get_discount.short_description = 'Discount'
    get_price.short_description = 'Price'


class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ['order_id', 'get_user', 'get_course', 'status']
    list_filter = ['course', 'status']

    def get_user(self, payment):
        return format_html(f'<a href="/admin/auth/user/{payment.user.id}">{payment.user}</a>')

    def get_course(self, payment):
        return format_html(f'<a href="/admin/courses/course/{payment.course.id}">{payment.course}</a>')

    get_user.short_description = 'User'
    get_course.short_description = 'Course'


class VideoAdmin(admin.ModelAdmin):
    model = Video
    list_display = ['title', 'serial_number', 'get_course', 'is_preview']
    list_filter = ['course', 'is_preview']

    def get_course(self, payment):
        return format_html(f'<a href="/admin/courses/course/{payment.course.id}">{payment.course}</a>')

    get_course.short_description = 'Course'


class UserCourseAdmin(admin.ModelAdmin):
    model = UserCourse
    list_display = ['get_details', 'get_user', 'get_course', 'is_active']

    def get_details(self, UserCourse):
        return('Show Details')

    def get_user(self, UserCourse):
        return format_html(f'<a href="/admin/auth/user/{UserCourse.user.id}">{UserCourse.user}</a>')

    def get_course(self, UserCourse):
        return format_html(f'<a href="/admin/courses/course/{UserCourse.course.id}">{UserCourse.course}</a>')

    get_course.short_description = 'Course'
    get_user.short_description = 'User'
    get_details.short_description = 'UserCourse'


class DoubtQuestionAdmin(admin.ModelAdmin):
    list_display = ['get_question', 'user', 'course']
    list_filter = ['user', 'course']

    def get_question(self, DoubtQuestion):
        if len(DoubtQuestion.question) > 30:
            return f'{DoubtQuestion.question[:30]}...'
        else:
            return f'{DoubtQuestion.question[:30]}'
    get_question.short_description = 'Question'


class DoubtAnswerAdmin(admin.ModelAdmin):
    list_display = ['get_answer', 'get_question', 'user', 'course']
    list_filter = ['user', 'course']

    def get_answer(self, DoubtAnswer):
        return f'{DoubtAnswer.answer[:30]}...'
    get_answer.short_description = 'Answer'

    def get_question(self, DoubtAnswer):
        return f'{DoubtAnswer.question.question[:15]}...'
    get_question.short_description = 'Question'


class CourseRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'course']
    list_filter = ['user', 'course']


admin.site.register(Course, CourseAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(UserCourse, UserCourseAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(DoubtQuestion, DoubtQuestionAdmin)
admin.site.register(DoubtAnswer, DoubtAnswerAdmin)
admin.site.register(CourseRequest, CourseRequestAdmin)
