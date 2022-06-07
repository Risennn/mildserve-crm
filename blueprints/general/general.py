from flask import Blueprint, render_template

from ...models.dealer import Dealer
from ...models.car import Car

general_bp = Blueprint(name="general_bp", import_name=__name__, template_folder='templates')


@general_bp.route('/')
def index():
    dealers = Dealer.query.all()
    cars = Car.query.all()
    return render_template('general/index.html', dealers=dealers, cars=cars)
