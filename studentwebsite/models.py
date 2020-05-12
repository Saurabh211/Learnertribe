from django.db import models
from django.conf import settings
from rest_framework.fields import JSONField


class Institute(models.Model):
    institute_code = models.CharField(max_length=100, null=False, blank=False)
    student_code = models.CharField(max_length=100, null=False, blank=False)
    teacher_code = models.CharField(max_length=100, null=False, blank=False)
    institute_name = models.CharField(max_length=40, null=False, blank=False)
    profile_image = models.FileField(max_length=255,upload_to='static/institute_logo')
    is_verified = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.institute_name + " : " + self.institute_code

    class Meta:
        db_table = "institute_info"


class ClassRoom(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=20, null=False, blank=False)
    class_code = models.CharField(max_length=20, null=False, blank=False)
    live_classes = models.BooleanField(default=True)
    videos = models.BooleanField(default=True)
    assignment = models.BooleanField(default=True)
    online_test = models.BooleanField(default=True)
    attendance = models.BooleanField(default=True)

    def __str__(self):
        return self.class_name + " : " + self.class_code

    class Meta:
        db_table = "class_info"


class Subject(models.Model):
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=20, null=False, blank=False)
    subject_code = models.CharField(max_length=20, null=False, blank=False)
    subject_logo = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.subject_name+" : "+self.subject_code

    class Meta:
        db_table = "subject_info"


class Video(models.Model):
    video_sub = models.ForeignKey(Subject, on_delete=models.CASCADE)
    video_name = models.CharField(max_length=40, null=False, blank=False)
    video_url = models.CharField(max_length=400, null=False, blank=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video_name

    class Meta:
        db_table = "video_info"

class LiveClass(models.Model):
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    live_class_name = models.CharField(max_length=40, null=False, blank=False)
    live_class_description = models.CharField(max_length=40, null=False, blank=False)
    meeting_id = models.CharField(max_length=200, null=False, blank=False)
    meeting_URL = models.CharField(max_length=400, null=False, blank=False)
    meeting_start_at = models.DateTimeField(auto_now_add=False)
    meeting_end_at = models.DateTimeField(auto_now_add=False)
    meeting_joining_till = models.DateTimeField(auto_now_add=False,null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.live_class_name

    class Meta:
        db_table = "liveclass_info"

class Assignment(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assisment_name = models.CharField(max_length=100, null=False, blank=False)
    discription = models.CharField(max_length=100, null=False, blank=False)
    assisment_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assignment_pdf = models.FileField(max_length=255,upload_to='static/assignments')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.assisment_name

    class Meta:
        db_table = "assignment_info"

class AssignmentResponse(models.Model):
    assisment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignment_pdf = models.FileField(max_length=255,upload_to='static/assignmentsresposne')
    remark = models.CharField(max_length=40, null=True)
    marks = models.CharField(max_length=40 , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.assisment.assisment_name+" Response"

    class Meta:
        db_table = "assignment_response_info"


class OnlineTest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    testname = models.CharField(max_length=40)
    totalmarks = models.CharField(max_length=25, null=True)
    totalquestion = models.CharField(max_length=45, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = "online_test"


class TestQuestion(models.Model):
    testname = models.ForeignKey(OnlineTest, on_delete=models.CASCADE)
    question = models.CharField(max_length=400)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    answer = models.CharField(max_length=25)
    marks = models.IntegerField()

    class Meta:
        db_table = "test_questions"


class StudentTestResponse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_answer = JSONField()
    obtainedmarks = models.IntegerField(null=True)

    class Meta:
        db_table = "student_answer"

