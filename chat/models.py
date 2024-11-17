from django.db import models
from django.conf import settings



class Chat(models.Model):
    sender=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,related_name='chat_starter')
    recevier=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name="chat_participant")
    start_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username+":"+self.recevier.username

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              null=True, related_name='message_sender')
    text = models.CharField(max_length=200, blank=True)
    attachment = models.FileField(blank=True)
    conversation_id = models.ForeignKey(Chat, on_delete=models.CASCADE,)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)


    def __str__(self):
        return self.text