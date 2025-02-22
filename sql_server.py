import pyodbc
import os
import sys

SERVER = os.getenv('SERVER', 'localhost')
DATABASE = os.getenv('DATABASE', 'yahoo_finance')
USERNAME = os.getenv('USERNAME', 'SA')
PASSWORD = os.getenv('PASSWORD', 'Admin123')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5434')
DRIVER = os.getenv('DRIVER', 'ODBC Driver 18 for SQL Server')
SSL_SERVER_CERTIFICAT = os.getenv('SSL_SERVER_CERTIFICAT', 'TrustServerCertificate=yes;')


def connect_to_sql_server(SERVER, POSTGRES_PORT, DATABASE, USERNAME, PASSWORD):
    try:
        # Établir la connexion à la base de données SQL Server
        conn_str = (
            f"DRIVER={DRIVER};"
            f"SERVER={SERVER},{POSTGRES_PORT};"
            f"DATABASE={DATABASE};"
            f"UID={USERNAME};"
            f"PWD={PASSWORD};"
            f"{SSL_SERVER_CERTIFICAT}"
        )

        conn = pyodbc.connect(conn_str)
        print("Connexion à la base de données SQL Server établie avec succès.")
        return conn

    except Exception as e:
        # Gestion des erreurs
        print("Erreur lors de la connexion à la base de données :", e)
        return None


def convert_numeric_columns(stock_data):
    # Convertir les colonnes numériques en nombres décimaux
    price = float(stock_data["PriceIntraday"])
    change = float(stock_data["Change"])
    percent_change = float(stock_data["ChangePercent"].strip("%"))  # Retirer le signe % avant de convertir
    volume = float(stock_data["Volume"].rstrip("M")) * 1000000  # Convertir les millions en entier
    avg_vol_3_month = float(stock_data["AvgVol3Month"].rstrip("M")) * 1000000  # Convertir les millions en entier
    market_cap = float(stock_data["MarketCap"].rstrip("B")) * 1000000000  # Convertir les milliards en entier
    pe_ratio = float(stock_data["PERatioTTM"]) if stock_data[
                                                      "PERatioTTM"] != "N/A" else ''  # Gérer le cas où la valeur est 'N/A'

    # Retourner un dictionnaire avec les valeurs converties
    return {
        "Symbol": stock_data["Symbol"],
        "NameSymbol": stock_data["NameSymbol"],
        "PriceIntraday": price,
        "Change": change,
        "ChangePercent": percent_change,
        "Volume": volume,
        "AvgVol3Month": avg_vol_3_month,
        "MarketCap": market_cap,
        "PERatioTTM": pe_ratio,
        "WeekRange": stock_data["WeekRange"]
    }


def store_in_sql_server(stock_data, conn):
    if conn is None:
        print("La connexion à la base de données n'est pas établie.")
        return

    try:
        # Créer un curseur pour exécuter des requêtes SQL
        cursor = conn.cursor()

        # Insérer les données dans la base de données
        stock_data_clean = convert_numeric_columns(stock_data)

        # Construction de la requête SQL d'insertion pour les nouvelles données
        sql_insert_query = """
        INSERT INTO Stock (Marque, Modele, Annee, Vehicule, Prix, DatePublication, Resumer, Dimensions, Weight, Habitability, Tires, Engine, Transmission, Technical, Performance, Consumption, GalleryImages, Immatriculation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        # Exécuter la requête SQL d'insertion
        cursor.execute(sql_insert_query, (
            stock_data_clean["Marque"],
            stock_data_clean["Modele"],
            stock_data_clean["Annee"],
            stock_data_clean["Vehicule"],
            stock_data_clean["Prix"],
            stock_data_clean["DatePublication"],
            stock_data_clean["Resumer"],
            stock_data_clean["Dimensions"],
            stock_data_clean["Weight"],
            stock_data_clean["Habitability"],
            stock_data_clean["Tires"],
            stock_data_clean["Engine"],
            stock_data_clean["Transmission"],
            stock_data_clean["Technical"],
            stock_data_clean["Performance"],
            stock_data_clean["Consumption"],
            stock_data_clean["GalleryImages"],
            stock_data_clean["Immatriculation"]
        ))

        # Valider et confirmer les changements dans la base de données
        conn.commit()

        print("Données insérées avec succès dans la base de données SQL Server.")

    except Exception as e:
        # Gestion des erreurs
        print("Erreur lors de l'insertion des données dans la base de données :", e)

    finally:
        # Fermer le curseur
        if cursor:
            cursor.close()


def deconnect(conn):
    conn.close()
    print("Connection closed SQL Server Connexion")


def main():
    # Établir la connexion à la base de données
    conn = connect_to_sql_server(SERVER, POSTGRES_PORT, DATABASE, USERNAME, PASSWORD)
    if conn is None:
        return

    # Appeler la fonction pour stocker les données dans la base de données SQL Server
    # store_in_sql_server(stocks_data, conn)

    # Fermer la connexion à la base de données
    conn.close()


if __name__ == "__main__":
    main()
