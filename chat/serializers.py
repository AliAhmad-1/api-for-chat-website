from rest_framework import serializers
from .models import *
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Message
        exclude=('conversation_id',)

class ChatListSerializer(serializers.ModelSerializer):
    sender=serializers.StringRelatedField()
    recevier=serializers.StringRelatedField()
    last_message=serializers.SerializerMethodField()
    class Meta:
        model=Chat
        fields=['sender','recevier','last_message']

    def get_last_message(self,obj):
        last_message=obj.message_set.first()
        if last_message:
            message_data = {
            'text': last_message.text,
            'attachment':last_message.attachment or '',
            'timestamp':last_message.timestamp
        }
            return message_data
        else:
            return None

class ChatSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    recevier = UserSerializer()
    message_set = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = ['sender', 'recevier', 'message_set']