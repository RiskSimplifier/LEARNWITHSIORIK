import base64
import datetime
import hashlib
import hmac
import secrets
import uuid
from django.contrib import messages
from django.shortcuts import redirect, render
from app.forms import ReviewForm, TransactionForm

from django.shortcuts import render, redirect


from app.models import Categories, Course, Lesson, Level, ReviewRating, UserCourse, Video,Payment, Blog
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum, Avg
import time

from .settings import * 
from django.views.decorators.csrf import csrf_exempt

import datetime
from uuid import uuid4
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.views.generic import FormView







def BASE(request):
    return render(request,'base.html')

def HOME( request):
    category = Categories.objects.all().order_by('id')[0:5]
    blog = Blog.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status = 'PUBLISH').order_by('-id')
    
    course_count = Course.objects.count()
    context = {
        'category': category,
        'course' : course,
        'blog' : blog,
        'course_count' :course_count,
        
    }
    return render(request, 'Main/home.html', context)

def SINGLE_COURSE( request):
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    FreeCourse_count = Course.objects.filter(price=0).count()
    PaidCourse_count = Course.objects.filter(price__gte=1).count()
    context = {
        'category':category,
        'level': level,
        'course': course,
        'FreeCourse_count':FreeCourse_count,
        'PaidCourse_count':PaidCourse_count,
    }
    return render(request, 'Main/single_course.html',context)

def filter_data(request):
   category = request.GET.getlist('category[]')
   level = request.GET.getlist('level[]')
   price = request.GET.getlist('price[]')

   if price == ['PriceFree']:
       course = Course.objects.filter(price=0)
   elif price == ['PricePaid']:
       course = Course.objects.filter(price__gte=1)
   elif price == ['PriceAll']:
        course = Course.objects.all()
   elif category:
       course = Course.objects.filter(category__id__in=category).order_by('-id')
   elif level:
       course = Course.objects.filter(level__id__in = level).order_by('-id')
   else:
       course = Course.objects.all().order_by('-id')
   
   context = {
       'course':course
   }
   t = render_to_string('ajax/course.html', context)
   return JsonResponse({'data': t})


def CONTACT_US( request):
    category = Categories.get_all_category(Categories)

    context = {
        'category':category
    }
    return render(request, 'Main/contact_us.html',context)

def ABOUT_US( request):
    category = Categories.get_all_category(Categories)

    context = {
        'category':category
    }
    return render(request, 'Main/about_us.html', context)

def BLOG( request):
    category = Categories.get_all_category(Categories)
    blog = Blog.objects.all()

    context = {
        'blog':blog,
        'category':category
    }
    return render(request, 'Main/blog.html', context)

def OUR_SERVICES( request):
    # category = Categories.get_all_category(Categories)

    # context = {
    #     'category':category
    # }
    return render(request, 'Main/our_services.html')

def DO_LOGIN(request):
    
    return None

def SEARCH_COURSE(request):
    category = Categories.get_all_category(Categories)

   
    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query)
    context = {
        'course':course,
        'category':category
    }
    return render(request,'search/search.html',context)

def COURSE_DETAILS(request, slug):
    if not request.user.is_authenticated:
        return redirect('register')
    
    category = Categories.get_all_category(Categories)
    time_duration = Video.objects.filter(course__slug = slug).aggregate(sum=Sum('time_duration'))['sum']
    hours, minutes = divmod(time_duration, 60)
    course_id = Course.objects.get(slug = slug)
    reviews = ReviewRating.objects.filter(course_id=course_id.id, status=True)
   
    #student_rating = ReviewRating.objects.filter(user = request.user, rating = rating_all, status=True).aggregate(sum=Sum('user'))
    lesson = Lesson.objects.filter(course_id=course_id.id)
    students = UserCourse.objects.filter(course= course_id)
    try:
        check_enroll = UserCourse.objects.get(user = request.user, course= course_id)
    except UserCourse.DoesNotExist:
        check_enroll = None
        course = Course.objects.filter(slug=slug)

    course = Course.objects.filter(slug = slug)
    if course.exists():
        course=course.first()
    else:
        return redirect('404')
    
   
    context = {
        'course': course,
        'category':category,
        'time_duration':time_duration,
        'check_enroll':check_enroll,
        'reviews': reviews,
        'students' : students,
        'lesson' : lesson,
         'hours':int(hours),
         'minutes':int(minutes)
        #'student_rating':student_rating
    }
    return render(request,'course/course_details.html',context)

def PAGE_NOT_FOUND(request):
    category = Categories.get_all_category(Categories)

    context = {
        'category':category
    }
    return render(request,'error/404.html', context)

def CHECKOUT(request, slug):
    course = Course.objects.get(slug=slug)
    user1 = request.user
    if UserCourse.objects.filter(user=request.user, course=course).exists():
        messages.error(request, 'You are already enrolled in this course')
        return redirect('my_course')
    if course.price == 0:
        course = UserCourse(
            user=request.user,
            course=course,
        )
        course.save()
        messages.success(request, 'Course Are Successfully Enrolled !')
        return redirect('my_course')

    elif request.method == 'POST':
        amount_cal = course.price - (course.price * course.discount / 100)
        amount = int(amount_cal)

        payment = Payment.objects.create(
            course=course,
            user=request.user,
            order_id=secrets.token_hex(8),
            payment_id=str(uuid.uuid4()),
        )

        signed_datetime = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

        # Create a payment request
        form_data = {
            "access_key": settings.CYBERSOURCE_ACCESS_KEY1,
            "profile_id": settings.CYBERSOURCE_PROFILE_ID1,
            "transaction_uuid": payment.payment_id,
            "signed_field_names": "",
            "unsigned_field_names": "card_type,card_number,card_expiry_date",
            "signed_date_time": signed_datetime,
            "locale": "en",
            "transaction_type": "sale",
            "reference_number": payment.order_id,
            "amount": amount,
            "currency": "USD",
            "payment_method": "card",
            "bill_to_forename": request.POST.get("first_name"),
            "bill_to_surname": request.POST.get("last_name"),
            "bill_to_email": request.POST.get("email"),
            "bill_to_phone": request.POST.get("billing_phone"),
            "bill_to_address_line1": get_attribute(request.POST, "billing_address_1", "Kathmandu"),
            "bill_to_address_city": get_attribute(request.POST, "billing_city", "Kathmandu"),
            "bill_to_address_state": get_attribute(request.POST, "billing_state", "Kathmandu"),
            "bill_to_address_country": get_attribute(request.POST, "billing_country", "NP"),
            "bill_to_address_postal_code": get_attribute(request.POST, "billing_postcode", "Kathmandu"),
        }
        signed_field_names = form_data.keys()
        form_data["signed_field_names"] = ",".join(signed_field_names)
        form_data["signature"] = construct_signature(
            signed_field_names, form_data
        )
        form_data["auth_trans_ref_no"] = payment.order_id
        
        
        return render(request, "checkout/process_payment_cybersource.html", context=form_data)
    else:
        # Display the checkout form (initial request)
        return render(request, 'checkout/checkout.html', context={"course": course,"user":user1})



def MY_COURSE(request):
    course = UserCourse.objects.filter(user = request.user)

    context = {
        'course': course,
    }

    return render(request, 'course/my-course.html', context)

def construct_signature(signed_field_names, data):
    signature = ""
    for field in signed_field_names:
        signature += field + "=" + str(data.get(field, "")) + ","
    signature = signature.rstrip(",")
    hashed = hmac.new(
        bytes(settings.CYBERSOURCE_SECRET_KEY1, "utf-8"),
        bytes(signature, "utf-8"),
        hashlib.sha256,
    )
    digest_base64 = base64.b64encode(hashed.digest()).decode("utf-8")
    return digest_base64


def get_attribute(data, attribute, default=""):
    if data.get(attribute):
        return data.get(attribute)
    return default


@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        request_data = request.POST.dict()
        
        payment = Payment.objects.get(payment_id=request_data.get("req_transaction_uuid"))
        signed_field_names = request_data.get("signed_field_names").split(",")
        signature = construct_signature(signed_field_names, request_data)
        if signature != request_data.get("signature"):
            payment.status = False
            payment.remarks = "Signature mismatch"
            payment.save()
            return render(request, 'verify_payment/fail.html', context={"transaction": payment})

        if request_data.get("decision") == "ACCEPT":
            payment.status = True
            user_course = UserCourse.objects.create(
                user=payment.user,
                course=payment.course,
                paid=True,
            )
            payment.user_course = user_course
        else:
            payment.status = False
        payment.remarks = request_data.get("message")
        payment.save()

        if payment.status is True:
            # Payment successful
            # Enroll the user in the course
            # ... your logic for course enrollment
            return render(request, 'verify_payment/success.html', {'payment': payment})
        else:
            # Payment failed
            return render(request, 'verify_payment/fail.html', {'error_message': payment.remarks})
    else:
        return render(request, 'verify_payment/fail.html')




def WATCH_COURSE(request, slug):
    course = Course.objects.filter(slug = slug)

    lecture = request.GET.get('lecture')
   
    
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    if lecture is not None and lecture != "":
        video = Video.objects.get(id = lecture)
        context = {
        'course' : course,
        'video' : video,
    }
    else:
         context = {
        'course' : course,
        
    }

    
    return render(request,'course/watch-course.html', context)

def SUBMIT_REVIEW(request, course_id):
    url = request.META.get('HTTP_REFERER')
   
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, course__id=course_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.review_title = form.cleaned_data['review_title']
                data.rating = form.cleaned_data['rating']
                data.review_content = form.cleaned_data['review_content']
                data.ip = request.META.get('REMOTE_ADDR')
                data.course_id  = course_id
                data.user_id = request.user.id
                data.save()
                print(data)
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
            


