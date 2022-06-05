from app import db, Car
from dealer import Dealer

dealer1 = Dealer(name='Yellow Dealer', email='123@example.com', desc='sample text 1')
dealer2 = Dealer(name='Green Dealer', email='456@example.com', desc='sample text 2')
dealer3 = Dealer(name='Black Dealer', email='789@example.com', desc='sample text 3')

car1 = Car(model_name='Tesla', color='white', dealer=dealer1)
car2 = Car(model_name='Mercedes', color='red', dealer=dealer2)
car3 = Car(model_name='Toyota', color='black', dealer_id=2)
car4 = Car(model_name='Kia', color='green', dealer_id=1)

db.session.add_all([dealer1, dealer2, dealer3])
db.session.add_all([car1, car2, car3, car4])

db.session.commit()
