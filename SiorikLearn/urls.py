
from django.contrib import admin
from django.urls import path,include
from .import views,user_login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base', views.BASE, name='base'),
    path('404', views.PAGE_NOT_FOUND, name='404'),
    path('', views.HOME, name='home'),
    path('courses', views.SINGLE_COURSE, name='single_course'),
    path('courses/filter-data',views.filter_data,name="filter-data"),
    path('course/<slug:slug>', views.COURSE_DETAILS, name='course_details'),
    path('search',views.SEARCH_COURSE, name='search_course'),
    path('Blog', views.BLOG, name='blog'),
    path('Services', views.OUR_SERVICES, name='our_services'),
    path('contact', views.CONTACT_US, name='contact_us'),
    path('about', views.ABOUT_US, name='about_us'),

    path('accounts/register', user_login.REGISTER, name='register'),
    path('accounts/login', user_login.DO_LOGIN, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('doLogin', user_login.DO_LOGIN, name='doLogin'),
    path('accounts/profile', user_login.PROFILE, name='profile'),
    path('accounts/profile/update', user_login.PROFILE_UPDATE, name='profile_update'),
    path('checkout/<slug:slug>/', views.CHECKOUT, name='checkout'),
    path('my-course', views.MY_COURSE, name='my_course'),
    path('course/watch-course/<slug:slug>',views.WATCH_COURSE,name='watch_course'),
    path('submit_review/<int:course_id>/', views.SUBMIT_REVIEW,name='submit_review'),
    path('verify-payment',views.verify_payment,name='verify_payment'),
   
    path('watch-course', include('CAMS_Res.urls')),
    path('watch-course', include('CAMS_Quiz.urls')),
     path('', include('chatbot.urls')),
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        # ...
        path('__debug__/', include(debug_toolbar.urls)),
        # ...
    ] + urlpatterns