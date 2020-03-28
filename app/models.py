from app import db 

class Transaction(db.Model):
    id = db.Column(db.String(10), primary_key=True, index= True)
    amount = db.Column(db.String(5))
    phone = db.Column(db.String(12))