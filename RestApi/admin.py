from django.contrib import admin
from .models import poll,Choices,Answers,DiscussionThread
# Register your models here.
admin.site.register(poll)
admin.site.register(Choices)
admin.site.register(Answers)
admin.site.register(DiscussionThread)
