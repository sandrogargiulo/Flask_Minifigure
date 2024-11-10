import os
from traceback import print_tb

import requests  # type: ignore
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

# Carica le variabili di ambiente dal file .env
load_dotenv()

auth = OAuth1(os.getenv('BRICKLINK_CONSUMER_KEY'),os.getenv('BRICKLINK_CONSUMER_SECRET'),
              os.getenv('BRICKLINK_TOKEN'),os.getenv('BRICKLINK_TOKEN_SECRET'))

#PRELEVA I DATI DELLA MINIFIGURA
# Preleva i dati della minifigura
def get_minifigure_description(minifig_id):
    url = f'https://api.bricklink.com/api/store/v1/items/MINIFIG/{minifig_id}'
    try:
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            data = response.json()
            print("Risposta JSON:", data)
            # Verifica se 'data' esiste ed è un dizionario con dati
            if 'data' in data and data['data']:
                return data['data']
            else:
                print("Nessun dato trovato per la minifigura richiesta.")
                return None
        else:
            print(f"Errore HTTP: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Errore di connessione: {e}")
        return None
