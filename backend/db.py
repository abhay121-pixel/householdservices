from app import app, db, User
from werkzeug.security import generate_password_hash

# Set up the app context for DB operations
with app.app_context():
    # Create the tables if they do not exist
    db.create_all()

    # Check if an admin already exists
    admin = User.query.filter_by(role='admin').first()

    if not admin:
        # Create a new admin user if one doesn't already exist
        admin = User(
            username='admin',
            password=generate_password_hash('12345678', method='pbkdf2:sha256'),
            role='admin',
            name='Admin User',
            email='admin@gmail.com',
            address='Default Admin Address',
            pin_code='123456',
            is_approved=True
        )

        try:
            # Add the new admin user to the session and commit
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        except Exception as e:
            print(f"Error creating admin user: {str(e)}")
            db.session.rollback()
    else:
        print("Admin user already exists.")
