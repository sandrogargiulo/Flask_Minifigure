from flask import render_template, current_app, Blueprint
from datetime import datetime


main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template('index.html', today=datetime.today().strftime("%m/%d/%Y"))

