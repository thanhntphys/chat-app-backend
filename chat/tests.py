from django.conf.urls import url
from django.test import TestCase

from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter

from .consumers import ChatConsumer

import json


application = URLRouter([
    url(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
])


class TestChatConsumer(TestCase):
    """
    Test class Consumer.
    """

    def setUp(self):
        """
        Setting up for the test
        """
        self.room = 'testroom'
        self.json_data = {
            'message': "testmessage",
            'name': "testname"
        }

    async def test_connect_disconnect(self):
        """
        Test can connect to server by WebSocket.
        """
        communicator = WebsocketCommunicator(application, f"/ws/chat/{self.room}/")
        connected, _ = await communicator.connect()

        self.assertEqual(connected, True)
        
        await communicator.disconnect()

    async def test_receive_chat_message(self):
        """
        Test data received is same as data sent.
        """
        communicator = WebsocketCommunicator(application, f"/ws/chat/{self.room}/")
        connected, _ = await communicator.connect()

        await communicator.send_json_to(self.json_data)
        response = await communicator.receive_from()
        response_json_data = json.loads(response)
        self.assertJSONEqual(response, response_json_data)

        await communicator.disconnect()
