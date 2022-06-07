import http

from flask import Blueprint, jsonify, request

from ...models.car import Car
from ...extensions import db

cars_api_bp = Blueprint(name="cars_api_bp", import_name=__name__)


@cars_api_bp.get('/cars/')
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

    return jsonify(result), http.HTTPStatus.OK


@cars_api_bp.delete('/cars/<int:car_id>/')
def delete(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    return '', http.HTTPStatus.NO_CONTENT


@cars_api_bp.post('/cars/')
def create():
    body = request.get_json()
    model_name = body.get('model_name')
    color = body.get('color')
    dealer_id = body.get('dealer_id')
    car = Car(model_name=model_name, color=color, dealer_id=dealer_id)
    db.session.add(car)
    db.session.commit()

    return jsonify(car), http.HTTPStatus.CREATED
