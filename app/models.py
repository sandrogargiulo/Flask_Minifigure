from . import db
from datetime import datetime

class Posizione(db.Model):
    __tablename__ = 'posizione'
    id = db.Column(db.Integer, primary_key=True)
    posizione = db.Column(db.Integer, nullable=False)
    no = db.Column(db.String(100), nullable=False)
    quadro = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.date(datetime.now()))
    updated_at = db.Column(db.DateTime, default=datetime.date(datetime.now()), onupdate=datetime.date(datetime.now()))

class Minifigure(db.Model):
    __tablename__ = 'minifigures_bl'
    id = db.Column(db.Integer, primary_key=True)
    no = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))
    category_id = db.Column(db.Integer)
    image_url = db.Column(db.String(255))
    thumbnail_url = db.Column(db.String(255))
    weight = db.Column(db.Float)
    dim_x = db.Column(db.Float)
    dim_y = db.Column(db.Float)
    dim_z = db.Column(db.Float)
    year_released = db.Column(db.Integer)
    is_obsolete = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.date(datetime.now()))
    updated_at = db.Column(db.DateTime, default=datetime.date(datetime.now()), onupdate=datetime.date(datetime.now()))