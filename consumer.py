# https://kafka-python.readthedocs.io/en/master/#kafkaproducer
import json
import os
import time
from datetime import datetime
from kafka import KafkaConsumer
from postgre_sql import connect_to_postgresql, store_in_postgresql

TOPIC = os.environ.get('TOPIC', 'vehicle_data')
CONSUMER_GROUP = os.environ.get('CONSUMER_GROUP', 'cg-group-id')
BOOTSTRAP_SERVERS = os.environ.get('BOOTSTRAP_SERVERS', 'localhost:9092,localhost:9093,localhost:9094').split(',')

BATCH_SIZE = 50


def setup_consumer():
    try:
        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=BOOTSTRAP_SERVERS,
            # auto_offset_reset='latest',  # Consommer les nouveaux messages
            auto_offset_reset='earliest',  # Consommer les anciens messages
            enable_auto_commit=True,
            group_id=CONSUMER_GROUP,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        print("Consumer is ready !")
        return consumer
    except Exception as e:
        if e == 'NoBrokersAvailable':
            print('waiting for brokers to become available')
        print(f'Error setting up producer: {e}')
        return 'not-ready'


def time_delta(received_time):
    now = datetime.now().strftime("%s")
    return int(now) - received_time


def main():
    # Établir la connexion à la base de données
    conn = connect_to_postgresql()
    if conn is None:
        return

    # Configurer le consumer Kafka
    print('starting consumer, checks if brokers are availabe')
    consumer = 'not-ready'

    while consumer == 'not-ready':
        print('Kafka brokers are not ready.')
        time.sleep(5)
        consumer = setup_consumer()

    print('Démarrage de la consommation des messages Kafka...')

    vehicules_a_insert = []

    iteration_count = 0
    for message in consumer:
        try:
            vehicle_data = message.value
            print(vehicle_data)
            vehicules_a_insert.append(vehicle_data)

            if len(vehicules_a_insert) >= BATCH_SIZE or iteration_count % BATCH_SIZE == 0:
                store_in_postgresql(vehicules_a_insert, conn)
                vehicules_a_insert.clear()
        except Exception as e:
            print("Exception lors de la consommation du message ou de l'insertion dans la base de données")
            print(e)

    # Gérer les restes
    if vehicules_a_insert:
        store_in_postgresql(vehicules_a_insert, conn)

    # Fermer la connexion à la base de données
    conn.close()
    print("Connexion fermée avec PostgreSQL")


if __name__ == "__main__":
    main()
