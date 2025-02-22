from kafka import KafkaAdminClient

admin_client = KafkaAdminClient(
    bootstrap_servers="localhost:9092",  # Remplacez par vos brokers
    client_id='my_client'
)

topics = admin_client.list_topics()
print("Topics:", topics)

localhost = "localhost:9091,localhost:9092,localhost:9093"
print(localhost.split(','))