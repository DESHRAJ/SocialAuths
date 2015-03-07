from django.shortcuts import render
from django.http import * 
from django.shortcuts import render_to_response
from django.template import Context,RequestContext
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
from lxml import etree
import urllib2
import requests
import re
import urllib2
import os
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
			fetchFromGoogle(category)
			# print "$$$$$$$$$$$$$", category
			# searchUrl='https://www.google.com/search?tbm=isch&q='+str(category)+'&gws_rd=cr&ei=8Vb6VJGvOIe5uASIk4KwAQ'
			# print searchUrl
			# page=urllib2.urlopen(searchUrl).read()
			# x=etree.HTML(page)
			# print x
			# url=x.xpath('//td[@class="titleColumn"]/a/@href')
			# rank=x.xpath('//td[@class="titleColumn"]/span[@name="ir"]/text()')
			# title=x.xpath('//td[@class="titleColumn"]/a/@title')
		return render_to_response('train.html',{'user':request.user},context_instance=RequestContext(request))
	return HttpResponseRedirect('/')

def fetchFromGoogle(query):
	image_type = "Action"
	# you can change the query for the image  here  
	# query = "Terminator 3 Movie"
	query= query.split()
	query='+'.join(query)
	url="https://www.google.co.in/searches_sm=122&source=lnms&tbm=isch&sa=X&ei=4r_cVID3NYayoQTb4ICQBA&ved=0CAgQ_AUoAQ&biw=1242&bih=619&q="+query
	print url
	header = {'User-Agent': 'Mozilla/5.0'} 
	soup = get_soup(url,header)
	images = [a['src'] for a in soup.find_all("img", {"src": re.compile("gstatic.com")})]
	for img in images:
		print "##########   ",img
	# for img in images:
	# 	raw_img = urllib2.urlopen(img).read()
	# 	#add the directory for your image here 
	# 	DIR="C:\Users\hp\Pictures\\valentines\\"
	# 	cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
	# 	print cntr
	# 	f = open(DIR + image_type + "_"+ str(cntr)+".jpg", 'wb')
	# 	f.write(raw_img)
	# 	f.close()
def get_soup(url,header):
	return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)))