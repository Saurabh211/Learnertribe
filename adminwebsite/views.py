from django.shortcuts import render

from django.contrib.auth import authenticate,login,logout
from datetime import datetime,timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import redirect,render
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse, JsonResponse
import csv
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from authuser.models import User


class LoginView(View):
	def get(self,request):
	    user_obj = request.user
	    try:
	        if user_obj.is_authenticated and user_obj.groups.all()[0].name == 'rental_admin':
	            return redirect('learnertribe_admin:dashboard')
	    except:
	        logout(request)
	    return render(request,'adminwebsite/login.html')

	def post(self , request):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request,username = username,password = password)

		if user:
			group_name = user.groups.all()[0].name
			if group_name == 'learnertribe_admin':
				login(request, user)
				message = 'success'
		else:
		    message = "Username or Password may be incorrect"
		return JsonResponse({'message' : message })


class LogoutView(View):
    def get(self ,request):
        logout(request)
        return redirect('learnertribe_admin:login')

@method_decorator(login_required(login_url = '/learnertribe_admin/login/'),name = 'dispatch')
class Dashboard(View):
	def get(self, request):
		all_teacher = User.objects.filter(groups__name = 'teacher')
		all_student = User.objects.filter(groups__name = 'student')
		total_teacher_count = all_teacher.count()
		total_student_count = all_student.count()

		return render(request,"adminwebsite/dashboard.html" , {'total_teacher_count':total_teacher_count,'total_student_count':total_student_count})

'''
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="userlisting.csv"'
		user_list = request.POST.getlist('user_list')[0].split(',')
		for user_id in user_list:
			user = RentalAppUser.objects.get(id=int(user_id))
			name = user.username
			email = user.email
			mobile_number = user.mobile_number
			gender = user.gender
			dob = user.dob
			business = user.business
			csv_data = (name, email, mobile_number, gender, user.added_on, dob, business)
			writer = csv.writer(response)
			writer.writerow(csv_data)
'''

@method_decorator(login_required(login_url = '/learnertribe_admin/login/'),name = 'dispatch')
class TeacherListing(View):
	def get(self, request):
		query = request.GET.get('search')
		download = request.GET.get('download')
		
		if query:
			query = query.rstrip()
			query = query.lstrip()
			lookups = Q(full_name__contains = query) | Q(email__contains = query)
			total_teacher = User.objects.filter(groups__name = 'teacher').filter(lookups)
		else:
			total_teacher = User.objects.filter(groups__name = 'teacher')
		
		if download:
			response = HttpResponse(content_type = 'text/csv')
			response['Content-Disposition'] = 'attachment; filename = "teacher_listing.csv"'
			fields = ['full_name','email','added_on']
			writer = csv.DictWriter(response,fieldnames = fields)
			writer.writeheader()
			writer.writerows(total_teacher.values('full_name','email','added_on'))
			return response
		
		page = request.GET.get('page','1')
		total_teacher = paginator_class(total_teacher,page)
		request.session["page"] = page
		return render(request, "adminwebsite/total_teacher.html", {'total_teacher': total_teacher})


@method_decorator(login_required(login_url = '/learnertribe_admin/login/'),name = 'dispatch')
class StudentListing(View):
	def get(self, request):
		query = request.GET.get('search')
		download = request.GET.get('download')
		
		if query:
			query = query.rstrip()
			query = query.lstrip()
			lookups = Q(full_name__contains = query) | Q(email__contains = query)
			total_student = User.objects.filter(groups__name = 'merchant', is_verified = True).filter(lookups)
		else:
			total_student = User.objects.filter(groups__name = 'merchant' , is_verified = True)

		if download:
			response = HttpResponse(content_type = 'text/csv')
			response['Content-Disposition'] = 'attachment; filename = "merchant_listing.csv"'
			fields = ['full_name','email','added_on','class']
			writer = csv.DictWriter(response,fieldnames = fields)
			writer.writeheader()
			writer.writerows(total_student.values('full_name','email','added_on','class'))
			return response

		page = request.GET.get('page', '1')
		total_student = paginator_class(total_student, page)
		request.session["page"] = page
		return render(request, "adminwebsite/total_student.html", {'total_student': total_student})


@method_decorator(login_required(login_url = '/learnertribe_admin/login/'),name = 'dispatch')
class UserDelete(View):
	def get(self, request, id):
		User.objects.filter(pk = id).delete()
		return JsonResponse({'message':'success'})

	def post(self, request, id):
		is_verified = int(request.POST['is_verified'])
		instance = User.objects.get(pk = id)
		instance.is_active = is_verified
		instance.save()
		return JsonResponse({'message':'success'})


@method_decorator(login_required(login_url = '/learnertribe_admin/login/'),name = 'dispatch')
class UserDetail(View):
	def get(self, request, id):
		user_obj = User.objects.filter(pk=id)
		return render(request , 'adminwebsite/user_detail.html' , {'user_obj' : user_obj[0]})

	def post(self, request, id):
		instance = User.objects.get(pk=id)
		instance.is_verified = True
		instance.save()
		return JsonResponse({'message': 'success'})


class FetchUsersView(View):
	def post(self, request, *args, **kwargs):
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="userlisting.csv"'
		user_list = request.POST.getlist('user_list')[0].split(',')
		for user_id in user_list:
			user = User.objects.get(id=int(user_id))
			name = user.username
			email = user.email
			mobile_number = user.mobile_number
			gender = user.gender
			dob = user.dob
			business = user.business
			csv_data = (name, email, mobile_number, gender, user.added_on, dob, business)
			writer = csv.writer(response)
			writer.writerow(csv_data)
		return response


@method_decorator(login_required(login_url = '/learnertribe_admin/login/'),name = 'dispatch')
class Notification(View):
	def get(self, request):
		all_users = User.objects.all()
		teacher_listing = all_users.filter(groups__name='teacher', is_verified=False)
		student_listing = all_users.filter(groups__name='student', is_verified=False)
		return render(request, "adminwebsite/notification.html", {'teacher_listing': teacher_listing, 'student_listing' : student_listing})




def paginator_class(users_list,page_no,records_per_page = 25):
    paginator = Paginator(users_list,records_per_page)
    try:
        users = paginator.page(page_no)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return users