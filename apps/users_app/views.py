from django.shortcuts import render, redirect
from django.contrib import messages
from apps.users_app.models import *
import bcrypt

# Create your views here.
def index(request):

	return render(request, "index.html")

def login(request):

	errors = User.objects.login_validator(request.POST)

	if len(errors):
		for key, value in errors.items():
			messages.error(request, value)
			return redirect('/')
	else:
		user = User.objects.get(email=request.POST['email'])

		if bcrypt.checkpw(request.POST['password'].encode(), user.password_hash.encode()):
			if "user" not in request.session:
				request.session['user'] = user.id
			else:
				request.session['user'] = user.id
			if "user-name" not in request.session:
				request.session['username'] = {"firstname" : user.first_name, "lastname" : user.last_name}
			else:
				request.session['username'] = {"firstname" : user.first_name, "lastname" : user.last_name}
			request.session['loggedin'] = True
			return redirect('/welcome')
		else:
			return redirect('/')

def logout(request):

	request.session['loggedin'] = False
	request.session['user'] = 0

	request.session.clear()

	return redirect("/")


def register(request):

	errors = User.objects.basic_validator(request.POST)

	if len(errors):
		for key, value in errors.items():
			messages.error(request, value)
			return redirect('/')
	else:
	
		first_name = request.POST['first-name']
		last_name = request.POST['last-name']
		email = request.POST['email']
		pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

		User.objects.create(first_name = first_name, last_name = last_name, email = email, password_hash = pw_hash )
		user = User.objects.last()
		if "user" not in request.session:
			request.session['user'] = user.id
		else:
			request.session['user'] = user.id
		if "user-name" not in request.session:
			request.session['username'] = {"firstname" : user.first_name, "lastname" : user.last_name}
		else:
			request.session['username'] = {"firstname" : user.first_name, "lastname" : user.last_name}
		request.session['loggedin'] = True
		return redirect('/welcome')

def welcome(request):

	user = User.objects.get(id = request.session['user'])
	likes = user.likes.all()
	# print(request.session["username"]["firstname"])
	print(likes.values())

	quotes = Quote.objects.all()
	
	return render(request, "welcome.html", {"quotes": quotes, "user": user})

def submit(request):

	errors = Quote.objects.basic_validator(request.POST)
	if len(errors):
		for key, value in errors.items():
			messages.error(request, value)
			return redirect('/welcome')
	else:
		content = request.POST['quote-content']
		user = User.objects.get(id = request.session['user'])
		author = request.POST['quote-author']

		Quote.objects.create(content = content, user = user, author = author)

		return redirect('/welcome')

def like(request):

	quote = Quote.objects.get(id = request.POST['quote-id'])
	user = User.objects.get(id = request.session['user'])

	user.likes.add(quote)
	user.save()
	print(user.likes, user.id, quote.id)
	
	return redirect('/welcome')

def show(request,id):

	user = User.objects.get(id = id)
	quotes = Quote.objects.filter(user = user)

	return render(request, "user.html", {'user': user, 'quotes' : quotes})

def userInfo(request):

	user = User.objects.get(id = request.session['user'])

	request.session['email'] = user.email

	return render(request, "update.html", {"user": user})

def submitEdit(request):
	errors = User.objects.update_validator(request.POST)

	if len(errors):
		for key, value in errors.items():
			messages.error(request, value)
			return redirect('/update')

	else:

		user = User.objects.get(id = request.session['user'])

		user.first_name = request.POST['first-name']
		user.last_name = request.POST['last-name']
		
		if request.POST['email'] == request.session['email']:
			request.POST = None

		user.save()

		request.session['username'] = {"firstname" : user.first_name, "lastname" : user.last_name}

		return redirect('/welcome')

def deleteQuote(request, id):

	quote = Quote.objects.get(id = id)

	quote.delete()

	return redirect('/welcome')

