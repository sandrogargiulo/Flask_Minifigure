import os
import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

# Carica le variabili di ambiente dal file .env
load_dotenv()

auth = OAuth1(
    os.getenv('BRICKLINK_CONSUMER_KEY'),
    os.getenv('BRICKLINK_CONSUMER_SECRET'),
    os.getenv('BRICKLINK_TOKEN'),
    os.getenv('BRICKLINK_TOKEN_SECRET')
)

def make_api_request(endpoint, params=None):
    """
    Effettua una richiesta generica all'API BrickLink.
    """
    url = f'https://api.bricklink.com/api/store/v1/{endpoint}'
    try:
        response = requests.get(url, params=params, auth=auth)
        response.raise_for_status()  # Solleva eccezione per errori HTTP
        data = response.json()
        return data.get('data', None)  # Restituisce 'data' se esiste, altrimenti None
    except requests.RequestException as e:
        print(f"Errore di connessione o API: {e}")
        return None


# Funzioni specifiche che utilizzano la funzione generica
def get_minifigure_description(minifig_id):
    """
    Ottiene la descrizione di una minifigura.
    """
    return make_api_request(f"items/MINIFIG/{minifig_id}")


def get_bricklink_value(minifig_id):
    """
    Ottiene il valore medio di una minifigura.
    """
    data = make_api_request(f"items/MINIFIG/{minifig_id}/price")
    return data.get('qty_avg_price', "N/A") if data else "N/A"


def get_price_minifigure_used(minifig_id):
    """
    Ottiene il valore medio usato di una minifigura.
    """
    params = {"new_or_used": "U"}
    data = make_api_request(f"items/MINIFIG/{minifig_id}/price", params=params)
    return data.get('avg_price', "N/A") if data else "N/A"

def get_brick_description(item_id):
    """
    Ottiene la descrizione di un pezzo.
    """
    return make_api_request(f"items/PART/{item_id}")


def get_brick_image(item_id, color_id):
    """
    Ottiene l'immagine di un pezzo con un colore specifico.
    """
    return make_api_request(f"items/PART/{item_id}/images/{color_id}")

def set_description(item_id):
    """
    Ottiene la descrizione di un set.
    """
    return make_api_request(f"items/SET/{item_id}")

def set_pieces(item_id):
    """
    Ottiene i pezzi contenuti in un set.
    """
    return make_api_request(f"items/SET/{item_id}/subsets")

def set_price(item_id, stato):
    """
    Ottiene il prezzo medio di un set (nuovo o usato).
    """
    params = {"new_or_used": "U"} if stato == "U" else None
    data = make_api_request(f"items/SET/{item_id}/price", params=params)
    return data.get('avg_price', "N/A") if data else "N/A"

def part_price(item_id, color_id, stato):
    """
    Ottiene il prezzo medio di un pezzo (nuovo o usato).
    """
    params = {"color_id": color_id, "new_or_used": stato}
    data = make_api_request(f"items/PART/{item_id}/price", params=params)
    return data.get('avg_price', "N/A") if data else "N/A"

