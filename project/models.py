from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ai_description = db.Column(db.Text)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    contact = db.Column(db.String(100), nullable=False)

#Ovde e za lost and found rabotite