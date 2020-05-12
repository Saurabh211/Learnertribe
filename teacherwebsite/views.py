from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from studentwebsite.models import *

@method_decorator(login_required(login_url = '/auth/login/000001/'),name = 'dispatch')
class TeacherDashbord(View):
	def get(self, request):
		return render(request, "teacherwebsite/dashbord.html")


@method_decorator(login_required(login_url = '/auth/login/000001/'),name = 'dispatch')
class TeachersClass(View):
	def get(self, request, data):
		request.session['action'] = data
		teachers_class = ClassRoom.objects.filter(institute = request.user.institute)
		return render(request, "teacherwebsite/teacher_classes.html" , {'teachers_class' : teachers_class})


@method_decorator(login_required(login_url = '/auth/login/000001/'),name = 'dispatch')
class TeacherSubject(View):
	def get(self, request, id):
		import logging
		logger = logging.getLogger(__name__)

		subjects = Subject.objects.filter(class_room__id = id)
		data = request.session['action']
		return render(request, "teacherwebsite/subject.html", {'subjects':subjects , 'data' : data})


@method_decorator(login_required(login_url = '/auth/login/000001/'),name = 'dispatch')
class LiveClasses(View):
	def get(self, request):
		import logging
		logger = logging.getLogger(__name__)

		live_classes = LiveClass.objects.filter(class_room__institute = request.user.institute)
		return render(request, "teacherwebsite/liveclasses.html", {'liveClasses':live_classes})


@method_decorator(login_required(login_url = '/auth/login/000001/'),name = 'dispatch')
class AddVideos(View):
	def get(self, request, id):
		subject = Subject.objects.get(pk = id)
		query = request.GET.get('start_date')
		try:
			start_date = datetime.strptime((query), "%m/%d/%Y").date()
		except:
			start_date = datetime.now()
		videos =  Video.objects.filter(video_sub__id = id, created_at = start_date)
		return render(request, "teacherwebsite/add_videos.html", {'subject' : subject , 'videos' : videos})

	def post(self, request, id):
		data = request.POST
		id = data['id']
		subject = Subject.objects.get(pk=id)
		Video.objects.create(video_sub = subject, video_name = data['video_name'], video_url = data['video_url'])
		return redirect('/teacher/'+id+'/add_videos')


@method_decorator(login_required(login_url = '/auth/login/000001/'),name = 'dispatch')
class AddAssignment(View):
	def get(self, request, id):
		subject = Subject.objects.get(pk = id)
		query = request.GET.get('start_date')

		start_date = datetime.now()
		assignment =  Assignment.objects.filter(assignment_subject__id = id, created_at__date = start_date)
		return render(request, "teacherwebsite/add_assignment.html", {'subject' : subject , 'assignment' : assignment})

	def post(self, request, id):
		data = request.POST
		try : assignment_pdf = request.FILES['assignment']
		except : assignment_pdf = ''
		id = data['id']
		subject = Subject.objects.get(pk=id)
		Assignment.objects.create(assignment_subject = subject, description = data['description'], assignment_name = data['assignment_name'], assignment_pdf = assignment_pdf , teacher = request.user)
		return redirect('/teacher/'+id+'/add_assignment')

