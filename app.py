"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, Cupcake

app = Flask(__name__)
app.app_context().push() 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "abc123"

connect_db(app)
toolbar = DebugToolbarExtension(app)

# Serialize data so that we could use jsonify to convert ot json data
def serialize(self):
     return {
        "id": self.id,
        'flavor': self.flavor, 
        'size': self.size, 
        'rating': self.rating, 
        'image': self.image
    }

@app.route('/api/cupcakes')
def get_cupcakes():
    cupcakes = Cupcake.query.all
    serialized = [serialize(cupcake) for cupcake in cupcakes]
    return jsonify(cupcakes = serialized)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    serialized = serialize(cupcake)
    return jsonify(serialized)

@app.route('/api/cupcakes', methods = ['POST'])
def create_cupcake():
    flavor = request.json(['flavor'])
    size = request.json(['size'])
    rating = request.json(['rating'])
    image = request.json(['image'])
    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    serialized = serialize(new_cupcake)
    return (jsonify(serialized),201)