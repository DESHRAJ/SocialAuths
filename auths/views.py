from django.shortcuts import render
from django.http import * 
from django.shortcuts import render_to_response
from django.template import Context,RequestContext
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
from lxml import etree
from urllib import FancyURLopener
import urllib2
import requests
import re
import os
import sys
import simplejson
import cStringIO
import Image
# Create your views here.
def home(request):
	''' View for the home page of the application'''
	if request.user.is_authenticated():
		return HttpResponseRedirect('/dashboard')
	return render_to_response('index.html')

# @login_required	
def dashboard(request):
	''' View of Dashboard page for user after logging in using the Social Account '''
	return render_to_response('dashboard.html',{'user':request.user},context_instance = RequestContext(request))

# @login_required
def trainModel(request):
	''' View for training the model after fetching the results from google/flickr etc'''
	if request.user.is_authenticated():
		if request.GET:
			category = request.GET.get('category')
			category = category.lower()
			# os.makedirs('/'+request.user.email+'/train/'+category)
			# os.makedirs('/'+request.user.email+'/test')
			fetchFromGoogle(category)
		return render_to_response('train.html',{'user':request.user},context_instance=RequestContext(request))
	return HttpResponseRedirect('/')

def fetchFromGoogle(searchTerm):
	''' Function for fetching 20 images using the google apis'''
	fetcher = urllib2.build_opener()
	startIndex = 0
	i,urls=1,1
	while(i<=20):
		flag=0
		searchUrl = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + str(searchTerm)+'&rsz=8'+'&start='+str(i)
		print searchUrl
		f = fetcher.open(searchUrl)
		deserialized_output = simplejson.load(f)
		for img in deserialized_output['responseData']['results']:
			if urls>=20:
				flag=1
				break
			else:
				file = cStringIO.StringIO(urllib2.urlopen(img['unescapedUrl']).read())
				img = Image.open(file)
				directory = "/home/dypy/Pictures/cloudcv/"+str(searchTerm)
				if not os.path.exists(directory):
					os.makedirs(directory)
				img.save(directory+"/image"+str(urls)+".jpg", format="JPEG")
				# urls.append(img['unescapedUrl'])
				# print "$$$$$$$$$$", "          ", len(urls)
				urls+=1
		if flag==1:
			break
		i+=8