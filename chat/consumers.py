from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
import base64
import json
import secrets
from channels.db import database_sync_to_async
from .serializers import *

from .models import *
class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        self.room_name=self.scope['url_route']["kwargs"]["room_name"]
        self.room_group_name=f"chat_{self.room_name}"
        self.user=self.scope["user"]
 
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)

        await self.send({
        "type":"websocket.accept"
        })

    async def websocket_receive(self,event):
        data=json.loads(event["text"])
       
        message=data["message"]
        print(message)
        await self.channel_layer.group_send(self.room_group_name,{"type":"chat.message","message":message})
    
    async def chat_message(self,event):
        text_data_json=event.copy()
        text_data_json.pop("type")
        message, attachment = (
            text_data_json["message"],
            text_data_json.get("attachment"),
        )
     
        conversation =await database_sync_to_async(Chat.objects.get)(id=int(self.room_name))
        
        sender=self.user

        if attachment:
            file_str, file_ext = attachment["data"], attachment["format"]

            file_data = ContentFile(
                base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}"
            )
            _message =await database_sync_to_async(Message.objects.create) (
                sender=sender,
                attachment=file_data,
                text=message,
                conversation_id=conversation,
            )
        else:
            _message =await database_sync_to_async(Message.objects.create) (
                sender=sender,
                text=message,
                conversation_id=conversation,
            )
        serializer=MessageSerializer(instance=_message)





        await self.send({
        "type":"websocket.send",
        "text":json.dumps(serializer.data)
        })

    async def websocket_disconnect(self,event):

        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)
        raise StopConsumer()

    
