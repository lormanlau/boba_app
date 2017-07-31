# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
from django.core import serializers
from django.http import JsonResponse
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

def getall(request):
	user = Users.objects.get(id = request.session['user_id'])
	user.lat = request.POST['lat']
	user.lng = request.POST['lng']
	user.save()
	boba2 = query_lng("boba", request.POST['lat'], request.POST['lng'])
	boba2 = json.dumps(boba2)
	print boba2
	# boba = query_api("boba", request.POST['city'])
	# boba = json.dumps(boba)
	print user.lat, user.lng
	return HttpResponse(boba2)


def profile(request, user_id):
	
	context = {
		"user": Users.objects.get(id=request.session['user_id']),
		"places": TimesDrugged.objects.filter(user_id = request.session['user_id']),
		"friends": Friendslist.objects.filter(user_friend_id = request.session['user_id']),
	}
	return render(request, 'track_boba/user_profile.html', context)

def search(request):
	if request.method == "POST":
		friend = request.POST.get('search', False)
		search = Users.objects.filter(Q(name__icontains = friend)).exclude(friendslist__user_friend__id = request.session['user_id']).exclude(id = request.session['user_id'])
		print search
		if len(search) < 1:
			return HttpResponse("None Found")
		return HttpResponse(serializers.serialize("json", search), content_type='application/json')

def add_friend(request, user_id):
	my_id = str(request.session['user_id'])
	user = Users.objects.get(id = request.session['user_id'])
	friend = Users.objects.get(id = user_id)
	Friendslist.objects.create(user_friend = user, friend = friend)
	return redirect('/profile/'+my_id)

def logout(request):
	user = Users.objects.get(id=request.session['user_id'])
	request.session['user_id'] = 0
	return redirect('/')

def addboba(request):
	
	return HttpResponse('Added')