from django.contrib import admin
from .models import *
from CAMS_Res.models import *
from CAMS_Quiz.models import *
from chatbot.models import *

class What_you_learn_TabularInline(admin.TabularInline):
    model = What_you_learn

class Requirement_TabularInline(admin.TabularInline):
    model = Requirements

class Video_TabularInline(admin.TabularInline):
    model = Video
    autocomplete_fields = ['lesson']

   

#@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = (What_you_learn_TabularInline,Requirement_TabularInline,Video_TabularInline)
    list_display = ['title' , 'price','discount']
    list_editable = ['price','discount']
    iist_per_page = 10
    search_fields = ['title']

class BlogAdmin(admin.ModelAdmin):
    search_fields =['blog_title']

class LessonAdmin(admin.ModelAdmin):
    search_fields =['name']

# Register your models here.
@admin.register(CAMS_Files)
class CAMSResAdmin(admin.ModelAdmin):
    search_fields = ['word_files','files_url']

# Register your models here.
admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course,CourseAdmin)
admin.site.register(Level)
admin.site.register(What_you_learn)
admin.site.register(Requirements)
admin.site.register(Lesson,LessonAdmin)
admin.site.register(Language)
admin.site.register(UserCourse)
admin.site.register(Payment)
admin.site.register(Blog,BlogAdmin)
admin.site.register(ReviewRating)
admin.site.register(QuizSet)
admin.site.register(Chat)

class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question','category' )
    search_fields = ['question']
admin.site.register(QuizQuestion,QuizQuestionAdmin)

class UserSubmittedAnswerAdmin(admin.ModelAdmin):
    list_display = ('id','question','user','right_answer')
admin.site.register(UserSubmittedAnswer,UserSubmittedAnswerAdmin)
