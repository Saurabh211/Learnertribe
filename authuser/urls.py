from .views import *
from django.urls import path

urlpatterns = [
	path('register/', Register.as_view(), name='register'),
	path('login/<slug:institute_code>/', Login.as_view(), name='login'),
	path('home/', Home.as_view(), name='home'),
	path('reset_password/<int:user_id>', ResetPasswordForm.as_view(), name='reset_password'),
	path('logout/', logout_view, name='logout'),
]
