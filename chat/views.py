from django.shortcuts import render,redirect
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from accounts.models import User
from .models import *
from django.db.models import Q
from rest_framework.response import Response
from .serializers import *
from django.urls import reverse
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
class StartChat(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        data=request.data
        username=data['username']
     
        try:
            participant=User.objects.get(username=username)
        except User.DoesNotExist:
            raise({'message':'You cannot chat with a non existent user'})
        
        conversation=Chat.objects.filter(Q(sender=request.user,recevier=participant)|Q(sender=participant,recevier=request.user))
        
        if conversation.exists():
            return redirect(reverse('get_conversation', args=(conversation[0].id,)))
        else:
            conversation=Chat.objects.create(sender=request.user,recevier=participant)
            return Response(ChatSerializer(instance=conversation).data)


class get_conversation(APIView):
    def get(self,request,chat_id,format=None):
        conversation=Chat.objects.filter(id=chat_id)
        if not conversation.exists():
            return Response({'message': 'Conversation does not exist'})

        else:
            serializer = ChatSerializer(instance=conversation[0])
            return Response(serializer.data)


class Conversations(ListAPIView):
    serializer_class=ChatListSerializer

    def get_queryset(self):
        chats=Chat.objects.filter(Q(sender=self.request.user)|Q(recevier=self.request.user))
        return chats
    
    
    