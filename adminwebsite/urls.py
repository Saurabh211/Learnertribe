from .views import *
from django.urls import path

app_name = 'learnertribe_admin'

urlpatterns = [
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('dashboard/', Dashboard.as_view(), name = 'dashboard'),
    path('teacher_listing/', TeacherListing.as_view(), name = 'teacher_listing'),
    path('student_listing/', StudentListing.as_view(), name = 'student_listing'),
    path('user_delete/<int:id>/', UserDelete.as_view(), name = 'user_delete'),
    path('user_detail/<int:id>/', UserDetail.as_view(), name = 'user_detail'),
    path('liveclass_listing/', LiveClassListing.as_view(), name = 'liveclass_listing'),
    path('liveclass_add/', LiveClassListing.as_view(), name = 'liveclass_add'),
    path('liveclass_delete/<int:id>/', LiveClassDelete.as_view(), name = 'liveclass_delete'),
    path('notifications/', Notification.as_view(), name='notifications'),
    path('manage_videos/', VideoListing.as_view(), name = 'videos_listing'),
    path('video_action/', VideoListing.as_view(), name = 'videos_listing_action'),
    path('manage_assignments/', AssignmentListing.as_view(), name = 'assignments_listing'),
    path('assignment_action/', AssignmentListing.as_view(), name = 'assignment_listing_action'),
    path('subject_listing/<int:id>/', SubjectListing.as_view(), name = 'subject_listing'),
    path('add_test/', AddTest.as_view(), name='add_test'),
    path('add_test_question/<int:id>', AddTestQuestion.as_view(), name='add_test_question'),
    path('subject/<slug:code>/', ChooseSubject.as_view(), name='subject'),
]
