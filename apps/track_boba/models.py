# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class UsersManager(models.Manager):
	def validate(self, user_data):
		errors = {}
		if len(user_data['name']) < 2:
			errors['name'] = "Name needs to be atleast 2 characters long"
		if len(user_data['pass']) < 8:
			errors['pass'] = "Password must be 8 characters long"
		if user_data['pass'] != user_data['con_pass']:
			errors['pass'] = "Passwords must match"

		return errors

# Create your models here.
class Users(models.Model):
	email = models.EmailField()
	name = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	lat = models.FloatField(null = True)
	lng = models.FloatField(null = True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UsersManager()

class BobaPlaces(models.Model):
	lat = models.FloatField()
	lng = models.FloatField()
	name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True, null = True)
	updated_at = models.DateTimeField(auto_now = True, null = True)

class TimesDrugged(models.Model):
	bobaplace = models.ForeignKey(BobaPlaces)
	user = models.ForeignKey(Users)
	timesDrugged = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

class Friendslist(models.Model):
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	druggie = models.ForeignKey(BobaPlaces)
	user_friend = models.ForeignKey(Users, related_name="friend")
		