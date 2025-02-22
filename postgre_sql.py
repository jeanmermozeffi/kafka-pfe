import json
import os
import time
from kafka import KafkaConsumer
import psycopg2

# Configuration Kafka
TOPIC = os.environ.get('TOPIC', 'foobar')
CONSUMER_GROUP = os.environ.get('CONSUMER_GROUP', 'cg-group-id')
BOOTSTRAP_SERVERS = os.environ.get('BOOTSTRAP_SERVERS', 'localhost:9091,localhost:9092,localhost:9093').split(',')

# Configuration PostgreSQL
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DATABASE = os.getenv('DATABASE', 'vehicle_leplus')
USERNAME = os.getenv('USERNAME', 'admin')
PASSWORD = os.getenv('PASSWORD', 'Admin123')
PORT = os.getenv('POSTGRES_HOST', '5434')
SQL_FILE_PATH = 'sql/create_tables.sql'


def connect_to_postgresql():
    try:
        conn_str = f"dbname={DATABASE} user={USERNAME} password={PASSWORD} host={POSTGRES_HOST} port={PORT}"
        conn = psycopg2.connect(conn_str)
        print("Connexion à la base de données PostgreSQL établie avec succès.")
        return conn
    except Exception as e:
        print("Erreur lors de la connexion à la base de données :", e)
        return None


def execute_sql_script(conn, file_path=SQL_FILE_PATH):
    try:
        cursor = conn.cursor()
        with open(file_path, 'r') as file:
            sql_script = file.read()
            cursor.execute(sql_script)
        conn.commit()
        print("Script SQL exécuté avec succès.")
    except Exception as e:
        print("Erreur lors de l'exécution du script SQL :", e)
    finally:
        if cursor:
            cursor.close()


def store_in_postgresql(vehicle_data_batch, conn):
    if conn is None:
        print("La connexion à la base de données n'est pas établie.")
        return

    # Exécution script SQL de création des tabless
    execute_sql_script(conn, SQL_FILE_PATH)

    try:
        cursor = conn.cursor()

        sql_insert_query = """
        INSERT INTO Vehicule (Marque, Immatriculation, Modele, Annee, Vehicule, Prix, DatePublication)
        VALUES (%s, %s, %s, %s, %s, %s, %s)RETURNING id;
        """

        vehicule_data_list = []
        dimensions_data_list = []

        for vehicle_data in vehicle_data_batch:
            vehicule_data_list.append((
                vehicle_data["Marque"],
                vehicle_data["Immatriculation"],
                vehicle_data["Modele"],
                vehicle_data["Annee"],
                vehicle_data["Vehicule"],
                vehicle_data["Prix"],
                vehicle_data["DatePublication"]
            ))

        # Insertion en batch pour la table Vehicule
        cursor.executemany(sql_insert_query, vehicule_data_list)

        # Récupérer les IDs des véhicules insérés
        cursor.execute("""
            SELECT id, Immatriculation FROM Vehicule
            WHERE Immatriculation IN %s;
        """, (tuple([data["Immatriculation"] for data in vehicle_data_batch]),))

        vehicule_ids_dict = {row[1]: row[0] for row in cursor.fetchall()}

        # Préparer les données de dimensions avec les IDs des véhicules
        for vehicle_data in vehicle_data_batch:
            if vehicle_data.get("Dimensions"):
                dimensions_data = vehicle_data["Dimensions"]

                # Si 'Dimensions' est une chaîne JSON
                if isinstance(dimensions_data, str):
                    dimensions_data = dimensions_data.replace("'", "\"")
                    dimensions_data = json.loads(dimensions_data)

                vehicule_id = vehicule_ids_dict.get(vehicle_data["Immatriculation"])

                dimensions_data_list.append((
                    vehicule_id,
                    dimensions_data.get("longueur"),
                    dimensions_data.get("largeur"),
                    dimensions_data.get("hauteur"),
                    dimensions_data.get("empattement"),
                    dimensions_data.get("reservoir"),
                    dimensions_data.get("porte_a_faux_avant"),
                    dimensions_data.get("porte_a_faux_arriere"),
                    dimensions_data.get("voies_avant"),
                    dimensions_data.get("voies_arriere"),
                    dimensions_data.get("garde_au_sol"),
                    dimensions_data.get("angle_dattaque"),
                    dimensions_data.get("angle_ventral"),
                    dimensions_data.get("angle_de_fuite"),
                    dimensions_data.get("Immatriculation"),
                ))

        # Préparer la requête pour la table Dimensions
        sql_insert_dimensions = """
        INSERT INTO Dimensions (vehicule_id, longueur, largeur, hauteur, empattement, reservoir, porte_a_faux_avant, porte_a_faux_arriere,
                                voies_avant, voies_arriere, garde_au_sol, angle_dattaque, angle_ventral, angle_de_fuite, Immatriculation)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        # Insertion en batch pour la table Dimensions
        if dimensions_data_list:
            cursor.executemany(sql_insert_dimensions, dimensions_data_list)

        # Commit les transactions
        conn.commit()
        print("Données insérées avec succès dans la base de données PostgreSQL.")

    except Exception as e:
        print("Erreur lors de l'insertion des données dans la base de données :", e)
        conn.rollback()  # Annuler la transaction en cas d'erreur
    finally:
        if cursor:
            cursor.close()
