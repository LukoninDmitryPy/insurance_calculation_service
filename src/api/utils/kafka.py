from kafka import KafkaProducer
from datetime import datetime
import json

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def log_action(user_id: int, action: str):
    message = {
        "user_id": user_id,
        "action": action,
        "timestamp": datetime.now().isoformat()
    }
    producer.send('insurance_logs', message)