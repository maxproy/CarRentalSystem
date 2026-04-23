import sys
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def create_admin(username, password):
    with app.app_context():
        existing_user = User.query.filter_by(name=username).first()
        if existing_user:
            print(f"User '{username}' already exists.")
            return
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        admin_user = User(name=username, email=f"{username}@example.com", password_hash=hashed_password)
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user '{username}' created successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_admin.py <username> <password>")
        sys.exit(1)
    username = sys.argv[1]
    password = sys.argv[2]
    create_admin(username, password)
