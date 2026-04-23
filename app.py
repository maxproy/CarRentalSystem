import os
from flask import Flask, request, jsonify, send_from_directory
from extensions import db
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import Car, User, Rental, ContactMessage
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    return app

app = create_app()

# --- ABSOLUTE PATH CONFIGURATION ---
# This forces Python to find exactly where app.py lives on your computer
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blizzardhub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "I2Z0Z0O4H"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db.init_app(app)
CORS(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes to serve static files (frontend)
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/admin.html')
def serve_admin():
    return send_from_directory('.', 'admin.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# Cars
@app.route('/api/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    cars_list = [car.to_dict() for car in cars]
    return jsonify({'success': True, 'cars': cars_list})

@app.route('/api/cars', methods=['POST'])
def add_car():
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image part in the request'}), 400
    
    image = request.files['image']
    if image.filename == '':
        return jsonify({'success': False, 'message': 'No selected image file'}), 400
        
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        
        # --- Print to terminal for debugging ---
        print(f"ATTEMPTING TO SAVE IMAGE TO: {app.config['UPLOAD_FOLDER']}")
        
        # --- Bulletproof Folder Creation ---
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
        # Save the image
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
        print(f"Database error: {e}") 
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
    
        start_date_obj = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()

        rental = Rental(
            car_id=data.get('car_id'),
            user_id=data.get('user_id'),
            start_date=start_date_obj,
            end_date=end_date_obj
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
        hashed_password = generate_password_hash(data.get('password'), method='pbkdf2:sha256')
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
    with app.app_context():
        if not os.path.exists('blizzardhub.db'):
            db.create_all()
            
    app.run(debug=True)
