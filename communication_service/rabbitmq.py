# rpc_client.py

import pika
import uuid
import json
from django.conf import settings


class RpcClient:
    def __init__(self):
    
        self.routing_key =  'communication_queue'
        self.connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
        self.channel = self.connection.channel()
        self.callback_queue = self.channel.queue_declare(queue='', exclusive=True).method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = body

    def call(self, payload):
        
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.routing_key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(payload)
        )

        while self.response is None:
            self.connection.process_data_events()

        try:
            return json.loads(self.response)
        except json.JSONDecodeError:
            return self.response
