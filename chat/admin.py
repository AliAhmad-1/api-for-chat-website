from django.contrib import admin
from .models import *



@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display=['sender','text','attachment','conversation_id','timestamp']


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display=['id','sender','recevier','start_time']