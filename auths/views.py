from django.shortcuts import render
from django.http import * 
from django.shortcuts import render_to_response
from django.template import Context,RequestContext
from django.contrib.auth.decorators import login_required
# from bs4 import BeautifulSoup
# from lxml import etree
from urllib import FancyURLopener
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import urllib2
import requests
import re
import os
import sys
import simplejson
import cStringIO
import zipfile
# Create your views here.

def home(request):
	''' View for the home page of the application'''
	# if request.user.is_authenticated():
		# return HttpResponseRedirect('/dashboard')
	return render_to_response('material.html')

def dashboard(request):
	''' View of Dashboard page for user after logging in using the Social Account '''
	return render_to_response('muitrain.html',{'user':request.user},context_instance = RequestContext(request))

def trainModel(request):
	''' View for training the model after fetching the results from google/flickr etc'''
	
	if not request.user.is_authenticated():
		jobId = createSession(request)
	else:
		jobId = request.session._session_key
	print "JOBID IS ",jobId
	if request.is_ajax():
		print "SUCCESS AJAX CALL"
		category = request.GET.get('category',None)
		print "THE CATEGORY IS ",category
		if "http" in category:
			print "INSIDE IF CONDITION"
			category = category[:-1]+"1"
			path = "/home/dypy/Pictures/cloudcv/"+jobId+"/train/"
			dropboxUrlFetch(category,path)
		else:
			category= category.split()
			category='+'.join(category)
			fetchFromGoogle(category,jobId)
	return render_to_response('muitrain.html',{'user':request.user},context_instance=RequestContext(request))

@csrf_exempt
def testaclass(request):
	''' View for testing the class '''
	if request.is_ajax():
		print 0
		if request.POST:
			jobId = request.session._session_key
			print jobId
			img = request.FILES['testimageA']
			print 1
			destination = open('/home/dypy/Pictures/cloudcv/'+jobId+'/test/'+img.name, 'wb+')
			print 2
			for chunk in img.chunks():
				print 3
				destination.write(chunk)
			destination.close()
			print "HEY I GOT THE FILE NAMED", img
		if request.GET:
			value = request.GET.get('value',None)
			if "http" in value:
				jobId = request.session._session_key
				print "INSIDE IF CONDITION"
				value = value[:-1]+"1"
				path = "/home/dypy/Pictures/cloudcv/"+jobId+"/test/"
				dropboxUrlFetch(value,path)
	return render_to_response('muitrain.html',context_instance = RequestContext(request))

def fetchFromGoogle(searchTerm,jobId):
	''' Function for fetching top 24 Google Images using the google apis'''
	
	directory = "/home/dypy/Pictures/cloudcv/"+jobId
	print "DIRETORY CREATION STARTS"
	if not os.path.exists(directory):
		os.makedirs(directory)
		os.makedirs(directory+"/test")
		os.makedirs(directory+"/util")
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
					filename = cStringIO.StringIO(urllib2.urlopen(img['unescapedUrl']).read())
					imgg = Image.open(filename)
					urls = len([i for i in os.listdir(directory+"/train/"+searchTerm) if image_type in i]) + 1
					if img['unescapedUrl'][-3:]=='png':
						imgg.save(directory+"/train/"+searchTerm+"/image"+str(urls)+".png", format="PNG")
					elif img['unescapedUrl'][-3:]=='jpg' or img['unescapedUrl'][-3:]=='jepg':
						imgg.save(directory+"/train/"+searchTerm+"/image"+str(urls)+".jpg", format="JPEG")
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
	''' view for creating the session for the new users '''
	if "userId" not in request.session:
		if not request.session.exists(request.session.session_key):
			request.session.create()
			print "NEW SESSION IS CREATED"
		request.session['userId']=request.session._session_key
	print "THE SESSION HAS BEEN CREATED WITH VALUE",request.session['userId'] 
	jobId = request.session['userId']
	return jobId

@csrf_exempt
def deleteImage(request):
	''' view for deleting the images from the /jobid/test/ folder'''
	print "YEAH I AM INSIDE DELETE"
	jobId = request.session._session_key
	if request.is_ajax():
		if request.POST:
			imgname = request.POST['name']
		# sessionId = request.session._session_key
		os.remove('/home/dypy/Pictures/cloudcv/'+jobId+'/test/'+imgname)
	return render_to_response('muitrain.html') 

def dropboxUrlFetch(url,path):
	print "UNZIPPING START"
	zippedfile = cStringIO.StringIO(urllib2.urlopen(url).read())
	print "SUCCESSFULLY READ THE URL FOR UNZIPPING"
	with zipfile.ZipFile(zippedfile, "r") as z:
		z.extractall(path)
		print "UNZIPPING DONE"

def material(request):
	return render_to_response("material.html",context_instance=RequestContext(request))

def temp(request):
	return render_to_response("mdashboard.html")

def temp1(request):
	return render_to_response("testing.html")