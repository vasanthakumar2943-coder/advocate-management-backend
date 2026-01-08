from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]

        if not user or user.is_anonymous:
            await self.close()
            return

        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        await self.send(text_data=json.dumps({
            "message": message,
            "user": self.scope["user"].username
        }))
