
from flask import render_template, Blueprint, request, flash, redirect, session
from datetime import datetime
from app.db.database import check_position_exists, insert_position_data, insert_minifigure_data
from app.db.api import get_minifigure_description
import json

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template('index.html', today=datetime.today().strftime("%m/%d/%Y"))

# pagina per la ricerca della minifigura
@main.route("/insert_bl")
def insert_bl():
    return  render_template("insert_bl.html")


# ROUTE PER IL CONTROLLO SE POSIZIONE O MINIFIGURA ESISTONO
@main.route("/control_exist", methods = ['GET','POST'])
def control_exist():
    # Preleva i dati dal form
    no = request.form.get("no")
    posizione = request.form.get("posizione")
    quadro = request.form.get("quadro")
    # Controlla se la posizione o la minifigura esistono
    if check_position_exists(posizione, no):
        flash("Posizione o numero minifigura già esistente.", "warning")
        return redirect('/insert_bl')
    else:
        # PRELEVA I DATI DELLA MINIFIGURA DA BRICKLINK
        descrizione = get_minifigure_description(no)
        if descrizione:
            # Salva descrizione e altri parametri nella sessione
            session['descrizione'] = json.dumps(descrizione)
            session['no'] = no
            session['posizione'] = posizione
            session['quadro'] = quadro
            return redirect("/preinsert")
        else:
            flash("Minifigura non trovata.", "danger")
            return redirect('/insert_bl')

# ROUTE PER VISIONARE I DATI PRIMA DELL' INSERIMENTO
@main.route("/preinsert", methods=['GET', 'POST'])
def preinsert():
    # Carica 'descrizione' dalla sessione
    descrizione = session.get('descrizione')
    no = session.get('no')
    posizione = session.get('posizione')
    quadro = session.get('quadro')
    if descrizione:
        descrizione = json.loads(descrizione)  # Converte la stringa JSON in un dizionario
    else:
        flash("Descrizione non disponibile.", "danger")
        return redirect('/insert_bl')

    return render_template('preinsert.html', descrizione=descrizione, no=no, posizione=posizione, quadro=quadro)

# ROUTE PER INSERIRE I DATI NEL DATABASE
@main.route("/insert_db", methods=['GET', 'POST'])
def insert_db():
    no = request.form.get('no')
    posizione = request.form.get('posizione')
    quadro = request.form.get('quadro')

    # Inserimento della posizione
    inserisci_posizione = insert_position_data(posizione, no, quadro)
    if not inserisci_posizione:
        flash("Errore durante l'inserimento della posizione.", "danger")
        return redirect('/insert_bl')  # Ritorno in caso di errore durante l'inserimento della posizione

    # Recupero dei dati per la minifigura
    no = request.form.get('no')
    name = request.form.get('name')
    tipo = request.form.get('type')
    category_id = request.form.get('category_id')
    image_url = request.form.get('image_url')
    thumbnail_url = request.form.get('thumbnail_url')
    weight = request.form.get('weight')
    dim_x = request.form.get('dim_x')
    dim_y = request.form.get('dim_y')
    dim_z = request.form.get('dim_z')
    year_released = request.form.get('year_released')


    # Inserimento della minifigura
    inserisci_minifigura = insert_minifigure_data(no, name, tipo, category_id, image_url, thumbnail_url, weight, dim_x, dim_y, dim_z, year_released)
    if inserisci_minifigura:
        flash("Inserimento avvenuto con successo.", "success")
        session.clear()
        return redirect('/insert_bl')  # Redirect dopo successo
    else:
        flash("Errore durante l'inserimento della minifigura.", "danger")
        return redirect('/insert_bl')  # Redirect in caso di errore durante l'inserimento della minifigura





