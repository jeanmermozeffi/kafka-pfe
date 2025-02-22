import json
import os
import time
import pandas as pd
from kafka import KafkaProducer
import data_cleaning as clr

# Charger votre dataframe ici
path = "/Users/jeanmermozeffi/DataspellProjects/GaoPimcore/Data/Fiches Technical Details/liste_fiches_technical_details.csv"
df = pd.read_csv(path)

# Application des fonctions de nettoyage et de transformation
df = (df.pipe(clr.clean_prix_column)
      .pipe(clr.convert_to_date)
      .pipe(clr.convert_column_to_int, 'Annee')
     )

TOPIC = os.environ.get('TOPIC', 'vehicle_data')
BOOTSTRAP_SERVERS = os.environ.get('BOOTSTRAP_SERVERS', 'localhost:9092,localhost:9093,localhost:9094').split(',')


def create_vehicle_message(row):
    message = {
        "Marque": row['Marque'],
        "Modele": row['Modele'],
        "Annee": row['Annee'],
        "Vehicule": row['Vehicule'],
        "Prix": row['Prix'],
        "DatePublication": row['Date Publication'],
        "Resumer": row['Resumer'],
        "Dimensions": row['Dimensions'],
        "Weight": row['Weight'],
        "Habitability": row['Habitability'],
        "Tires": row['Tires'],
        "Engine": row['Engine'],
        "Transmission": row['Transmission'],
        "Technical": row['Technical'],
        "Performance": row['Performance'],
        "Consumption": row['Consumption'],
        "GalleryImages": row['Gallery Images'],
        "Immatriculation": row['Immatriculation']
    }
    return message


def setup_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            request_timeout_ms=120000
            # enable_idempotence=True  # Activer l'idempotence
        )
        print("Producer setup successful.")
        return producer
    except Exception as e:
        if e == 'NoBrokersAvailable':
            print('waiting for brokers to become available')
        print(f'Error setting up producer: {e}')
        return 'not-ready'


if __name__ == "__main__":
    print('setting up producer, checking if brokers are available')
    producer = 'not-ready'

    while producer == 'not-ready':
        print('brokers not available yet')
        time.sleep(5)
        producer = setup_producer()

    print('brokers are available and ready to produce messages')
    count = 0
    for _, row in df.iterrows():
        json_message = create_vehicle_message(row)
        registration_key = json_message['Immatriculation']
        producer.send(TOPIC, json_message, key=bytes(registration_key, 'utf-8'))
        # print(f'Message sent to Kafka for vehicle {row["Marque"]} {row["Modele"]} with year {row["Annee"]}')
        time.sleep(2)
        count += 1
        if count == 200:
            print(f"{count} Données traitées !")
            break

    producer.close()
