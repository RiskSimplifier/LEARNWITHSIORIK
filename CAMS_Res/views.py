from django.shortcuts import render
from .models import CAMS_Files
from django.views import generic
# Create your views here.

class CAMS_RESOURCES(generic.ListView):
	model = CAMS_Files
	template_name = 'CAMS_Res/Resources.html'
	context_object_name = 'files'
	paginate_by = 10


	def get_queryset(self):
		return CAMS_Files.objects.order_by('id')