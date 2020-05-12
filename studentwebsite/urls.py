from .views import *
from django.urls import path

urlpatterns = [
	path('dashboard/', StudentDashbord.as_view(), name='dashboard'),
	path('student_subjects/<slug:data>/', StudentSubject.as_view(), name='student_subjects'),
	path('liveclasses/', LiveClasses.as_view(), name='liveclass'),
	path('<int:id>/videos/', SubjectVideos.as_view(), name='videos'),
	path('videos/more/', SubjectVideosMore.as_view(), name='videos_more'),
	path('<int:id>/assignments/', SubjectAssignments.as_view(), name='student_assignments'),
	path('assignments/more/', SubjectAssignmentsMore.as_view(), name='videos_more'),
	path('<int:id>/assignment_detail/', AssignmentDetail.as_view(), name='assignment_detail'),
	# path('<int:id>/playvideo/', PlayVideo.as_view(), name='playvideo'),
]