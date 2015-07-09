from allauth.forms import * 
from django.db import models
from django.forms import ModelForm

class UserLogin(ModelForm):
	class Meta:
		model  = User
		fields = '__all__'