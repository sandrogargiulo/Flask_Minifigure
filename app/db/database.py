import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import datetime
import os

# Carica le variabili di ambiente dal file .env
load_dotenv()


def get_db_connection():
    """Crea una connessione al database MySQL."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USERNAME"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE")
        )
        print("Connessione al database avvenuta con successo.")
        return connection
    except Error as e:
        print("Errore durante la connessione al database:", e)
        return None

def check_position_exists(position, minifig_no):
    query = """
    SELECT COUNT(*) FROM posizione WHERE posizione = %s OR no = %s
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (position, minifig_no))
        result = cursor.fetchone()
        return result[0] > 0
    except Error as e:
        print("Errore durante il controllo della posizione:", e)
        return 0

def insert_position_data(position, minifig_no, quadro):
    query = """
    INSERT INTO posizione (posizione, no, quadro, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        values = (position, minifig_no, quadro, datetime.datetime.now(), datetime.datetime.now())
        cursor.execute(query, values)
        conn.commit()
    except Error as e:
        print("Errore durante l'inserimento della posizione:", e)
    return False

def insert_minifigure_data(data):
    query = """
    INSERT INTO minifigures_bl (no, name, type, category_id, image_url, thumbnail_url, weight, dim_x, dim_y, dim_z, year_released, is_obsolete, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        values = (
            data['no'],
            data['name'],
            data['type'],
            data['category_id'],
            data['image_url'],
            data['thumbnail_url'],
            data['weight'],
            data['dim_x'],
            data['dim_y'],
            data['dim_z'],
            data['year_released'],
            data['is_obsolete'],
            datetime.datetime.now(),
            datetime.datetime.now()
        )
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
    except Error as e:
        print("Errore durante l'inserimento della posizione:", e)
        return False
