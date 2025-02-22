import pandas as pd
from datetime import datetime


def clean_prix_column(df):
    # Retirer le signe euro, enlever les espaces à l'intérieur des nombres, et convertir en float
    df['Prix'] = df['Prix'].replace({'€': '', ' ': ''}, regex=True).astype(float)
    return df


def convert_to_date(df):
    def format_date(date_str):
        try:
            return datetime.strptime(date_str, '%m-%Y').strftime('%Y-%m-%d')
        except ValueError:
            return None

    df['Date Publication'] = df['Date Publication'].apply(format_date)

    return df


def convert_column_to_int(df, column_name):
    """
    Convertit une colonne spécifiée d'un DataFrame en type int.

    :param df: DataFrame contenant la colonne à convertir.
    :param column_name: Nom de la colonne à convertir.
    :return: DataFrame avec la colonne convertie en type int.
    """
    # Assurer que la colonne existe dans le DataFrame
    if column_name in df.columns:
        # Convertir la colonne en int après avoir supprimé les valeurs manquantes
        df[column_name] = pd.to_numeric(df[column_name], errors='coerce').astype('Int64')
    else:
        print(f"Erreur : La colonne '{column_name}' n'existe pas dans le DataFrame.")
    return df
