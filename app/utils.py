# app/utils.py
from app.models import Posizione
from app import db

def check_position_exists(position, minifig_no):
    # Usa SQLAlchemy per controllare l'esistenza della posizione o del numero della minifigura
    result = db.session.query(Posizione).filter(
        (Posizione.posizione == position) | (Posizione.no == minifig_no)
    ).count()

    return result > 0
