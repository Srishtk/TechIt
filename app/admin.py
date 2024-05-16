from django.contrib import admin
from .models import *

class WhatYouLearn_TabularInline(admin.TabularInline):
    model = WhatYouLearn

class Requirements_TabularInline(admin.TabularInline):
    model = Requirements

class Video_TabularInline(admin.TabularInline):
    model = Video
class CourseAdmin(admin.ModelAdmin):
    inlines = (WhatYouLearn_TabularInline , Requirements_TabularInline, Video_TabularInline)

admin.site.register(Categories)
admin.site.register(Course,CourseAdmin)
admin.site.register(Organisation)
admin.site.register(Level)
admin.site.register(WhatYouLearn)
admin.site.register(Requirements)
admin.site.register(Lesson)
admin.site.register(UserCourse)
admin.site.register(Review)

# Register your models here.
