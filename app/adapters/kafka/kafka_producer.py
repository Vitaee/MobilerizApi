from kafka import KafkaProducer as KP
from app.core.config import settings
import json


class KafkaProducerAdapter:
    def __init__(self):
        self.producer = KP(
            bootstrap_servers=[ settings.KAFKA_BOOTSTRAP_SERVERS ],
            api_version=(0,11,5),
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda v: json.dumps(v).encode('utf-8'),
        )
    
    def send_message(self, topic: str, key: str, message: dict):
        self.producer.send(topic, message)
        self.producer.flush()
        future = self.producer.send(topic, key=key, value=message)
        try:
            record_metadata = future.get(timeout=10)
            # Log success if necessary
            print(f"Message sent to {record_metadata.topic} partition {record_metadata.partition}")
        except Exception as e:
            # Handle exceptions (e.g., log the error)
            print(f"Error sending message to Kafka: {e}")
    
    def close(self):
        self.producer.flush()
        self.producer.close()