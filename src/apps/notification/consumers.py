import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class NotificationConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = None
        self.user_group_name = None

    def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user_group_name = f'notification_{self.user_id}'

        # Accept the connection
        self.accept()
        # Join the group
        async_to_sync(self.channel_layer.group_add)(
            self.user_group_name,
            self.channel_name
        )

    def disconnect(self, code):
        # Leave the group
        async_to_sync(self.channel_layer.group_discard)(
            self.user_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            try:
                text_data_json = json.loads(text_data)
                message = text_data_json.get('message', '')

                # Send the message to the group
                async_to_sync(self.channel_layer.group_send)(
                    self.user_group_name,
                    {
                        'type': 'send_notification',
                        'message': message,
                    }
                )
            except json.JSONDecodeError:
                # Handle JSON decoding error
                self.send(text_data=json.dumps({'error': 'Invalid JSON'}))

    def send_notification(self, event):
        message = event['message']

        # Send the message to WebSocket
        self.send(text_data=json.dumps({
            'type':'send_notification',
            'message': message
        }))