from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from .models import QuizSet, QuizQuestion, UserSubmittedAnswer
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
@login_required
def CAMS_QUIZSET(request):
    catData=QuizSet.objects.all()
    return render(request, 'CAMS_Quiz/Quizset.html',{'data':catData})
@login_required
def CAMS_QUESTIONS(request, cat_id):
    category=QuizSet.objects.get(id=cat_id)
    question=QuizQuestion.objects.filter(category=category).order_by('id').first()
    return render(request, 'CAMS_Quiz/Camsquestions.html',{'question':question,'category':category})


@login_required
def SUBMIT_ANSWER(request, cat_id, quest_id):

    if request.method == 'POST':
        category = get_object_or_404(QuizSet, id=cat_id)
        question = QuizQuestion.objects.filter(category=category, id__gt=quest_id).exclude(id=quest_id).order_by('id').first()
        question_prev = QuizQuestion.objects.filter(category=category, id__lt=quest_id).exclude(id=quest_id).order_by('-id').first()
        questions_cat = QuizQuestion.objects.filter(category=category)
        total_questions = questions_cat.count()

        if 'previous' in request.POST:
            if question_prev:
                # Get the previously submitted answer, if any
                prev_answer = UserSubmittedAnswer.objects.filter(user=request.user, question=question_prev).first()
                
                return render(request, 'CAMS_Quiz/Camsquestions.html', {'question': question_prev, 'category': category, 'prev_answer': prev_answer})
            else:
                return HttpResponse('No More Questions!!!')
        else:
            quest = get_object_or_404(QuizQuestion, id=quest_id)
            user = request.user
            answer = request.POST.get('answer')

            # Check if the user has already submitted an answer for the current question
            existing_answer = UserSubmittedAnswer.objects.filter(user=user, question=quest).first()

            if existing_answer:
                # Update the existing answer if it exists
                existing_answer.right_answer = answer
                existing_answer.save()
            else:
                # If no existing answer, create a new one
                UserSubmittedAnswer.objects.create(user=user, question=quest, right_answer=answer if answer else '')
        

        if question:
            return render(request, 'CAMS_Quiz/Camsquestions.html', {'question': question, 'category': category})
        else:
            result=UserSubmittedAnswer.objects.filter(user=request.user)
            percentage = 0 
            rightAns=0
            for row in result:
               if  row.question.right_opt == row.right_answer:
                   rightAns += 1
            percentage=(rightAns*100)/total_questions   


            return render(request, 'CAMS_Quiz/result.html',{'result':result,'rightAns':rightAns,'percentage':percentage})
    else:
        return HttpResponse('Method not allowed!!')

@login_required
def restart_quiz(request):
    # Delete all UserSubmittedAnswer instances for the user
    UserSubmittedAnswer.objects.filter(user=request.user).delete()
    
    # Redirect to the first question in the category
    first_question = QuizQuestion.objects.filter(category__in=QuizSet.objects.all()).order_by('id').first()
    if first_question:
        return redirect('quizset')
    else:
        return HttpResponse('No questions available.')