"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.app_context().push() 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "abc123"

connect_db(app)
toolbar = DebugToolbarExtension(app)

# Serialize data so that we could use jsonify to convert ot json data

@app.route('/')
def homepage():
    '''Show homepage'''
    
    return render_template('index.html')

@app.route('/api/cupcakes')
def get_cupcakes():
    '''Get data about all cupcakes and respond with JSON like: 
    {cupcakes: [{id, flavor, size, rating, image}, ...]}.'''
    
    cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in cupcakes]
    return jsonify(cupcakes = serialized)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    '''Get data of a cupcake and respond with JSON like: 
    {cupcake: {id, flavor, size, rating, image}}'''
    
    cupcake = Cupcake.query.get_or_404(id)
    serialized = cupcake.serialize()
    return jsonify(cupcake = serialized)

@app.route('/api/cupcakes', methods = ['POST'])
def create_cupcake():
    '''Create new cupcake and respond with json: 
    {cupcake: {id, flavor, size, rating, image}}'''
    
    data = request.json
    
    flavor = data['flavor']
    size = data['size']
    rating = data['rating']
    image = data['image'] or None
    
    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    
    db.session.add(new_cupcake)
    db.session.commit()
    
    serialized = new_cupcake.serialize()
    
    return (jsonify(cupcake = serialized),201)

@app.route('/api/cupcakes/<int:id>', methods = ['PATCH'])
def update_cupcake(id):
    '''Update cupcake details and Respond with JSON of the newly-updated 
    cupcake, like this: {cupcake: {id, flavor, size, rating, image}}'''
    
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    
    
    db.session.add(cupcake)
    db.session.commit()
    serialized = cupcake.serialize()
    
    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    '''Delete a cupcake and Respond with JSON of {message: "Deleted"}'''
    
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")