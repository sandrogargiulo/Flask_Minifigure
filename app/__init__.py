from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Carica le variabili di ambiente
load_dotenv()
# Crea un'istanza di SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configurazione delle variabili di ambiente
    app.config['BRICKLINK_CONSUMER_KEY'] = os.getenv('BRICKLINK_CONSUMER_KEY')
    app.config['BRICKLINK_CONSUMER_SECRET'] = os.getenv('BRICKLINK_CONSUMER_SECRET')
    app.config['BRICKLINK_TOKEN'] = os.getenv('BRICKLINK_TOKEN')
    app.config['BRICKLINK_TOKEN_SECRET'] = os.getenv('BRICKLINK_TOKEN_SECRET')

    # Configurazione del database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('USERNAME')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}/{os.getenv('DATABASE')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    #IMPOSTAZIONE DELLA SECRET KEY
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Inizializza SQLAlchemy con l'app
    db.init_app(app)

    # Registrazione dei blueprint
    from app.routes import main
    app.register_blueprint(main)

    return app


