from django.urls import path
from . import views
urlpatterns = [
    path('start/', views.StartChat.as_view(), name='start_convo'),
    path('<int:chat_id>/', views.get_conversation.as_view(), name='get_conversation'),
    path('', views.Conversations.as_view(), name='conversations')
]
