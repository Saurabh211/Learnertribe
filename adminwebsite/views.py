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

from studentwebsite.models import *

from authuser.models import User


class LoginView(View):
	def get(self,request):
		user_obj = request.user
		try:
			if user_obj.is_authenticated and user_obj.groups.all()[0].name == 'institute_admin':
				return redirect('learnertribe_admin:dashboard')
		except:
			logout(request)
		return render(request,'adminwebsite/login.html')

	def post(self , request):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request,username = username,password = password)
		message = ''
		if user:
			group_name = user.groups.all()[0].name
			if group_name == 'institute_admin':
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
		all_teacher = User.objects.filter(institute = request.user.institute, groups__name = 'teacher')
		all_student = User.objects.filter(institute = request.user.institute, groups__name = 'student')
		total_teacher_count = all_teacher.count()
		total_student_count = all_student.count()

		return render(request,"adminwebsite/dashboard.html" , {'total_teacher_count':total_teacher_count,'total_student_count':total_student_count})


@method_decorator(login_required(login_url = '/learnertribe_admin/login/'),name = 'dispatch')
class Notification(View):
	def get(self, request):
		all_users = User.objects.all().order_by('-id')
		teacher_listing = all_users.filter(institute = request.user.institute, groups__name='teacher', is_verified=False)[:20]
		student_listing = all_users.filter(institute = request.user.institute, groups__name='student', is_verified=False)[:20]
		return render(request, "adminwebsite/notification.html", {'teacher_listing': teacher_listing, 'student_listing' : student_listing})


@method_decorator(login_required(login_url = '/learnertribe_admin/login/'),name = 'dispatch')
class TeacherListing(View):
	def get(self, request):
		query = request.GET.get('search')
		download = request.GET.get('download')

		if query:
			query = query.rstrip()
			query = query.lstrip()
			lookups = Q(full_name__contains = query) | Q(email__contains = query)
			total_teacher = User.objects.filter(institute = request.user.institute, groups__name = 'teacher', is_verified = True).filter(lookups)
		else:
			total_teacher = User.objects.filter(institute = request.user.institute, groups__name = 'teacher', is_verified = True)

		if download:
			response = HttpResponse(content_type = 'text/csv')
			response['Content-Disposition'] = 'attachment; filename = "teacher_listing.csv"'
			fields = ['full_name','email','created_at']
			writer = csv.DictWriter(response,fieldnames = fields)
			writer.writeheader()
			writer.writerows(total_teacher.values('full_name','email','created_at'))
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
			total_student = User.objects.filter(institute = request.user.institute, groups__name = 'student', is_verified = True).filter(lookups)
		else:
			total_student = User.objects.filter(institute = request.user.institute, groups__name = 'student' , is_verified = True)

		if download:
			response = HttpResponse(content_type = 'text/csv')
			response['Content-Disposition'] = 'attachment; filename = "student_listing.csv"'
			fields = ['full_name','email','created_at']
			writer = csv.DictWriter(response,fieldnames = fields)
			writer.writeheader()
			writer.writerows(total_student.values('full_name','email','created_at'))
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
		instance.is_verified = is_verified
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


@method_decorator(login_required(login_url = '/learnertribe_admin/login/'),name = 'dispatch')
class LiveClassListing(View):
	def get(self, request):
		live_classes = LiveClass.objects.filter(class_room__institute = request.user.institute).order_by('-id')[:20]
		classList = ClassRoom.objects.filter(institute=request.user.institute)
		return render(request, "adminwebsite/live_classes.html", {'liveClasses':live_classes, 'classList':classList})

	def post(self, request):
		classRoom = request.POST['classRoom']
		title = request.POST['title']
		description = request.POST['description']
		startTimeString = request.POST['startTime']
		startTime = datetime.strptime((startTimeString), "%m/%d/%Y %H:%M:%S")
		duration = int(request.POST['duration'])
		endTime = startTime + timedelta(hours=duration)
		meeting_url = request.POST['meeting_url']

		liveClassRoom = ClassRoom.objects.filter(pk=classRoom)
		LiveClass.objects.create(class_room=liveClassRoom[0], live_class_name=title, live_class_description=description, meeting_URL=meeting_url, meeting_start_at=startTime, meeting_end_at=endTime )
		return JsonResponse({'message':'success'})

@method_decorator(login_required(login_url = '/learnertribe_admin/login/'),name = 'dispatch')
class LiveClassDelete(View):
	def get(self, request, id):
		LiveClass.objects.filter(pk = id).delete()
		return JsonResponse({'message':'success'})


@method_decorator(login_required(login_url = '/learnertribe_admin/login/'),name = 'dispatch')
class VideoListing(View):
	def get(self, request):
		class_id = request.GET.get('class_id')
		subject_id = request.GET.get('subject_id')

		if class_id and subject_id:
			total_video = Video.objects.filter(video_sub__class_room__id = class_id, video_sub__id = subject_id)
		else:
			total_video = Video.objects.filter(video_sub__class_room__institute = request.user.institute).order_by('-id')[:20]

		all_classes = ClassRoom.objects.filter(institute = request.user.institute)
		all_subjects = []
		if class_id:
			all_subjects = Subject.objects.filter(class_room__pk = class_id)

		page = request.GET.get('page', '1')
		total_video = paginator_class(total_video, page)
		request.session["page"] = page
		return render(request, "adminwebsite/manage_videos.html", {'total_video': total_video, 'all_classes':all_classes, 'all_subjects':all_subjects, 'class_id':class_id, 'subject_id':subject_id })

	def post(self, request):
		action = request.POST['action']
		if action == "Create":
			class_room = request.POST['class']
			subject = request.POST['subect']
			name = request.POST['name']
			key = request.POST['key']

			video_sub = Subject.objects.filter(pk=subject)
			Video.objects.create(video_sub=video_sub[0], video_name=name, video_url=key )
			return JsonResponse({'message':'success'})

		else:
			video_id = request.POST['video_id']
			Video.objects.filter(pk=video_id).delete()
			return JsonResponse({'message': 'success'})


@method_decorator(login_required(login_url = '/learnertribe_admin/login/'),name = 'dispatch')
class AssignmentListing(View):

	def get(self, request):
		class_id = request.GET.get('class_id')
		subject_id = request.GET.get('subject_id')

		if class_id and subject_id:
			total_assignment = Assignment.objects.filter(assignment_subject__id=subject_id)
		else:
			total_assignment = Assignment.objects.filter(assignment_subject__class_room__institute=request.user.institute).order_by('-id')[
						  :20]

		all_classes = ClassRoom.objects.filter(institute=request.user.institute)
		all_subjects = []
		if class_id:
			all_subjects = Subject.objects.filter(class_room__pk=class_id)

		page = request.GET.get('page', '1')
		total_assignment = paginator_class(total_assignment, page)
		request.session["page"] = page
		return render(request, "adminwebsite/manage_assignments.html",
					  {'total_assignment': total_assignment, 'all_classes': all_classes, 'all_subjects': all_subjects,
					   'class_id': class_id, 'subject_id': subject_id})

	def post(self, request):
		action = request.POST['action']
		if action == "Create":
			class_room = request.POST['classname']
			subject = request.POST['subjectname']
			name = request.POST['assignmentname']
			desc = request.POST['assignmentdesc']

			assignment_pdf = request.FILES['assignmentFile']

			assignment_sub = Subject.objects.filter(pk=subject)
			Assignment.objects.create(assignment_subject = assignment_sub [0], assignment_name = name, description = desc, teacher = request.user, assignment_pdf = assignment_pdf )
			return JsonResponse({'message': 'success'})


@method_decorator(login_required(login_url = '/admin/login/'),name = 'dispatch')
class AddTestQuestion(View):
	def get(self, request , id):
		test = OnlineTest.objects.get(pk = id)
		return render(request , 'adminwebsite/add_test_question.html', {'test' : test })

	def post(self, request , id):
		data = request.POST
		test = OnlineTest.objects.get(pk=id)
		TestQuestion.objects.create(testname = test, question = data['question'] , option1 = data['option1'], option2 = data['option2']
		                            , option3 = data['option3'], option4 = data['option4'], answer = data['answer'],  marks = data['marks'])
		id = data['testname'].id
		return redirect('/admin/add_test_question/'+id+'/')



@method_decorator(login_required(login_url = '/admin/login/'),name = 'dispatch')
class AddTest(View):
	def get(self, request):
		tests = OnlineTest.objects.filter().order_by('-created_at')[:10]
		classes = ClassRoom.objects.filter(institute = request.user.institute)
		return render(request , 'adminwebsite/add_test.html', {'tests' : tests, 'classes' : classes})

	def post(self, request):
		data = request.POST
		subject = Subject.objects.filter(subject_name = data['subject'] , class_room__institute = request.user.institute,  class_room__class_code = data['class'] )
		OnlineTest.objects.create(user = request.user, test_subject = subject, testname = data['test_name'], totalmarks =data['totalmarks'], totalquestion = data['totalquestion'])
		return redirect('learnertribe_admin:add_test')



@method_decorator(login_required(login_url = '/learnertribe_admin/login/'),name = 'dispatch')
class SubjectListing(View):
	def get(self, request, id):
		subject_list = list(Subject.objects.filter(class_room__pk = id).values())
		return JsonResponse({'subject_list':subject_list})



def paginator_class(users_list,page_no,records_per_page = 25):
    paginator = Paginator(users_list,records_per_page)
    try:
        users = paginator.page(page_no)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return users




class ChooseSubject(View):
	def get(self, request , code):
		import pdb;pdb.set_trace()
		subject = Subject.objects.filter(class_room__id = code)
		# print(subject)
		return JsonResponse({"subject" : subject})


