from __future__ import unicode_literals
from django.db import models
import re
# Create your models here.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
LETTERS_ONLY_REGEX = re.compile(r'^[a-zA-Z]+$')
class UserManager(models.Manager):
	def basic_validator(self, postData):
		errors = {}
		if len(postData['first-name']) < 2 or len(postData['last-name']) < 2:
			errors['name'] = "Names must be at least 3 letters long"
		elif not LETTERS_ONLY_REGEX.match(postData['first-name']) or not LETTERS_ONLY_REGEX.match(postData['last-name']):
			errors['name'] = "Names must be letters only"
		elif not EMAIL_REGEX.match(postData['email']):
			errors['email'] = "Must be a valid email"
		elif len(postData['email']) < 1:
			errors['email'] = "Email can't be blank"
		elif User.objects.filter(email = postData['email']):
			errors['email'] = "Email exists"
		elif postData['password'] != postData['confirm-pw']:
			errors['password'] = "Passwords must match"
		elif postData['password'] < 8:
			errors['password'] = "Passwords must be at least 8 characters match"
		return errors

	def update_validator(self, postData):
		errors = {}
		if len(postData['first-name']) < 2 or len(postData['last-name']) < 2:
			errors['name'] = "Names must be at least 3 letters long"
		elif not LETTERS_ONLY_REGEX.match(postData['first-name']) or not LETTERS_ONLY_REGEX.match(postData['last-name']):
			errors['name'] = "Names must be letters only"
		elif not EMAIL_REGEX.match(postData['email']):
			errors['email'] = "Must be a valid email"
		elif len(postData['email']) < 1:
			errors['email'] = "Email can't be blank"
		elif User.objects.filter(email = postData['email']):
			errors['email'] = "Email exists"
		return errors

class User(models.Model):
	first_name = models.CharField(max_length = 255)
	last_name = models.CharField(max_length = 255)
	email = models.CharField(max_length = 255)
	password_hash = models.CharField(max_length = 255)

	objects = UserManager()


class QuoteManager(models.Manager):
	def basic_validator(self, postData):
		errors = {}
		if len(postData['quote-content']) < 10:
			errors['quote'] = "Quotes must be at least 10 letters long"
		elif len(postData['quote-author']) < 3:
			errors['quote'] = "Quote authors must be at least 3 letters long"
		return errors
class Quote(models.Model):
	content = models.TextField()
	author = models.CharField(max_length = 255)
	likes = models.ManyToManyField(User, related_name = "likes")
	user = models.ForeignKey(User, related_name = "quotes", on_delete = models.CASCADE)

	objects = QuoteManager()