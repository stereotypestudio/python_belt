from django.urls import path
from . import views

urlpatterns = [
	path('', views.index),
	path('login', views.login),
	path('logout', views.logout),
	path('register', views.register),
	path('welcome', views.welcome),
	path('submit', views.submit),
	path('like', views.like),
	path('<id>/user', views.show),
	path('update', views.userInfo),
	path('submitEdit', views.submitEdit),
	path('deleteQuote', views.deleteQuote),
]