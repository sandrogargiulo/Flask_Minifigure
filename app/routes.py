
from flask import render_template, Blueprint, request, flash, redirect, session
import datetime
from app.utils import check_position_exists
from app.api import get_minifigure_description, get_bricklink_value
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
    caso = None  # Imposta caso di default su None
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        numero_minifigura = request.form.get('no')
        posizione = request.form.get('posizione')
        quadro = request.form.get('quadro')

        try:
            if tipo == '0':  # Ricerca per posizione
                posizione_record = Posizione.query.filter_by(posizione=posizione).first()
                if posizione_record:
                    numero_minifigura = posizione_record.no
                    quadro = posizione_record.quadro
                    minifigura = Minifigure.query.filter_by(no=numero_minifigura).first()
                    nome_troncato = (minifigura.name.split('&')[0] if isinstance(minifigura.name, str) else "") if minifigura else ""
                    valore_medio = get_bricklink_value(numero_minifigura)
                    caso = None  # caso rimane None in questo caso
                    return render_template('view.html', esito=minifigura, nome_troncato=nome_troncato,
                                           posizione=posizione, quadro=quadro, valore_medio=valore_medio, caso=caso)
                caso = None  # caso in None quando posizione non trovata
                return render_template('view.html', esito=None, messaggio="Posizione non trovata.", caso=caso)

            elif tipo == '1':  # Ricerca per numero minifigura
                posizione_record = Posizione.query.filter_by(no=numero_minifigura).first()
                if posizione_record:
                    quadro = posizione_record.quadro
                    posizione = posizione_record.posizione
                    minifigura = Minifigure.query.filter_by(no=numero_minifigura).first()
                    nome_troncato = (minifigura.name.split('&')[0] if isinstance(minifigura.name, str) else "") if minifigura else ""
                    valore_medio = get_bricklink_value(numero_minifigura)
                    caso = None  # caso rimane None in questo caso
                    return render_template('view.html', esito=minifigura, nome_troncato=nome_troncato,
                                           posizione=posizione, quadro=quadro, valore_medio=valore_medio, caso=caso)
                caso = None  # caso in None quando minifigura non trovata
                return render_template('view.html', esito=None, messaggio="Minifigura non trovata.", caso=caso)

            elif tipo == '2':  # Ricerca per quadro
                posizioni = Posizione.query.filter_by(quadro=quadro).all()
                minifigure = Minifigure.query.filter(Minifigure.no.in_([pos.no for pos in posizioni])).all()
                print(f"Posizioni trovate: {posizioni}")  # Debug: stampa posizioni
                print(f"Minifigure trovate: {minifigure}")  # Debug: stampa minifigure

                # Controllo se posizioni e minifigure hanno lo stesso numero di elementi
                if len(posizioni) != len(minifigure):
                    return render_template('view.html', esito=None,
                                           messaggio="Mismatch nel numero di posizioni e minifigure.")

                # Crea una lista di tuple (posizione, minifigure)
                posizioni_minifigure = list(zip(posizioni, minifigure))

                if not posizioni_minifigure:
                    return render_template('view.html', esito=None,
                                               messaggio="Nessun risultato trovato.")

                return render_template('view.html', posizioni_minifigure=posizioni_minifigure, caso=5)

        except Exception as e:
            print(f"Errore: {e}")  # Debug: stampa errore
            caso = None  # caso in None se c'è un errore
            return render_template('view.html', esito=None, messaggio=f"Errore: {str(e)}", caso=caso)

    # Richiesta GET
    caso = None  # caso in None per la richiesta GET
    return render_template('view.html', messaggio="Inserisci i parametri di ricerca.", caso=caso)





