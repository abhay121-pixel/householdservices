from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

# User Model - Handles Admin, Service Professional, and Customer roles
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'admin', 'customer', 'service_professional'
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)  # Changed to nullable=False
    pin_code = db.Column(db.String(20), nullable=False)  # Changed to nullable=False
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_blocked = db.Column(db.Boolean, default=False)  # For blocking functionality
    is_approved = db.Column(db.Boolean, default=False)  # Make sure this line exists

    def is_active(self):
        return not self.is_blocked  # If blocked, return False

    def __repr__(self):
        return f"<User {self.username}, Role {self.role}, Blocked {self.is_blocked}>"

# ServiceProfessional Model - Stores additional information specific to service professionals
class ServiceProfessional(db.Model):
    __tablename__ = 'service_professionals'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)  # One-to-one with User
    service_name = db.Column(db.String(100), nullable=False)  # Type of service offered
    experience_years = db.Column(db.Integer, nullable=False)  # Years of experience
    document_upload = db.Column(db.String(255), nullable=True)  # Path to uploaded document (single PDF)
    average_rating = db.Column(db.Float, default=0.0)  # Add this line for average rating
    total_ratings = db.Column(db.Integer, default=0)   # Add this line for total number of ratings

    # Relationship with User
    user = db.relationship('User', backref=db.backref('service_professional', uselist=False))

    def __repr__(self):
        return f"<ServiceProfessional {self.user_id}, Service {self.service_name}, Experience {self.experience_years}>"

# Service Model - Defines the services available
class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Service {self.name}, Price {self.price}>"

# Service Request Model - Defines the service requests made by customers
class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    date_of_request = db.Column(db.DateTime, default=datetime.utcnow)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    service_status = db.Column(db.String(50), default='requested')
    remarks = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    rating_comment = db.Column(db.Text, nullable=True)
    rating_date = db.Column(db.DateTime, nullable=True)

    # Relationships
    customer = db.relationship('User', foreign_keys=[customer_id], backref='customer_requests')
    professional = db.relationship('User', foreign_keys=[professional_id], backref='professional_requests')
    service = db.relationship('Service', backref='service_requests')

    def __repr__(self):
        return f"<ServiceRequest {self.id}, Status {self.service_status}, Rating {self.rating}>"
