
from flask import render_template, Blueprint, request, flash, redirect, session
import datetime
from app.utils import check_position_exists
from app.api import get_minifigure_description
from app.models import Posizione, Minifigure
from datetime import datetime

from app import db
import json

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template('index.html', today=datetime.today())

# pagina per l'inserimento della minifigura
@main.route("/insert_bl")
def insert_bl():
    return  render_template("insert_bl.html")

# pagina per la ricerca della minifigura
@main.route("/search_minifigure")
def search_minifigure():
    return  render_template("search_minifigure.html")


# ROUTE PER IL CONTROLLO SE POSIZIONE O MINIFIGURA ESISTONO
@main.route("/control_exist", methods=['GET', 'POST'])
def control_exist():
    # Preleva i dati dal form
    no = request.form.get("no")
    posizione = request.form.get("posizione")
    quadro = request.form.get("quadro")

    # Controlla se la posizione o la minifigura esistono
    if check_position_exists(posizione, no):
        flash("Posizione o numero minifigura già esistente.", "warning")
        return redirect('/insert_bl')  # Ritorna indietro in caso di duplicato

    else:
        # PRELEVA I DATI DELLA MINIFIGURA DA BRICKLINK
        descrizione = get_minifigure_description(no)
        if descrizione:
            # Salva descrizione e altri parametri nella sessione
            session['descrizione'] = json.dumps(descrizione)
            session['no'] = no
            session['posizione'] = posizione
            session['quadro'] = quadro
            return redirect("/preinsert")  # Ritorna alla pagina di preinserimento
        else:
            flash("Minifigura non trovata.", "danger")
            return redirect('/insert_bl')  # In caso di errore nel recupero della minifigura

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
    # Recupero i dati dal form
    no = request.form.get('no')
    posizione = request.form.get('posizione')
    quadro = request.form.get('quadro')

    # Inserimento della posizione
    try:
        nuova_posizione = Posizione(
            posizione=posizione,
            no=no,
            quadro=quadro,
            created_at=datetime.today(),
            updated_at=datetime.today()
        )
        db.session.add(nuova_posizione)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Rollback in caso di errore
        flash(f"Errore durante l'inserimento della posizione: {e}", "danger")
        return redirect('/insert_bl')

    # Recupero dei dati per la minifigura
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
    is_obsolete = request.form.get('is_obsolete') == '1'  # Assicurati di convertire il valore

    # Inserimento della minifigura
    try:
        nuova_minifigura = Minifigure(
            no=no,
            name=name,
            type=tipo,
            category_id=category_id,
            image_url=image_url,
            thumbnail_url=thumbnail_url,
            weight=weight,
            dim_x=dim_x,
            dim_y=dim_y,
            dim_z=dim_z,
            year_released=year_released,
            is_obsolete=is_obsolete,
            created_at=datetime.today(),
            updated_at=datetime.today()
        )
        db.session.add(nuova_minifigura)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Rollback in caso di errore
        flash(f"Errore durante l'inserimento della minifigur: {e}.", "danger")
        return redirect('/insert_bl')

    # Se l'inserimento è andato a buon fine
    flash("Inserimento avvenuto con successo.", "success")
    return redirect('/insert_bl')  # Redirect dopo successo


@main.route('/cerca', methods=['GET', 'POST'])
def cerca():
    if request.method == 'POST':
        # Recupera i dati del form
        tipo = request.form.get('tipo')
        numero_minifigura = request.form.get('no')
        posizione = request.form.get('posizione')
        quadro = request.form.get('quadro')


        if tipo == 0:
           print("tipo 0")
        if tipo == 1:
            print("tipo 1")
        if tipo == 2:
            print("tipo 2")




        # Passa i dati al template
        return render_template('search_minifigure.html',
                               numero_minifigura=numero_minifigura,
                               posizione=posizione,
                               quadro=quadro)
    return render_template('search_minifigure.html')




