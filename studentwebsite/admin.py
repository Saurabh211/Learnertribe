from django.contrib import admin
from studentwebsite.models import *

class InstituteAdmin(admin.ModelAdmin):
    list_display = ('institute_name', 'institute_code', 'student_code','teacher_code','created_at')
    # list_filter=('institute_name','institute_code')
admin.site.register(Institute,InstituteAdmin)

class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('institute', 'class_name','class_code')
    list_filter=('institute','class_name','class_code')
admin.site.register(ClassRoom,ClassRoomAdmin)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('class_room','subject_name','subject_code','subject_logo')
    list_filter=('class_room','subject_name','subject_code')
admin.site.register(Subject,SubjectAdmin)

class VideoAdmin(admin.ModelAdmin):
    list_display = ('video_name','video_sub','created_at')
    list_filter=('video_name','video_sub','created_at')
admin.site.register(Video,VideoAdmin)

class LiveClassAdmin(admin.ModelAdmin):
    list_display = ('live_class_name','class_room', 'meeting_start_at')
    list_filter=('live_class_name','class_room','meeting_start_at')
admin.site.register(LiveClass,LiveClassAdmin)

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('assisment_name','assisment_subject','teacher','created_at')
    list_filter=('assisment_name','assisment_subject','teacher','created_at')
admin.site.register(Assignment,AssignmentAdmin)

class AssignmentResponseAdmin(admin.ModelAdmin):
    list_display = ('student','assisment', 'created_at')
    list_filter=('student','assisment','created_at')
admin.site.register(AssignmentResponse,AssignmentResponseAdmin)