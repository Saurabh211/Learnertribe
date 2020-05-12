from .views import *
from django.urls import path

urlpatterns = [
	path('dashboard/', TeacherDashbord.as_view(), name='dashboard'),
	path('teacher_classes/<slug:data>/', TeachersClass.as_view(), name='teacher_classes'),
	path('liveclasses/', LiveClasses.as_view(), name='liveclass'),
	path('<int:id>/subject/', TeacherSubject.as_view(), name='subject'),
	path('<int:id>/add_videos/', AddVideos.as_view(), name='add_videos'),
	path('<int:id>/add_assignment/', AddAssignment.as_view(), name='add_assignment'),
	path('<int:id>/assignment_response/', ResponseAssignment.as_view(), name='assignment_response'),
	# path('<int:id>/remark/', Remark.as_view(), name='remark'),
]
