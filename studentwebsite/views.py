from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.utils.decorators import method_decorator
from studentwebsite.models import *


@method_decorator(login_required(login_url = '/auth/login/000001/'),name = 'dispatch')
class StudentDashbord(View):
	def get(self, request, *args, **kwargs):
		return render(request, "studentwebsite/dashbord.html")

@method_decorator(login_required(login_url = '/auth/login/000001/'),name = 'dispatch')
class StudentSubject(View):
	def get(self, request, data):
		import logging
		logger = logging.getLogger(__name__)

		request.session['action'] = data
		subjects = Subject.objects.filter(class_room = request.user.class_room)
		return render(request, "studentwebsite/subject.html", {'subjects':subjects, 'data' : data})

@method_decorator(login_required(login_url = '/auth/login/000001/'),name = 'dispatch')
class SubjectVideos(View):

	def get(self, request, id):
		#import pdb; pdb.set_trace();

		vidSubject = Subject.objects.filter(id=id)
		start_date = datetime.today()

		videos = Video.objects.filter(video_sub__id = id , created_at__date = start_date)
		formatted_date = datetime.strftime(start_date, "%m/%d/%Y")
		return render(request, "studentwebsite/videos.html", {'subject':vidSubject[0],'videos' : videos,'filterDate':formatted_date})

class SubjectVideosMore(View):
	def post(self, request, *args, **kwargs):
		data = request.POST
		try:
			subject_id = data['subject_id']
			filter_date = data['filter_date']

			start_date = datetime.strptime((filter_date), "%m/%d/%Y").date()
			videos = Video.objects.filter(video_sub__id=subject_id, created_at__date=start_date)
			videoList = []
			for v in videos:
				videoList.append({'id':v.id, 'video_name':v.video_name})
			status = "Success"
		except:
			status = "Error"
		return JsonResponse({"status": status, 'videos':videoList}, safe=False)


@method_decorator(login_required(login_url = '/auth/login/000001/'),name = 'dispatch')
class PlayVideo(View):
	def get(self, request, id):
		import logging
		logger = logging.getLogger(__name__)

		video = Video.objects.filter(id = id )
		return render(request, "studentwebsite/playvideo.html", {'video':video[0]})


@method_decorator(login_required(login_url = '/auth/login/000001/'),name = 'dispatch')
class LiveClasses(View):
	def get(self, request, *args, **kwargs):
		import logging
		logger = logging.getLogger(__name__)

		start_date = datetime.today()
		live_classes = LiveClass.objects.filter(class_room=request.user.class_room, meeting_start_at__date=start_date)
		return render(request, "studentwebsite/liveclasses.html", {'liveClasses':live_classes})


@method_decorator(login_required(login_url = '/auth/login/000001/'),name = 'dispatch')
class SubjectAssignments(View):
	def get(self, request, id):
		assignSubject = Subject.objects.filter(id=id)
		start_date = datetime.today()

		assignments = Assignment.objects.filter(assisment_subject__id = id, created_at__date = start_date)
		formatted_date = datetime.strftime(start_date, "%m/%d/%Y")
		return render(request, "studentwebsite/assignments.html", {'subject':assignSubject[0], 'assignments':assignments,'filterDate':formatted_date})

class SubjectAssignmentsMore(View):
	def post(self, request, *args, **kwargs):
		import logging
		logger = logging.getLogger(__name__)
		data = request.POST
		try:
			subject_id = data['subject_id']
			filter_date = data['filter_date']

			start_date = datetime.strptime((filter_date), "%m/%d/%Y").date()
			assignments = Assignment.objects.filter(assisment_subject__id=subject_id, created_at__date=start_date)
			assignmentList = []
			for v in assignments:
				assignmentList.append({'id':v.id, 'assisment_name':v.assisment_name})
			status = "Success"
		except:
			status = "Error"
		return JsonResponse({"status": status, 'assignments':assignmentList}, safe=False)

class AssignmentDetail(View):
	def get(self, request, id):
		assignment = Assignment.objects.filter(pk = id)
		return render(request, "studentwebsite/assignment_detail.html", {'assignment':assignment[0]})

	def post(self, requset, id):
		assignments = Assignment.objects.filter(pk=id)
		try : answersheet = requset.FILES['answersheet']
		except : answersheet = ''
		AssignmentResponse.objects.create(assisment = assignments[0], student = requset.user, assignment_pdf = answersheet)
		return render(requset, 'studentwebsite/dashbord.html')