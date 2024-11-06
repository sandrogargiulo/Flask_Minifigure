
from flask import render_template, current_app, Blueprint, request, flash, redirect
from datetime import datetime
from app.db.database import check_position_exists, insert_position_data, insert_minifigure_data
from app.db.api import get_minifigure_description

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
            # Passa descrizione come parametro nella query string
            return redirect(f"/preinsert?descrizione={descrizione}")
        else:
            flash("Minifigura non trovata.", "danger")
            return redirect('/insert_bl')

# ROUTE PER VISIONARE I DATI PRIMA DELL' INSERIMENTO
@main.route("/preinsert", methods = ['GET','POST'])
def preinsert():
    # Recupera descrizione dalla query stringa
    descrizione = request.args.get('descrizione', None)
    if not descrizione:
        flash("Descrizione non disponibile.", "danger")
        return redirect('/insert_bl')  # Se non c'è descrizione, redirige

    return render_template('preinsert.html', descrizione=descrizione)




