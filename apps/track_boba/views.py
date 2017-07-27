# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
from django.core import serializers
import json

# Create your views here.
def dashboard(request):
	return render(request, 'track_boba/index.html')

def index(request):
	return render(request, 'track_boba/login.html')

def register(request):
	if request.method == "POST":
		errors = Users.objects.validate(request.POST)
		if errors:
			for tags,error in errors.iteritems():
				messages.error(request, error, extra_tags=tags)
		else:
			taken = Users.objects.filter(email = request.POST['email'])
			if len(taken) > 1:
				messages.error(request, "Email is already in use")
			else:
				user = Users.objects.create(name = request.POST['name'], email = request.POST['email'], password = request.POST['pass'])
				request.session['user_id'] = user.id
				return redirect('/dashboard')
	
	return redirect('/')

def addplace(request):
	print request.POST['lat']
	print request.POST['lng']
	print request.POST['name']
	place = BobaPlaces.objects.create(lat = request.POST['lat'], lng = request.POST['lng'] , name = request.POST['name'])
	TimesDrugged.objects.create(bobaplace = place, user = Users.objects.get(id = request.session['user_id']), timesDrugged = 1)
	return HttpResponse('Hello')

def getall(request):
	boba = BobaPlaces.objects.all()
	return HttpResponse(serializers.serialize("json", boba), content_type='application/json')


