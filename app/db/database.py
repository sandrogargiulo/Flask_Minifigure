import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Carica le variabili di ambiente dal file .env
load_dotenv()

def create_connection():
    """Crea una connessione al database MySQL."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USERNAME"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE")
        )
        if connection.is_connected():
            print("Connessione al database avvenuta con successo!")
            return connection
    except Error as e:
        print("Errore durante la connessione al database:", e)
        return None
