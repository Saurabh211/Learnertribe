from .views import *
from django.urls import path

urlpatterns = [
    path('', PublicHome.as_view(), name='dashboard'),
	path('about_us/', PublicAboutUs.as_view(), name='subject'),
]