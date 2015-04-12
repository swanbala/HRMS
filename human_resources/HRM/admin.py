from django.contrib import admin
from HRM.models import basic_staff,work_staff,pay,time,exit_staff,sign_note
# Register your models here.

admin.site.register(basic_staff)
admin.site.register(work_staff)
admin.site.register(pay)
admin.site.register(time)
admin.site.register(exit_staff)
admin.site.register(sign_note)

