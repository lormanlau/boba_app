# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
from django.core import serializers
import json
from .yelp import *
from django.db.models import Q 

# Create your views here.
def dashboard(request):
	context = {
		'lat': Users.objects.get(id=request.session['user_id']).lat,
		'lng': Users.objects.get(id=request.session['user_id']).lng
	}
	return render(request, 'track_boba/index.html', context)

def index(request):
	return render(request, 'track_boba/login.html')



def signin(request):
	context = {
		'type': False
	}
	return render(request, 'track_boba/login.html', context)

def login(request):
	if request.method == 'POST':
		user = Users.objects.filter(email = request.POST['email'])
		if len(user) < 1:
			messages.error(request, "Email does not exist", extra_tags="email")
		else:
			user = user.first()
			if request.POST['pass'] != user.password:
				messages.error(request, "Password does not match", extra_tags="password")
			else:
				request.session['user_id'] = user.id
				request.session['lat'] = user.lat
				request.session['lng'] = user.lng
				return redirect('/dashboard')
	return redirect('/')

def reg(request):
	context = {
		'type': True
	}
	return render(request, 'track_boba/login.html', context)

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
	
	return redirect('/', context)

def giveLastPos(request):
	user = Users.objects.get(id = request.session['user_id'])
	return HttpResponse('{lat:user.lat, lng:user.lng}')

def getall(request):
	user = Users.objects.get(id = request.session['user_id'])
	user.lat = request.POST['lat']
	user.lng = request.POST['lng']
	user.save()
	boba = query_api("boba", request.POST['city'])
	boba = json.dumps(boba)
	print user.lat, user.lng
	return HttpResponse(boba)


def profile(request, user_id):
	friend = request.POST.get('search', False)
	search = Users.objects.filter(Q(name__icontains = friend))
	context = {
		"user": Users.objects.get(id=request.session['user_id']),
		"places": TimesDrugged.objects.filter(user_id = request.session['user_id']),
		"friends": Friendslist.objects.filter(user_friend_id = request.session['user_id']),
		"searches": search
	}
	return render(request, 'track_boba/user_profile.html', context)

def add_friend(request, user_id):
	my_id = str(request.session['user_id'])
	user = Users.objects.get(id = request.session['user_id'])
	friend = Users.objects.get(id = user_id)
	Friendslist.objects.create(user_friend = user, friend = friend)
	return redirect('/profile/'+my_id+'')

def logout(request):
	user = Users.objects.get(id=request.session['user_id'])
	request.session['user_id'] = 0
	return redirect('/')