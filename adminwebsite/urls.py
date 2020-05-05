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
    path('fetch-users/', FetchUsersView.as_view(), name='fetch-users'),
    path('notifications/', Notification.as_view(), name='notifications'),

]
