import os
from dataclasses import dataclass
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@dataclass
class Dealer(db.Model):
    id: int
    name: str
    email: str
    created_at: str
    desc: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    desc = db.Column(db.Text)
    cars = db.relationship('Car', backref='dealer')

    def __repr__(self):
        return f'<Dealer {self.name}>'


@dataclass
class Car(db.Model):
    id: int
    model_name: str
    color: str
    created_at: str
    dealer_id: int

    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    dealer_id = db.Column(db.Integer, db.ForeignKey('dealer.id'))

    def __repr__(self):
        return f'<Car {self.model_name}>'


@app.route('/')
def index():
    dealers = Dealer.query.all()
    cars = Car.query.all()
    return render_template('index.html', dealers=dealers, cars=cars)


@app.get('/dealers/')
def dealers():
    return Dealer.query.all()


@app.route('/dealers/<int:dealer_id>/')
def dealer(dealer_id):
    dealer = Dealer.query.get_or_404(dealer_id)
    return render_template('dealer.html', dealer=dealer)


@app.route('/dealers/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        desc = request.form['desc']
        dealer = Dealer(name=name, email=email, desc=desc)
        db.session.add(dealer)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/dealers/<int:dealer_id>/edit/', methods=('GET', 'POST'))
def edit(dealer_id):
    dealer = Dealer.query.get_or_404(dealer_id)

    if request.method == 'POST':
        firstname = request.form['firstname']
        email = request.form['email']
        desc = request.form['desc']

        dealer.name = firstname
        dealer.email = email
        dealer.desc = desc

        db.session.add(dealer)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', dealer=dealer)


@app.post('/dealers/<int:dealer_id>/delete/')
def delete(dealer_id):
    dealer = Dealer.query.get_or_404(dealer_id)
    db.session.delete(dealer)
    db.session.commit()
    return redirect(url_for('index'))


@app.get('/cars/')
def cars():
    args = request.args
    model_name = args.get('model_name')
    color = args.get('color')
    dealer_id = args.get('dealer_id')

    if None not in (model_name, color, dealer_id):
        result = Car.query.filter_by(model_name=model_name, color=color, dealer_id=dealer_id).all()
    elif model_name is not None:
        result = Car.query.filter_by(model_name=model_name).all()
    elif color is not None:
        result = Car.query.filter_by(color=color).all()
    elif dealer_id is not None:
        result = Car.query.filter_by(dealer_id=dealer_id).all()
    else:
        result = Car.query.all()

    return jsonify(result)


@app.route('/cars/<int:car_id>/')
def car(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('car.html', car=car)


@app.route('/cars/create/', methods=('GET', 'POST'))
def car_create():
    dealers = Dealer.query.all()

    if request.method == 'POST':
        model_name = request.form['model_name']
        color = request.form['color']
        dealer_id = request.form['dealer_id']
        car = Car(model_name=model_name, color=color, dealer_id=dealer_id)
        db.session.add(car)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('car-create.html', dealers=dealers)


@app.route('/cars/<int:car_id>/edit/', methods=('GET', 'POST'))
def car_edit(car_id):
    car = Car.query.get_or_404(car_id)
    dealers = Dealer.query.all()

    if request.method == 'POST':
        model_name = request.form['model_name']
        color = request.form['color']
        dealer_id = request.form['dealer_id']

        car.model_name = model_name
        car.color = color
        car.dealer_id = dealer_id

        db.session.add(car)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('car-edit.html', car=car, dealers=dealers)


@app.post('/cars/<int:car_id>/delete/')
def car_delete(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.run(host='127.0.0.1', port=5005)
