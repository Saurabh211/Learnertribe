from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from studentwebsite.models import *
from authuser.models import User


class Home(View):
	def get(self, request, *args, **kwargs):
		return render(request, "authuser/homepage.html")

class Register(View):
	def post(self, request, *args, **kwargs):
		data = request.POST
		if data['user_role'] == 'student':
			try :
				institute_code = Institute.objects.get(student_code = data['code'])
			except :
				info = 'Please enter a valid institute code.'
				return JsonResponse({"message": info})

			try :
				class_room_code = ClassRoom.objects.get(class_code = data['class_code'] , institute = institute_code)
			except :
				info = 'Please enter a valid class room code.'
				return JsonResponse({"message": info})
			if institute_code:
					try:
						instance = User.objects.create_user(username = data['email'], email = data['email'], mobile_number = data['mobile_number'], full_name = data['full_name'], password = data['password'], class_room = class_room_code, institute = institute_code )
						info = 'success'

						try:
							group_obj = Group.objects.get(name='student')
							instance.groups.add(group_obj)
						except:
							info = 'Something went wrong. Please try again or contact administrator.'
					except:
						info="This username already exists."

		else:
			try :
				institute_code = Institute.objects.get(teacher_code = data['code'])
			except :
				institute_code = ''
				info = 'Please enter a valid institute code.'

			if institute_code:
					try:
						instance = User.objects.create_user(username = data['email'], email = data['email'], mobile_number = data['mobile_number'], full_name = data['full_name'], password = data['password'], institute = institute_code )
						info = 'success'

						try:
							group_obj = Group.objects.get(name='teacher')
							instance.groups.add(group_obj)
						except:
							info = 'Something went wrong. Please try again or contact administrator.'
					except:
						info="This username already exists."
		return JsonResponse({"message": info})


class Login(View):
	def get(self, request, institute_code):
		if request.user.is_authenticated:
			user_group = request.user.groups.all()[0].name
			if user_group == 'teacher':
				return redirect('/teacher/dashboard/')
			elif user_group == 'student':
				return redirect('/student/dashboard/')
			elif user_group == 'institute_admin':
				return redirect('/admin/dashboard/')
			else:
				logout(request)
				return redirect('/auth/login/' + institute_code + '/')
		else:
			try :
				institute_code = Institute.objects.get(institute_code = institute_code)
			except :
				institute_code = '000001'
			return render(request, "authuser/signup.html" , {'institute_code' : institute_code})

	def post(self, request, institute_code):
		data = request.POST
		redirect_to = ''
		try:
			user_obj = authenticate(username=data['username'], password=data['password'])
			if user_obj is not None:
				if user_obj.is_verified:
					login(request, user_obj)
					user_group = user_obj.groups.all()[0].name
					if user_group == 'teacher':
						redirect_to = '/teacher/dashboard/'
					elif user_group == 'student':
						redirect_to = '/student/dashboard/'
					elif user_group == 'admin':
						redirect_to = '/admin/dashboard/'

					info = 'success'
				else:
					info="User verification is pending for this user. Please contact system administrator for verification."
			else:
				info = "Invalid username or password."
		except:
			info = "something went wrong. Please try again."
		return JsonResponse({"message": info,'redirect_to': redirect_to}, safe=False)


class ResetPasswordForm(View):
	def get(self, request, user_id, *args, **kwargs):
		return render(request, "user/reset_password.html", {'user_id': user_id})

def logout_view(request):
	if request.user.is_authenticated:
		institute_id = request.user.institute.institute_code
		logout(request)
		return redirect('/auth/login/' + institute_id + '/')
	else:
		return redirect('/auth/login/000001/')
