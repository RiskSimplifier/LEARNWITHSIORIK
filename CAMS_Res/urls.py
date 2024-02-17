from django.urls import path, include
from . import views

urlpatterns = [
  path('/camsresources', views.CAMS_RESOURCES.as_view(), name='camsresources'),
 
]