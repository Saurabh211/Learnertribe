from django.contrib.auth.models import AbstractUser
from django.db import models
from studentwebsite.models import *


class User(AbstractUser):
	institute = models.ForeignKey(Institute, on_delete=models.CASCADE,null=True, blank=True)
	class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE,null=True, blank=True)
	full_name = models.CharField(max_length=100, null=False, blank=False)
	mobile_number = models.CharField(max_length=20, null=False, blank=False)
	readable_password = models.CharField(max_length=45, null=True, blank=True)
	is_verified = models.BooleanField(default=False)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now_add = True)

	class Meta:
		db_table = "user_info"

# Model to store the list of logged in users
class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username