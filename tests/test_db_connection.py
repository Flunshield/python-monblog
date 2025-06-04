import os
import psycopg2
from urllib.parse import quote_plus

# Configuration de la base de données
DB_NAME = "blog_db"
DB_USER = "postgres"
DB_PASSWORD = "julien"
DB_HOST = "localhost"
DB_PORT = "5432"

try:
    # Connexion à PostgreSQL
    connection = psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("Connexion réussie !")
    print(f"Version PostgreSQL : {record}")
    
    cursor.close()
    connection.close()
    
except Exception as error:
    print(f"Erreur de connexion : {error}")
