from flask import Blueprint, render_template, request, url_for, redirect

from ...models.dealer import Dealer
from ...extensions import db

dealers_bp = Blueprint(name="dealers_bp", import_name=__name__, template_folder='templates')


@dealers_bp.get('/dealers/<int:dealer_id>/')
def dealer(dealer_id=None):
    dealer = Dealer.query.get_or_404(dealer_id)
    return render_template('dealers/dealer.html', dealer=dealer)


@dealers_bp.route('/dealers/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        desc = request.form['desc']
        dealer = Dealer(name=name, email=email, desc=desc)
        db.session.add(dealer)
        db.session.commit()

        return redirect(url_for('general_bp.index'))

    return render_template('dealers/create.html')


@dealers_bp.route('/dealers/<int:dealer_id>/edit/', methods=('GET', 'POST'))
def edit(dealer_id):
    dealer = Dealer.query.get_or_404(dealer_id)

    if request.method == 'POST':
        firstname = request.form['name']
        email = request.form['email']
        desc = request.form['desc']

        dealer.name = firstname
        dealer.email = email
        dealer.desc = desc

        db.session.add(dealer)
        db.session.commit()

        return redirect(url_for('general_bp.index'))

    return render_template('dealers/edit.html', dealer=dealer)


@dealers_bp.post('/dealers/<int:dealer_id>/delete/')
def delete(dealer_id):
    dealer = Dealer.query.get_or_404(dealer_id)
    db.session.delete(dealer)
    db.session.commit()
    return redirect(url_for('general_bp.index'))
