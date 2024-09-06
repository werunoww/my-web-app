from ..extensions import db

class Apiary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    beeCount = db.Column(db.Integer)
    breed = db.Column(db.String(20))
    hiveType = db.Column(db.String(20))
    feed = db.Column(db.String(10))
    
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    