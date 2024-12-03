from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from models import db, User
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_migrate import Migrate
import redis
from flask_caching import Cache
from flask_restful import Api
import sys

# Print Python path for debugging
print(f"Using Python from: {sys.executable}")

app = Flask(__name__)
api = Api()

redis_client = redis.Redis(host='localhost', port=6379, db=0)
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS': redis_client})

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['JWT_SECRET_KEY'] = "your-secret-key"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

# Configure CORS to allow Authorization header
CORS(app, resources={
    r"/*": {
        "origins": "http://localhost:8080",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "/login"

# Initialize JWT
jwt = JWTManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import routes and initialize API
from routes import api as routes_api
routes_api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
