from django.shortcuts import render
from django.views.generic import ListView
from .models import News


class NewsList(ListView):
	'''Here I want to render News throught list.html'''
	model = News
	template_name = 'news/list.html'