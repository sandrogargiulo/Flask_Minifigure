from flask import render_template, current_app, Blueprint
from datetime import datetime


main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template('index.html', today=datetime.today().strftime("%m/%d/%Y"))

# pagina per la ricerca della minifigura
@main.route("/insert_bl")
def insert_bl():
    return  render_template("insert_bl.html")

