from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
app = Flask(__name__)

FLASK_ENV_SECRET_KEY = os.getenv('FLASK_ENV_SECRET_KEY', "12345678")
# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blizzardhub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

db = SQLAlchemy(app)
CORS(app)

# Import models after db initialization to avoid circular imports

from models import Car, User, Rental, ContactMessage

# Routes to serve static files (frontend)
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

import os

@app.route('/admin.html')
def serve_admin():
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'FRONTEND')
    return send_from_directory(frontend_dir, 'admin.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# API Endpoints

# Cars
@app.route('/api/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    cars_list = [car.to_dict() for car in cars]
    return jsonify({'success': True, 'cars': cars_list})

from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/cars', methods=['POST'])
def add_car():
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image part in the request'}), 400
    image = request.files['image']
    if image.filename == '':
        return jsonify({'success': False, 'message': 'No selected image file'}), 400
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        return jsonify({'success': False, 'message': 'Invalid image file type'}), 400

    data = request.form
    try:
        car = Car(
            name=data.get('name'),
            brand=data.get('brand'),
            year=int(data.get('year')),
            price_per_day=float(data.get('price_per_day')),
            image=filename
        )
        db.session.add(car)
        db.session.commit()
        return jsonify({'success': True, 'car': car.to_dict()})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# Rentals
@app.route('/api/rentals', methods=['GET'])
def get_rentals():
    rentals = Rental.query.all()
    rentals_list = [rental.to_dict() for rental in rentals]
    return jsonify({'success': True, 'rentals': rentals_list})

@app.route('/api/rentals', methods=['POST'])
def add_rental():
    data = request.json
    try:
        rental = Rental(
            car_id=data.get('car_id'),
            user_id=data.get('user_id'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date')
        )
        db.session.add(rental)
        db.session.commit()
        return jsonify({'success': True, 'rental': rental.to_dict()})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/rentals/<int:rental_id>', methods=['DELETE'])
def delete_rental(rental_id):
    rental = Rental.query.get(rental_id)
    if not rental:
        return jsonify({'success': False, 'message': 'Rental not found'}), 404
    db.session.delete(rental)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Rental deleted'})

# Users
@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    try:
        hashed_password = generate_password_hash(data.get('password'), method='sha256')
        user = User(
            name=data.get('name'),
            email=data.get('email'),
            password_hash=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'success': True, 'user': user.to_dict()})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(name=data.get('username')).first()
    if not user or not check_password_hash(user.password_hash, data.get('password')):
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
    # For simplicity, no token generation, just success response
    return jsonify({'success': True, 'message': 'Login successful'})

# Contact
@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.json
    try:
        message = ContactMessage(
            name=data.get('name'),
            email=data.get('email'),
            message=data.get('message')
        )
        db.session.add(message)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Message received'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    if not os.path.exists('blizzardhub.db'):
        db.create_all()
    app.run(debug=True)
