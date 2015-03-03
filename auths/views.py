from django.shortcuts import render
from django.http import * 
from django.shortcuts import render_to_response
# Create your views here.
def home(request):
	''' View for the home page of the application'''
	if request.user.is_authenticated():
		return HttpResponseRedirect('/dashboard')
	return render_to_response('index.html')

def dashboard(request):
	return render_to_response('dashboard.html')
