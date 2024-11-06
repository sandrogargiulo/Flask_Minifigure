from flask import Flask
from .db.database import create_connection
import os
from dotenv import load_dotenv

# Carica le variabili di ambiente
load_dotenv()




def create_app():
    app = Flask(__name__)

    # Configurazione delle variabili di ambiente
    app.config['BRICKLINK_CONSUMER_KEY'] = os.getenv('BRICKLINK_CONSUMER_KEY')
    app.config['BRICKLINK_CONSUMER_SECRET'] = os.getenv('BRICKLINK_CONSUMER_SECRET')
    app.config['BRICKLINK_TOKEN'] = os.getenv('BRICKLINK_TOKEN')
    app.config['BRICKLINK_TOKEN_SECRET'] = os.getenv('BRICKLINK_TOKEN_SECRET')
    app.config['HOST'] = os.getenv('HOST')
    app.config['USERNAME'] = os.getenv('USERNAME')
    app.config['PASSWORD'] = os.getenv('PASSWORD')
    app.config['DATABASE'] = os.getenv('DATABASE')

    # Registrazione dei blueprint
    from .routes import main
    app.register_blueprint(main)


    # Test della connessione (opzionale, puoi rimuoverlo in produzione)
    with app.app_context():
        connection = create_connection()
        if connection:
            print("Connessione stabilita.")
            connection.close()

    return app


