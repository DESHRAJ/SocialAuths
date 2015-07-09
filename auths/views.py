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
	if request.user.is_authenticated():
		print "first_name : ",request.user.first_name
		print "last_name : ",request.user.last_name
		print "email : ", request.user.email
		print "username : ", request.user.username
	return render_to_response('material.html')

def dashboard(request):
	''' View of Dashboard page for user after logging in using the Social Account '''
	return render_to_response('cloudcvtest.html',{'user':request.user},context_instance = RequestContext(request))

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

#################################################################################################################


from django.contrib.auth.models import User
from auths.models import *
# from app.models import *

# @csrf_exempt
# @login_required
# def s3connect(request):
# 	credentials = None
# 	print request.user.first_name
# 	# if request.is_ajax():
# 	if request.user.is_authenticated():
# 		print "!!!!!!!!!!!!!!!!!!!"
# 		if request.method=="POST":
# 			print "@@@@@@@@@@@@@"
# 			key = request.POST['key']
# 			secret = request.POST['secret']
# 			print key
# 			print secret
# 			print request.user.id
# 			# StorageCredentials.objectes.create(aws_access_key = key, aws_access_secret = secret, user = request.user).save()
# 			# try:
# 			user = User.objects.get(id=request.user.id)
# 			StorageCredentials.objects.create(aws_access_key = str(key), aws_access_secret = str(secret), user = user).save()
# 			print "TRY"
# 			# credentials.save()
# 				# except:
# 					# credentials = None
# 					# print "EXCEPT"
# 	return HttpResponseRedirect("/addstorage")

def addstorage(request):
	return render_to_response("add_storage.html")


from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.views import *

class AddStorage(FormView):
	template_name = "add_storage.html"
	form_class = DisconnectForm
	success_url = "/addstorage"

	# def get(self, request, *args, **kwargs):
	# 	return render_to_response("add_storage.html")

	def get_form_class(self):
		return get_form_class(app_settings.FORMS,
							  'disconnect',
							  self.form_class)

	def get_form_kwargs(self):
		kwargs = super(AddStorage, self).get_form_kwargs()
		kwargs["request"] = self.request
		return kwargs

	def form_valid(self, form):
		get_account_adapter().add_message(self.request,
										  messages.INFO,
										  'socialaccount/messages/'
										  'account_disconnected.txt')
		form.save()
		return super(AddStorage, self).form_valid(form)
	
	def post(self,request):
		if request.user.is_authenticated():
			if request.method=="POST":
				key = request.POST['key']
				secret = request.POST['secret']
				print key
				print secret
				print request.user.id
				# try:
				user = User.objects.get(id=request.user.id)
				StorageCredentials.objects.create(aws_access_key = str(key), aws_access_secret = str(secret), user = user).save()
				print "TRY"
		return HttpResponseRedirect("/addstorage/")

storage = login_required(AddStorage.as_view())

from boto.s3.connection import S3Connection,Key
@login_required
def get_from_s3(request):
	path_to_download = ""
	# user = User.objects.get(id = request.user.id)
	# if request.method=="POST":

		# provider = request.POST['provider']
		# if provider.lower()=="dropbox":
			# s3_instance = request.POST['']
			# conn = S3Connection(, )


'''

AWS S3 Working for CloudCV

from boto.s3.connection import * 
conn = S3Connection("AKIAJISUCCBNYECJPTIA","1tLIgzgYIpGXlP3WGDeAXW2t4b+GU1QT7k/STi/J")
b = conn.get_bucket("cloudcv")
k = Key(b)
k.key = "/home/test.txt"  
k.set_contents_from_filename("/home/pydev/code.txt")
k.get_contents_as_string()
for i in b.list():
	print i.name.encode('utf-8')

bucket_entries = bucket.list(prefix='/path/to/your/directory')


# returns a list of files stored in bucket 'bucket_name'
getFileNamesInBucket(bucket_name)
 
# download a file named 'filename' from bucket 'bucket_name' to 'local_download_directory'
downloadFileFromBucket(bucket_name, filename, local_download_directory)
 
# download all of the files in bucket 'bucket_name' to the 'local_download_directory"
downloadAllFilesFromBucket(bucket_name, local_download_directory)
 
# delete all files in bucket 'bucket_name'
deleteAllFilesFromBucket(bucket_name)
 
# download files with names that satisfy 'filename_predicate' from 'bucket_name' to 'local_download_directory'
downloadFilesInBucketWithPredicate(bucket_name, filename_predicate, local_download_directory)
 
# delete files with names that satisfy 'filename_predicate' from 'bucket_name'
deleteFilesInBucketWithPredicate(bucket_name, filename_predicate)

'''
from allauth.socialaccount.models import * 
# def apitest(request):
# 	providers = []
# 	# user = User.objects.get(id = request.user.id)
# 	# social_account = SocialAccount.objects.get(user = )
# 	tokens = SocialToken.objects.filter(account__user__id = request.user.id)
# 	for i in tokens:
# 		providers.append(str(i.app))
# 	s3 = StorageCredentials.objects.filter(user__id = request.user.id).count()
# 	print s3
# 	print providers
# 	if s3:
# 		providers.append("Amazon S3")
# 	return render_to_response("upload_to_storage.html",{'p':providers},context_instance = RequestContext(request))

class UploadApiTest(TemplateView):
	def get(self, request, *args, **kwargs):
		providers = []
		tokens = SocialToken.objects.filter(account__user__id = request.user.id)
		for i in tokens:
			providers.append(str(i.app))
		s3 = StorageCredentials.objects.filter(user__id = request.user.id).count()
		if s3:
			providers.append("Amazon S3")
		return render_to_response("upload_to_storage.html",{'p':providers},context_instance = RequestContext(request))
	
	@csrf_exempt
	def post(self,request):
		print "POST Request to API "
		storage = request.POST['storageName']
		path = request.POST['path']
		if storage=="Amazon S3":
			result = put_data_on_s3(request,path)
		else:
			social_token = SocialToken.objects.get(account__user__id = request.user.id, app__name = storage)
			print "Its ",storage
		return HttpResponse(json.dumps(result), content_type="application/json")


class DownloadApiTest(TemplateView):
	def get(self, request, *args, **kwargs):
		providers = []
		tokens = SocialToken.objects.filter(account__user__id = request.user.id)
		for i in tokens:
			providers.append(str(i.app))
		s3 = StorageCredentials.objects.filter(user__id = request.user.id).count()
		if s3:
			providers.append("Amazon S3")
		return render_to_response("download_from_storage.html",{'p':providers},context_instance = RequestContext(request))
	
	def post(self,request):
		path = request.POST['path']
		storage = request.POST['storageName']
		if storage=="Amazon S3":
			result = get_data_from_s3(request,path)
		else:
			social_token = SocialToken.objects.get(account__user__id = request.user.id, app__name = storage)
			print "Its ",storage
		return HttpResponse(json.dumps(result), content_type="application/json")




from boto.s3.connection import * 

import json
import traceback 
def put_data_on_s3(request,path):
	result = {}
	bucket = request.POST["bucket"]
	result['pathProvided'] = request.POST['path']
	result['bucket'] = bucket
	result['storage'] = request.POST['storageName']
	result['user'] = request.user.email
	result['uplaodedTo'] = []
	images = request.FILES.getlist('images')
	if str(path)[-1]!="/":
		path = str(path)+"/"
	s3 = StorageCredentials.objects.get(user__id = request.user.id)
	conn = S3Connection(s3.aws_access_key,s3.aws_access_secret)
	try:
		b = conn.get_bucket(bucket)
	except:
		b = conn.create_bucket(bucket)
	for i in images:
		destination = open('/media/' + (i.name).encode('utf-8'), 'wb+')
		for chunk in i.chunks():
			destination.write(chunk)
		destination.close()
		k = Key(b)
		k.key = path+str(i.name).encode("utf-8")
		result['uplaodedTo'].append(k.key)
		k.set_contents_from_filename("/media/" + str(i.name).encode("utf-8"))
	return result


def get_data_from_s3(request,path):
	result = {}
	bucket = request.POST["bucket"]
	# result['location'] = request.POST['path']
	result['user'] = request.user.email
	result['storage'] = request.POST['storageName']
	result['bucket'] = bucket
	result['location']= []
	result['downloadTo'] = []
	if str(path)[-1]!="/":
		path = str(path)+"/"
	s3 = StorageCredentials.objects.get(user__id = request.user.id)
	conn = S3Connection(s3.aws_access_key,s3.aws_access_secret)
	try:
		b = conn.get_bucket(bucket)
	except:
		print "NO BUCKET FOUND"
	bucket_entries = b.list(path[1:])
	for i in bucket_entries:
		result['location'].append(i.key)
		# print "Working"
		print i.key
		file_name = str(i.key).split("/")[-1]
		result['downloadTo'].append("/media/"+file_name)
		i.get_contents_to_filename("/media/"+file_name)
	# conn.downloadFilesInBucketWithPredicate(bucket, bucket_entries,"/media/")
	# except:
		# print "#### ERRRRRORRRRRR  #####"
		# return HttpResponse(str(traceback.format_exc())
	# for i in bucket_entries:
	# 	# download files with names that satisfy 'filename_predicate' from 'bucket_name' to 'local_download_directory'
	# 	destination = open('/media/' + (i.name).encode('utf-8'), 'wb+')
	# 	for chunk in i.chunks():
	# 		destination.write(chunk)
	# 	destination.close()
	# 	k = Key(b)
	# 	k.key = path+str(i.name).encode("utf-8")
	# 	k.set_contents_from_filename("/media/" + str(i.name).encode("utf-8"))
	return result

up_storage_api = login_required(UploadApiTest.as_view())
down_storage_api = login_required(DownloadApiTest.as_view())

