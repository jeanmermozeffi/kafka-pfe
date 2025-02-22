from kafka import KafkaProducer
import json

# Configuration du producteur Kafka
bootstrap_servers = 'localhost:9092'
topic_name = 'test'

# value_serializer=lambda v: json.dumps(v).encode('utf-8')

# Création du producteur Kafka
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: v.encode('utf-8')
)


# Fonction pour envoyer un message au topic Kafka
def send_message(message):
    producer.send(topic_name, message)
    producer.flush()


for i in range(1, 10):
    message = f"Bonjour, tu as un nouveau Message KafkaProducer #{i}"
    send_message(message)