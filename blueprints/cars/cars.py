from flask import Blueprint, render_template, request, url_for, redirect

from ...models.car import Car
from ...models.dealer import Dealer
from ...extensions import db

cars_bp = Blueprint(name="cars_bp", import_name=__name__, template_folder='templates')


@cars_bp.route('/cars/<int:car_id>/')
def car(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('cars/car.html', car=car)


@cars_bp.route('/cars/create/', methods=('GET', 'POST'))
def create():
    dealers = Dealer.query.all()

    if request.method == 'POST':
        model_name = request.form['model_name']
        color = request.form['color']
        dealer_id = request.form['dealer_id']
        car = Car(model_name=model_name, color=color, dealer_id=dealer_id)
        db.session.add(car)
        db.session.commit()

        return redirect(url_for('general_bp.index'))

    return render_template('cars/create.html', dealers=dealers)


@cars_bp.route('/cars/<int:car_id>/edit/', methods=('GET', 'POST'))
def edit(car_id):
    car = Car.query.get_or_404(car_id)
    dealers = Dealer.query.all()

    if request.method == 'POST':
        model_name = request.form['model_name']
        color = request.form['color']
        dealer_id = request.form.get('dealer_id')

        car.model_name = model_name
        car.color = color
        car.dealer_id = dealer_id

        db.session.add(car)
        db.session.commit()

        return redirect(url_for('general_bp.index'))

    return render_template('cars/edit.html', car=car, dealers=dealers)


@cars_bp.post('/cars/<int:car_id>/delete/')
def delete(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('general_bp.index'))
