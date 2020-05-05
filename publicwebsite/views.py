from django.shortcuts import render
from django.views import View

class PublicHome(View):
	def get(self, request, *args, **kwargs):
		return render(request, "publicwebsite/home.html")


class PublicAboutUs(View):
	def get(self, request, *args, **kwargs):
		return render(request, "publicwebsite/about_us.html")