from channels.generic.websocket import AsyncWebsocketConsumer

import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Connect a new socket and add the channel to the group depend on the room name.
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        # print('url_route', self.scope['url_route'])

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """
        Disconnect a socket.
        """

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive data from WebSocket and send to the channel's group.
        """

        text_data_json = json.loads(text_data)
        try:
            message = text_data_json['message']
            name = text_data_json['name']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'name': name
                }
            )
        except KeyError:
            print('Missing message or name data')

    async def chat_message(self, event):
        """
        Send data from the channel's group to WebSocket.
        """

        message = event['message']
        name = event['name']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'name': name
        }))
