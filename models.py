"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

def connect_db(app):
    """Connect the database to our Flask app."""

    db.app = app
    db.init_app(app)

default_image = 'https://tinyurl.com/y63x78zs'


class Cupcake(db.Model):
    '''Cupcakes model to structure cupcake details'''
    __tablename__='cupcakes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable = False)
    size = db.Column(db.Text, nullable = False)
    rating = db.Column(db.Float, nullable = False)
    image = db.Column(db.Text, nullable = False, default = default_image)
    
    def serialize(self):
        return {
            "id": self.id,
            'flavor': self.flavor, 
            'size': self.size, 
            'rating': self.rating, 
            'image': self.image
            }