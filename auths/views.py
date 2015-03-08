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

def dashboard(request):
	''' View of Dashboard page for user after logging in using the Social Account '''
	return render_to_response('dashboard.html',{'user':request.user},context_instance = RequestContext(request))

def trainModel(request):
	''' View for training the model after fetching the results from google/flickr etc'''
	if not request.user.is_authenticated():
		# if "userId" not in request.session:
		# 	if not request.session.exists(request.session.session_key):
		# 		request.session.create()
		# 		print "NEW SESSION IS CREATED"
		# 	request.session['userId']=request.session._session_key
		# print "THE SESSION HAS BEEN CREATED WITH VALUE",request.session['userId'] 
		# jobId = request.session['userId']
		jobId = createSession(request)
	else:
		jobId = request.session._session_key
	print "JOBID IS ",jobId
	if request.is_ajax():
		print "SUCCESS AJAX CALL"
		category = request.GET.get('category',None)
		category= category.split()
		category='+'.join(category)
		fetchFromGoogle(category,jobId)
	return render_to_response('train.html',{'user':request.user},context_instance=RequestContext(request))

def fetchFromGoogle(searchTerm,jobId):
	''' Function for fetching top 24 Google Images using the google apis'''
	directory = "/home/dypy/Pictures/cloudcv/"+jobId
	print "DIRETORY CREATION STARTS"
	if not os.path.exists(directory):
		os.makedirs(directory+"/test")
		os.makedirs(directory+"/utils")
	if not os.path.exists(directory+"/train/"+searchTerm):
		os.makedirs(directory+"/train/"+searchTerm)
		print "DIRECTORY CREATION SUCCESSFUL"
	fetcher = urllib2.build_opener()
	icount=-1
	flag = 0
	image_type = "image"
	while(icount<=24):
		searchUrl = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + str(searchTerm)+'&rsz=8'+'&start='+str(icount+1)
		print searchUrl
		f = fetcher.open(searchUrl)
		deserialized_output = simplejson.load(f)
		for img in deserialized_output['responseData']['results']:
			try:
				if img['unescapedUrl'][-3:]!="gif":
					file = cStringIO.StringIO(urllib2.urlopen(img['unescapedUrl']).read())
					img = Image.open(file)
					urls = len([i for i in os.listdir(directory+"/train/"+searchTerm) if image_type in i]) + 1
					img.save(directory+"/train/"+searchTerm+"/image"+str(urls)+".jpg", format="JPEG")
					if urls==20:
						flag=1
						break
			except:
				print "$$$$$$$ LOG $$$$$$$"
				print img['unescapedUrl'],urls
		if flag:
			break
		icount+=8

def createSession(request):
	if "userId" not in request.session:
		if not request.session.exists(request.session.session_key):
			request.session.create()
			print "NEW SESSION IS CREATED"
		request.session['userId']=request.session._session_key
	print "THE SESSION HAS BEEN CREATED WITH VALUE",request.session['userId'] 
	jobId = request.session['userId']
	return jobId