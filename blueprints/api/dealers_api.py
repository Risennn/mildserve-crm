import http

from flask import Blueprint, jsonify, request

from ...models.dealer import Dealer
from ...extensions import db

dealers_api_bp = Blueprint(name="dealers_api_bp", import_name=__name__)


@dealers_api_bp.get('/dealers/')
def dealers():
    return jsonify(Dealer.query.all()), http.HTTPStatus.OK


@dealers_api_bp.delete('/dealers/<int:dealer_id>/')
def delete(dealer_id):
    dealer = Dealer.query.get_or_404(dealer_id)
    db.session.delete(dealer)
    db.session.commit()
    return '', http.HTTPStatus.NO_CONTENT


@dealers_api_bp.post('/dealers/')
def create():
    body = request.get_json()
    name = body.get('name')
    email = body.get('email')
    desc = body.get('desc')
    dealer = Dealer(name=name, email=email, desc=desc)
    db.session.add(dealer)
    db.session.commit()
    return jsonify(dealer), http.HTTPStatus.CREATED


@dealers_api_bp.get('/dealers/<int:dealer_id>/')
def dealer(dealer_id):
    dealer = Dealer.query.get_or_404(dealer_id)
    return jsonify(dealer, dealer=dealer), http.HTTPStatus.OK
