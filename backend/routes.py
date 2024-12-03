from flask import request, jsonify, send_from_directory
from flask_restful import Resource, Api
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Service, ServiceRequest, ServiceProfessional
from sqlalchemy import func
from sqlalchemy.orm import aliased
from datetime import timedelta
import os
from flask_caching import Cache
import redis
#from app import app
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity, 
    get_jwt,
    create_access_token,
)
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from sqlalchemy.orm import aliased

# Initialize the Api
api = Api()

# Create uploads directory if it doesn't exist
UPLOAD_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

class SignUp(Resource):
    def post(self):
        try:
            data = request.get_json() if request.content_type == 'application/json' else request.form

            if not data:
                return {"message": "No data provided"}, 400

            # Basic required fields for all users
            required_fields = ['username', 'password', 'role', 'name', 'email', 'address', 'pin_code']
            missing_fields = [field for field in required_fields if not data.get(field)]
            
            # Additional required fields for service professionals
            if data.get('role') == 'service_professional':
                professional_fields = ['service_name', 'experience_years']
                missing_fields.extend([field for field in professional_fields if not data.get(field)])

            if missing_fields:
                return {
                    "message": f"Missing required fields: {', '.join(missing_fields)}",
                    "missing_fields": missing_fields
                }, 400

            # Set approval status based on role
            is_approved = True if data['role'] == 'customer' else False

            # Create new user
            new_user = User(
                username=data['username'],
                password=generate_password_hash(data['password']),
                role=data['role'],
                name=data['name'],
                email=data['email'],
                address=data['address'],
                pin_code=data['pin_code'],
                is_approved=is_approved,  # Customers are auto-approved
                is_blocked=False
            )

            db.session.add(new_user)
            db.session.commit()  # Commit to get the user ID

            # If it's a service professional, create the professional record
            if data['role'] == 'service_professional':
                professional = ServiceProfessional(
                    user_id=new_user.id,
                    service_name=data['service_name'],
                    experience_years=int(data['experience_years'])
                )
                db.session.add(professional)
                db.session.commit()

                return {
                    "message": "Registration successful! Please wait for admin approval. 😊"
                }, 201
            else:
                # For customers, just return success message
                return {
                    "message": "Registration successful! 😊"
                }, 201

        except Exception as e:
            print(f"Error in signup: {str(e)}")
            db.session.rollback()
            return {"message": f"Error during registration: {str(e)}"}, 500
        
redis_client = redis.Redis(host='localhost', port=6379, db=0)
#cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS': redis_client})

class UserInfo(Resource):
    #@cache.cached(timeout=10)
    @login_required
    def get(self):
        return {
            "username": current_user.username,
            "role": current_user.role,
            "email": current_user.email
        }, 200

# Register the route



class Login(Resource):
    def get(self):
        return {"message": "Login endpoint is ready."}, 200

    def post(self):
        try:
            # Print request details for debugging
            print("Request Headers:", dict(request.headers))
            print("Request Method:", request.method)
            
            data = request.get_json()
            print("Request Data:", data)  # Debug print
            
            email = data.get("email")
            password = data.get("password")
            role = data.get("role")

            print(f"Login attempt - Email: {email}, Role: {role}")

            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                if user.role != role:
                    return {"message": f"Invalid role. Your role is {user.role}"}, 403

                if user.is_blocked:
                    return {
                        "message": "Your account has been blocked. Please contact admin."
                    }, 403

                if role == 'service_professional' and not user.is_approved:
                    return {
                        "message": "Your account is pending approval. Please wait for admin approval."
                    }, 403

                access_token = create_access_token(
                    identity=str(user.id),
                    additional_claims={
                        "role": user.role,
                        "email": user.email,
                        "is_approved": user.is_approved
                    }
                )
                
                response_data = {
                    "message": "Login successful!",
                    "role": user.role,
                    "token": access_token,
                    "user_id": user.id,
                    "is_approved": user.is_approved
                }
                
                print("Login successful, returning:", response_data)  # Debug print
                return response_data, 200
            else:
                return {"message": "Invalid email or password"}, 401

        except Exception as e:
            print(f"Login error: {str(e)}")
            import traceback
            traceback.print_exc()  # Print full stack trace
            return {"message": f"Server error: {str(e)}"}, 500

    def options(self):
        # Handle OPTIONS request explicitly
        response = jsonify({'message': 'OK'})
        origin = request.headers.get('Origin')
        if origin in ['http://localhost:8080', 'http://localhost:8081']:
            response.headers.add('Access-Control-Allow-Origin', origin)
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

class AdminDashboard(Resource):
    @jwt_required()
    def get(self):
        if current_user.role != 'admin':
            return {"message": "Unauthorized access"}, 403
        return {"message": "Welcome to the Admin Dashboard!"}, 200
class CreateService(Resource):
    @jwt_required()
    def post(self):
        try:
            # Get user identity and JWT data
            current_user_id = get_jwt_identity()
            user = User.query.get(int(current_user_id))
            
            if not user or user.role != 'admin':
                return {"message": "Unauthorized access"}, 403

            data = request.get_json()
            print("Received service data:", data)

            # Validate required fields
            required_fields = ['name', 'price', 'time_required', 'description']
            for field in required_fields:
                if field not in data:
                    return {"message": f"Missing required field: {field}"}, 400

            # Create new service
            new_service = Service(
                name=data['name'],
                price=float(data['price']),
                time_required=data['time_required'],
                description=data['description']
            )

            db.session.add(new_service)
            db.session.commit()

            print(f"Service created successfully: {new_service.name}")

            return {
                "message": "Service created successfully!",
                "service": {
                    "id": new_service.id,
                    "name": new_service.name,
                    "price": new_service.price,
                    "description": new_service.description,
                    "time_required": new_service.time_required
                }
            }, 201

        except Exception as e:
            print("Error creating service:", str(e))
            db.session.rollback()
            return {"message": f"Error creating service: {str(e)}"}, 500

class EditService(Resource):
    @jwt_required()
    def put(self, service_id):
        try:
            # Get user identity and check if admin
            current_user_id = get_jwt_identity()
            user = User.query.get(int(current_user_id))
            
            if not user or user.role != 'admin':
                return {"message": "Unauthorized access"}, 403

            service = Service.query.get(service_id)
            if not service:
                return {"message": "Service not found"}, 404

            data = request.get_json()
            
            # Update service fields
            service.name = data.get('name', service.name)
            service.description = data.get('description', service.description)
            service.price = float(data.get('price', service.price))
            service.time_required = data.get('time_required', service.time_required)

            db.session.commit()
            return {"message": "Service updated successfully!"}, 200
            
        except Exception as e:
            print("Error updating service:", str(e))
            db.session.rollback()
            return {"message": "Error updating service"}, 500

class DeleteService(Resource):
    @jwt_required()
    def delete(self, service_id):
        try:
            # Get user identity and check if admin
            current_user_id = get_jwt_identity()
            user = User.query.get(int(current_user_id))
            
            if not user or user.role != 'admin':
                return {"message": "Unauthorized access"}, 403

            # Check if service exists
            service = Service.query.get(service_id)
            if not service:
                return {"message": "Service not found"}, 404

            # Check if service is being used in any service requests
            service_requests = ServiceRequest.query.filter_by(service_id=service_id).first()
            if service_requests:
                return {"message": "Cannot delete service as it has associated service requests"}, 400

            # Delete the service
            db.session.delete(service)
            db.session.commit()
            
            return {"message": "Service deleted successfully!", "service_id": service_id}, 200
            
        except Exception as e:
            print("Error deleting service:", str(e))
            db.session.rollback()
            return {"message": f"Error deleting service: {str(e)}"}, 500

class ListAllUsers(Resource):
    @jwt_required()
    def get(self):
        try:
            print("Fetching customers...")
            customers = User.query.filter_by(role='customer').all()
            
            users_list = [{
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "pin_code": user.pin_code,
                "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "is_blocked": user.is_blocked,
                "is_approved": user.is_approved,
                "role": user.role
            } for user in customers]
            
            print(f"Found {len(users_list)} customers")
            return {"users": users_list}, 200
            
        except Exception as e:
            print("Error fetching customers:", str(e))
            return {"message": "Error fetching customers"}, 500

class ListServiceProfessionals(Resource):
    @jwt_required()
    def get(self):
        try:
            print("Fetching professionals...")
            professionals = db.session.query(User, ServiceProfessional)\
                .join(ServiceProfessional)\
                .filter(User.role == "service_professional")\
                .all()
            
            print(f"Found {len(professionals)} professionals")
            
            professionals_list = [{
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "pin_code": user.pin_code,
                "service_name": prof.service_name,
                "experience_years": prof.experience_years,
                "document_upload": prof.document_upload,
                "is_blocked": user.is_blocked,
                "is_approved": user.is_approved
            } for user, prof in professionals]
            
            return {"service-professionals": professionals_list}, 200
            
        except Exception as e:
            print("Error fetching professionals:", str(e))
            return {"message": "Error fetching professionals"}, 500

class ToggleProfessionalBlock(Resource):
    @jwt_required()
    def post(self, professional_id, action):
        try:
            # Verify admin access
            current_user_id = get_jwt_identity()
            admin = User.query.get(current_user_id)
            if not admin or admin.role != 'admin':
                return {"message": "Unauthorized access"}, 403

            # Get the professional
            professional = User.query.filter_by(id=professional_id, role='service_professional').first()
            if not professional:
                return {"message": "Professional not found"}, 404

            # Toggle block status
            if action == 'block':
                professional.is_blocked = True
                message = "Professional blocked successfully"
            elif action == 'unblock':
                professional.is_blocked = False
                message = "Professional unblocked successfully"
            else:
                return {"message": "Invalid action"}, 400

            db.session.commit()
            return {"message": message}, 200

        except Exception as e:
            print("Error toggling professional block status:", str(e))
            db.session.rollback()
            return {"message": "Error updating professional status"}, 500

class ListServices(Resource):
    @jwt_required()
    def get(self):
        try:
            services = Service.query.all()
            print(f"Found {len(services)} services")  # Debug print
            
            service_list = [{
                "id": service.id,
                "name": service.name,
                "description": service.description,
                "price": service.price,
                "time_required": service.time_required
            } for service in services]

            print("Returning services:", service_list)  # Debug print
            return {"services": service_list}, 200

        except Exception as e:
            print("Error fetching services:", str(e))  # Debug print
            return {"message": "Error fetching services"}, 500

class BlockServiceProfessional(Resource):
    @login_required
    def post(self, professional_id):
        professional = ServiceProfessional.query.get(professional_id)
        if not professional:
            return {"message": "Professional not found"}, 404
        professional.status = "blocked"
        db.session.commit()
        return {"message": "Professional blocked successfully"}, 200

# Service Requests
class ServiceRequestResource(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()
            print(f"Received service request data: {data}")  # Debug print

            # Create new service request
            new_request = ServiceRequest(
                service_id=data['service_id'],
                customer_id=current_user_id,
                service_status='requested',  # Initial status
                remarks=data.get('remarks', ''),
                date_of_request=datetime.utcnow()
            )

            db.session.add(new_request)
            db.session.commit()

            print(f"Created service request: {new_request.id}")  # Debug print
            return {"message": "Service request created successfully"}, 201

        except Exception as e:
            print(f"Error creating service request: {str(e)}")  # Debug print
            db.session.rollback()
            return {"message": "Error creating service request"}, 500

    @jwt_required()
    def get(self, request_id=None):
        try:
            if request_id:
                request = ServiceRequest.query.get(request_id)
                if not request:
                    return {"message": "Request not found"}, 404
                return {
                    "id": request.id,
                    "service_id": request.service_id,
                    "customer_id": request.customer_id,
                    "professional_id": request.professional_id,
                    "status": request.service_status,
                    "remarks": request.remarks
                }, 200
            else:
                requests = ServiceRequest.query.all()
                return {
                    "requests": [{
                        "id": req.id,
                        "service_id": req.service_id,
                        "customer_id": req.customer_id,
                        "professional_id": req.professional_id,
                        "status": req.service_status,
                        "remarks": req.remarks
                    } for req in requests]
                }, 200
        except Exception as e:
            print(f"Error fetching service request(s): {str(e)}")
            return {"message": "Error fetching service request(s)"}, 500

class ApproveService(Resource):
    @login_required
    def post(self, service_id):
        service = Service.query.get(service_id)
        if not service:
            return {"message": "Service not found"}, 404
        service.status = "approved"
        db.session.commit()
        return {"message": "Service approved successfully"}, 200

class RejectService(Resource):
    @login_required
    def post(self, service_id):
        service = Service.query.get(service_id)
        if not service:
            return {"message": "Service not found"}, 404
        service.status = "rejected"
        db.session.commit()
        return {"message": "Service rejected successfully"}, 200

class SummaryData(Resource):
    @jwt_required()
    def get(self):
        try:
            # Verify admin access
            current_user_id = get_jwt_identity()
            admin = User.query.get(current_user_id)
            if not admin or admin.role != 'admin':
                return {"message": "Unauthorized access"}, 403

            # Get metrics
            metrics = {
                "totalUsers": User.query.filter_by(role='customer').count(),
                "totalProfessionals": User.query.filter_by(role='service_professional').count(),
                "totalServices": Service.query.count(),
                "totalRequests": ServiceRequest.query.count()
            }

            print("Metrics:", metrics)  # Debug print

            # Get service request status counts
            status_counts = {
                "requested": ServiceRequest.query.filter_by(service_status='requested').count(),
                "accepted": ServiceRequest.query.filter_by(service_status='accepted').count(),
                "completed": ServiceRequest.query.filter_by(service_status='completed').count(),
                "rejected": ServiceRequest.query.filter_by(service_status='rejected').count()
            }

            print("Status counts:", status_counts)  # Debug print

            # Get monthly data (last 6 months)
            six_months_ago = datetime.utcnow() - timedelta(days=180)
            monthly_requests = db.session.query(
                func.date_format(ServiceRequest.date_of_request, '%Y-%m').label('month'),
                func.count(ServiceRequest.id).label('count')
            ).filter(
                ServiceRequest.date_of_request >= six_months_ago
            ).group_by(
                'month'
            ).order_by(
                'month'
            ).all()

            monthly_data = {
                "labels": [],
                "counts": []
            }

            # Process monthly data
            if monthly_requests:
                monthly_data["labels"] = [req[0] for req in monthly_requests]
                monthly_data["counts"] = [req[1] for req in monthly_requests]

            print("Monthly data:", monthly_data)  # Debug print

            # Get top services
            top_services = db.session.query(
                Service.name,
                func.count(ServiceRequest.id).label('count')
            ).join(
                ServiceRequest, Service.id == ServiceRequest.service_id
            ).group_by(
                Service.name
            ).order_by(
                func.count(ServiceRequest.id).desc()
            ).limit(5).all()

            top_services_data = {
                "labels": [service[0] for service in top_services],
                "counts": [service[1] for service in top_services]
            }

            print("Top services:", top_services_data)  # Debug print

            # Get rating distribution
            rating_distribution = [0] * 5  # Initialize array for ratings 1-5
            rated_requests = ServiceRequest.query.filter(
                ServiceRequest.rating.isnot(None)
            ).all()

            for request in rated_requests:
                if 1 <= request.rating <= 5:
                    rating_distribution[request.rating - 1] += 1

            print("Rating distribution:", rating_distribution)  # Debug print

            return {
                "metrics": metrics,
                "statusCounts": status_counts,
                "monthlyData": monthly_data,
                "topServices": top_services_data,
                "ratingDistribution": rating_distribution
            }, 200

        except Exception as e:
            print("Error in SummaryData:", str(e))
            import traceback
            traceback.print_exc()
            return {"message": f"Error fetching summary data: {str(e)}"}, 500

class SearchServiceRequests(Resource):
    @jwt_required()
    def get(self):
        try:
            search_by = request.args.get('searchBy', '')
            search_text = request.args.get('searchText', '')

            print(f"Searching by: {search_by}, text: {search_text}")  # Debug print

            # Base query
            query = ServiceRequest.query

            # Apply filters based on search criteria
            if search_by == 'status':
                query = query.filter(ServiceRequest.service_status.ilike(f'%{search_text}%'))
            elif search_by == 'customer':
                query = query.join(User, ServiceRequest.customer_id == User.id)\
                           .filter(User.name.ilike(f'%{search_text}%'))
            elif search_by == 'professional':
                query = query.join(User, ServiceRequest.professional_id == User.id)\
                           .filter(User.name.ilike(f'%{search_text}%'))
            elif search_by == 'date':
                try:
                    search_date = datetime.strptime(search_text, '%Y-%m-%d').date()
                    query = query.filter(func.date(ServiceRequest.date_of_request) == search_date)
                except ValueError:
                    return {"message": "Invalid date format. Use YYYY-MM-DD"}, 400

            # Execute query
            requests = query.all()
            print(f"Found {len(requests)} matching requests")  # Debug print

            # Format results
            result = []
            for req in requests:
                customer = User.query.get(req.customer_id)
                professional = User.query.get(req.professional_id) if req.professional_id else None
                service = Service.query.get(req.service_id)

                request_data = {
                    "id": req.id,
                    "customer_name": customer.name if customer else "Unknown",
                    "customer_email": customer.email if customer else "Unknown",
                    "professional_name": professional.name if professional else None,
                    "professional_email": professional.email if professional else None,
                    "service_name": service.name if service else "Unknown",
                    "status": req.service_status,
                    "date_of_request": req.date_of_request.isoformat() if req.date_of_request else None,
                    "remarks": req.remarks,
                    "address": customer.address if customer else "Unknown"
                }
                result.append(request_data)

            print("Search results:", result)  # Debug print
            return {"requests": result}, 200

        except Exception as e:
            print("Error searching requests:", str(e))
            import traceback
            traceback.print_exc()  # Print full stack trace
            return {"message": f"Error searching requests: {str(e)}"}, 500

class Logout(Resource):
    def get(self):
        try:
            # Clear any server-side session data if needed
            return {"message": "Logged out successfully!"}, 200
        except Exception as e:
            print(f"Error during logout: {str(e)}")
            return {"message": "Error during logout"}, 500

class GetDocument(Resource):
    @jwt_required()
    def get(self, filename):
        try:
            return send_from_directory(UPLOAD_DIRECTORY, filename)
        except Exception as e:
            return {"message": "Error accessing document"}, 404

class ApproveProfessional(Resource):
    @jwt_required()
    def post(self, professional_id):
        try:
            professional = User.query.filter_by(
                id=professional_id, 
                role='service_professional'
            ).first()
            
            if not professional:
                return {"message": "Professional not found"}, 404

            professional.is_approved = True
            db.session.commit()
            return {"message": "Professional approved successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error approving professional"}, 500

class TestProfessionals(Resource):
    def get(self):
        try:
            users = User.query.filter_by(role="service_professional").all()
            professionals = ServiceProfessional.query.all()
            
            return {
                "message": "Test successful",
                "user_count": len(users),
                "professional_count": len(professionals),
                "users": [{"id": u.id, "name": u.name, "email": u.email} for u in users],
                "professionals": [{"id": p.id, "user_id": p.user_id, "service_name": p.service_name} for p in professionals]
            }, 200
        except Exception as e:
            return {"error": str(e)}, 500

class ToggleUserBlock(Resource):
    @jwt_required()
    def post(self, user_id, action):
        try:
            user = User.query.filter_by(id=user_id, role='customer').first()
            if not user:
                return {"message": "User not found"}, 404
                
            user.is_blocked = action == 'block'
            if user.is_blocked:
                user.is_approved = False
                
            db.session.commit()
            
            return {
                "message": f"User {action}ed successfully",
                "is_blocked": user.is_blocked,
                "is_approved": user.is_approved
            }, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error {action}ing user"}, 500

class ApproveUser(Resource):
    @jwt_required()
    def post(self, user_id):
        try:
            user = User.query.filter_by(id=user_id, role='customer').first()
            if not user:
                return {"message": "User not found"}, 404

            user.is_approved = True
            db.session.commit()
            return {"message": "User approved successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error approving user"}, 500

class ToggleProfessionalApproval(Resource):
    @jwt_required()
    def post(self, professional_id, action):
        try:
            # Verify admin access
            current_user_id = get_jwt_identity()
            admin = User.query.get(current_user_id)
            if not admin or admin.role != 'admin':
                return {"message": "Unauthorized access"}, 403

            # Get the professional
            professional = User.query.filter_by(id=professional_id, role='service_professional').first()
            if not professional:
                return {"message": "Professional not found"}, 404

            # Toggle approval status
            if action == 'approve':
                professional.is_approved = True
                message = "Professional approved successfully"
            elif action == 'unapprove':
                professional.is_approved = False
                message = "Professional unapproved successfully"
            else:
                return {"message": "Invalid action"}, 400

            db.session.commit()
            return {"message": message}, 200

        except Exception as e:
            print("Error toggling professional approval:", str(e))
            db.session.rollback()
            return {"message": "Error updating professional status"}, 500

class ToggleUserApproval(Resource):
    @jwt_required()
    def post(self, user_id, action):
        try:
            user = User.query.filter_by(id=user_id, role='customer').first()
            if not user:
                return {"message": "User not found"}, 404

            if action not in ['approve', 'unapprove']:
                return {"message": "Invalid action"}, 400

            user.is_approved = (action == 'approve')
            db.session.commit()
            
            return {
                "message": f"User {action}d successfully",
                "user_id": user_id,
                "is_approved": user.is_approved
            }, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error {action}ing user"}, 500

class CreateInitialAdmin(Resource):
    def post(self):
        try:
            # Check if admin already exists
            admin = User.query.filter_by(email="admin@example.com").first()
            if admin:
                return {"message": "Admin user already exists"}, 200

            # Create admin user
            admin = User(
                username="admin",
                password=generate_password_hash("admin123"),
                role="admin",
                name="Admin User",
                email="admin@example.com",
                address="Admin Office Address",
                pin_code="123456",
                is_approved=True
            )
            
            print(f"Creating admin user: {admin.email}")  # Debug print
            
            db.session.add(admin)
            db.session.commit()
            
            print("Admin user created successfully")  # Debug print
            
            return {"message": "Admin user created successfully"}, 201
            
        except Exception as e:
            print(f"Error creating admin: {str(e)}")  # Debug print
            db.session.rollback()
            return {"message": f"Error creating admin: {str(e)}"}, 500

class ProfessionalServiceRequests(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user_id = get_jwt_identity()
            professional = User.query.get(current_user_id)
            
            if not professional or professional.role != 'service_professional':
                return {"message": "Unauthorized access"}, 403

            service_requests = ServiceRequest.query\
                .join(User, ServiceRequest.customer_id == User.id)\
                .join(Service, ServiceRequest.service_id == Service.id)\
                .filter(
                    (
                        (ServiceRequest.service_status == 'requested') |
                        (
                            (ServiceRequest.service_status.in_(['accepted', 'completed', 'rejected'])) &
                            (ServiceRequest.professional_id == current_user_id)
                        )
                    )
                )\
                .all()

            result = []
            for req in service_requests:
                customer = User.query.get(req.customer_id)
                service = Service.query.get(req.service_id)
                
                request_data = {
                    "id": req.id,
                    "service_name": service.name if service else "Unknown Service",
                    "price": service.price if service else 0,
                    "customer_name": customer.name if customer else "Unknown Customer",
                    "address": customer.address if customer else "No Address",
                    "date_of_request": req.date_of_request.isoformat(),
                    "date_of_completion": req.date_of_completion.isoformat() if req.date_of_completion else None,
                    "status": req.service_status,
                    "remarks": req.remarks,
                    "rating": req.rating,
                    "rating_comment": req.rating_comment,
                    "rating_date": req.rating_date.isoformat() if req.rating_date else None
                }
                result.append(request_data)

            return {"requests": result}, 200

        except Exception as e:
            print("Error fetching service requests:", str(e))
            import traceback
            traceback.print_exc()
            return {"message": "Error fetching service requests"}, 500

class HandleServiceRequest(Resource):
    @jwt_required()
    def post(self, request_id, action):
        try:
            current_user_id = get_jwt_identity()
            professional = User.query.get(current_user_id)
            
            if not professional or professional.role != 'service_professional':
                return {"message": "Unauthorized access"}, 403

            service_request = ServiceRequest.query.get(request_id)
            if not service_request:
                return {"message": "Service request not found"}, 404

            if action == 'accept':
                service_request.service_status = 'accepted'
                service_request.professional_id = current_user_id
            elif action == 'reject':
                service_request.service_status = 'rejected'
                service_request.professional_id = current_user_id
                service_request.date_of_completion = datetime.utcnow()
            else:
                return {"message": "Invalid action"}, 400

            db.session.commit()
            print(f"Service request {request_id} {action}ed by professional {current_user_id}")  # Debug print
            return {"message": f"Service request {action}ed successfully"}, 200

        except Exception as e:
            print(f"Error {action}ing service request:", str(e))
            db.session.rollback()
            return {"message": f"Error {action}ing service request"}, 500

class CustomerRequests(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user_id = get_jwt_identity()
            print(f"Fetching requests for user {current_user_id}")  # Debug print
            
            # Get all requests for this customer
            requests = ServiceRequest.query\
                .join(Service, ServiceRequest.service_id == Service.id)\
                .outerjoin(User, ServiceRequest.professional_id == User.id)\
                .filter(ServiceRequest.customer_id == current_user_id)\
                .all()

            print(f"Found {len(requests)} requests")  # Debug print

            result = []
            for req in requests:
                service = Service.query.get(req.service_id)
                professional = User.query.get(req.professional_id) if req.professional_id else None
                
                request_data = {
                    "id": req.id,
                    "service_id": req.service_id,
                    "service_name": service.name if service else "Unknown Service",
                    "professional_name": professional.name if professional else None,
                    "status": req.service_status,
                    "date_of_request": req.date_of_request.isoformat(),
                    "remarks": req.remarks,
                    "price": service.price if service else 0
                }
                result.append(request_data)
                print(f"Added request: {request_data}")  # Debug print

            return {"requests": result}, 200

        except Exception as e:
            print("Error fetching customer requests:", str(e))
            import traceback
            traceback.print_exc()  # Print full stack trace
            return {"message": f"Error fetching requests: {str(e)}"}, 500

class CompleteServiceRequest(Resource):
    @jwt_required()
    def post(self, request_id):
        try:
            current_user_id = get_jwt_identity()
            
            # Get the service request
            service_request = ServiceRequest.query.get(request_id)
            
            if not service_request:
                return {"message": "Service request not found"}, 404
                
            # Verify this is the customer's request
            if service_request.customer_id != int(current_user_id):
                return {"message": "Unauthorized access"}, 403
                
            # Get data from request
            data = request.get_json()
            
            # Update the request status and details
            service_request.service_status = 'completed'
            service_request.date_of_completion = datetime.utcnow()
            
            # Handle rating
            if 'rating' in data:
                service_request.rating = data['rating']
                service_request.rating_date = datetime.utcnow()
                
                # Update professional's average rating
                professional = ServiceProfessional.query.filter_by(
                    user_id=service_request.professional_id
                ).first()
                
                if professional:
                    # Update total ratings and calculate new average
                    if professional.total_ratings == 0:
                        professional.average_rating = float(data['rating'])
                    else:
                        current_total = professional.average_rating * professional.total_ratings
                        new_total = current_total + float(data['rating'])
                        professional.average_rating = new_total / (professional.total_ratings + 1)
                    
                    professional.total_ratings += 1
            
            # Add remarks if provided
            if 'remarks' in data:
                service_request.remarks = data['remarks']
            
            # Add rating comment if provided
            if 'rating_comment' in data:
                service_request.rating_comment = data['rating_comment']
            
            db.session.commit()
            
            return {
                "message": "Service request completed successfully",
                "rating": service_request.rating,
                "rating_date": service_request.rating_date.isoformat() if service_request.rating_date else None
            }, 200
            
        except Exception as e:
            print("Error completing service request:", str(e))
            db.session.rollback()
            return {"message": "Error completing service request"}, 500

class CloseServiceRequest(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()
            
            service_id = data.get('service_id')
            remarks = data.get('remarks', '')
            
            # Get the service request
            service_request = ServiceRequest.query.get(service_id)
            
            if not service_request:
                return {"message": "Service request not found"}, 404
                
            # Verify this is the customer's request
            if service_request.customer_id != int(current_user_id):
                return {"message": "Unauthorized access"}, 403
                
            # Update the request status and remarks
            service_request.service_status = 'completed'
            if remarks:
                service_request.remarks = remarks
                
            # Set completion date
            service_request.date_of_completion = datetime.utcnow()
            
            db.session.commit()
            
            return {"message": "Service request closed successfully"}, 200
            
        except Exception as e:
            print("Error closing service request:", str(e))
            db.session.rollback()
            return {"message": "Error closing service request"}, 500

class ServiceProviders(Resource):
    @jwt_required()
    def get(self, service_id):
        try:
            # Get all service professionals who can provide this service
            professionals = ServiceProfessional.query\
                .join(User)\
                .filter(User.is_approved == True)\
                .filter(User.is_blocked == False)\
                .all()

            providers_list = [{
                "id": prof.user.id,
                "name": prof.user.name,
                "experience_years": prof.experience_years,
                "service_name": prof.service_name,
                "rating": 4.5  # You can add actual rating logic here
            } for prof in professionals]

            return {"providers": providers_list}, 200

        except Exception as e:
            print("Error fetching service providers:", str(e))
            return {"message": "Error fetching service providers"}, 500

class CustomerProfile(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user:
                return {"message": "User not found"}, 404

            return {
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "pin_code": user.pin_code
            }, 200

        except Exception as e:
            print("Error fetching profile:", str(e))
            return {"message": "Error fetching profile"}, 500

    @jwt_required()
    def put(self):
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user:
                return {"message": "User not found"}, 404

            data = request.get_json()
            
            # Update user fields
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
            user.address = data.get('address', user.address)
            user.pin_code = data.get('pin_code', user.pin_code)

            db.session.commit()
            return {"message": "Profile updated successfully"}, 200

        except Exception as e:
            print("Error updating profile:", str(e))
            db.session.rollback()
            return {"message": "Error updating profile"}, 500

class ProfessionalProfile(Resource):
    @jwt_required()
    def get(self, professional_id=None):
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)

            # If no professional_id is provided, return current user's profile
            if professional_id is None:
                if current_user.role != 'service_professional':
                    return {"message": "Unauthorized access"}, 403
                professional_id = current_user_id
            # If professional_id is provided, check if user is admin
            elif current_user.role != 'admin':
                return {"message": "Unauthorized access"}, 403

            # Get professional profile with ratings
            professional = User.query.join(ServiceProfessional)\
                .filter(User.id == professional_id)\
                .filter(User.role == 'service_professional')\
                .first()

            if not professional:
                return {"message": "Professional not found"}, 404

            prof_details = ServiceProfessional.query.filter_by(user_id=professional_id).first()

            # Get all completed service requests with ratings
            rated_services = ServiceRequest.query.filter(
                ServiceRequest.professional_id == professional_id,
                ServiceRequest.service_status == 'completed',
                ServiceRequest.rating.isnot(None)
            ).all()

            # Calculate average rating
            total_ratings = len(rated_services)
            avg_rating = 0
            if total_ratings > 0:
                avg_rating = sum(req.rating for req in rated_services) / total_ratings

            # Get recent ratings (last 5)
            recent_ratings = [{
                'rating': req.rating,
                'comment': req.rating_comment,
                'date': req.rating_date.isoformat() if req.rating_date else None
            } for req in rated_services[-5:]]

            return {
                "id": professional.id,
                "username": professional.username,
                "name": professional.name,
                "email": professional.email,
                "address": professional.address,
                "pin_code": professional.pin_code,
                "service_name": prof_details.service_name,
                "experience_years": prof_details.experience_years,
                "document_upload": prof_details.document_upload,
                "average_rating": round(avg_rating, 1),
                "total_ratings": total_ratings,
                "recent_ratings": recent_ratings,
                "created_at": professional.created_at.isoformat(),
                "is_blocked": professional.is_blocked,
                "is_approved": professional.is_approved
            }, 200

        except Exception as e:
            print("Error fetching professional profile:", str(e))
            return {"message": "Error fetching professional profile"}, 500

    @jwt_required()
    def put(self):
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            professional = ServiceProfessional.query.filter_by(user_id=current_user_id).first()
            
            if not user or not professional:
                return {"message": "Professional not found"}, 404

            data = request.get_json()
            
            # Update user fields
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
            user.address = data.get('address', user.address)
            user.pin_code = data.get('pin_code', user.pin_code)

            # Update professional fields
            professional.service_name = data.get('service_name', professional.service_name)
            professional.experience_years = data.get('experience_years', professional.experience_years)

            db.session.commit()
            return {"message": "Profile updated successfully"}, 200

        except Exception as e:
            print("Error updating profile:", str(e))
            db.session.rollback()
            return {"message": "Error updating profile"}, 500

class CustomerServiceHistory(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user_id = get_jwt_identity()
            print(f"Fetching history for user {current_user_id}")  # Debug print
            
            # Get all service requests for this customer
            history = ServiceRequest.query\
                .join(Service, ServiceRequest.service_id == Service.id)\
                .outerjoin(User, ServiceRequest.professional_id == User.id)\
                .filter(ServiceRequest.customer_id == current_user_id)\
                .order_by(ServiceRequest.date_of_request.desc())\
                .all()

            print(f"Found {len(history)} history records")  # Debug print

            result = []
            for req in history:
                service = Service.query.get(req.service_id)
                professional = User.query.get(req.professional_id) if req.professional_id else None
                
                request_data = {
                    "id": req.id,
                    "service_name": service.name if service else "Unknown Service",
                    "professional_name": professional.name if professional else None,
                    "status": req.service_status,
                    "date_of_request": req.date_of_request.isoformat() if req.date_of_request else None,
                    "date_of_completion": req.date_of_completion.isoformat() if req.date_of_completion else None,
                    "price": service.price if service else 0,
                    "rating": req.rating if hasattr(req, 'rating') else None,
                    "remarks": req.remarks
                }
                result.append(request_data)
                print(f"Added history record: {request_data}")  # Debug print

            return {"history": result}, 200

        except Exception as e:
            print("Error fetching service history:", str(e))
            import traceback
            traceback.print_exc()  # Print full stack trace
            return {"message": f"Error fetching service history: {str(e)}"}, 500

class UserProfile(Resource):
    @jwt_required()
    def get(self, user_id):
        try:
            # Check if admin
            current_user_id = get_jwt_identity()
            admin = User.query.get(current_user_id)
            if not admin or admin.role != 'admin':
                return {"message": "Unauthorized access"}, 403

            # Get user profile
            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404

            return {
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "address": user.address,
                "pin_code": user.pin_code,
                "created_at": user.created_at.isoformat(),
                "is_blocked": user.is_blocked,
                "is_approved": user.is_approved
            }, 200

        except Exception as e:
            print("Error fetching user profile:", str(e))
            return {"message": "Error fetching user profile"}, 500

class AdminServiceRequests(Resource):
    @jwt_required()
    def get(self):
        try:
            # Verify admin access
            current_user_id = get_jwt_identity()
            admin = User.query.get(current_user_id)
            if not admin or admin.role != 'admin':
                return {"message": "Unauthorized access"}, 403

            # Create aliases for the User table to handle multiple joins
            CustomerAlias = aliased(User)
            ProfessionalAlias = aliased(User)

            # Get all service requests with related data
            requests = ServiceRequest.query\
                .join(Service, ServiceRequest.service_id == Service.id)\
                .join(CustomerAlias, ServiceRequest.customer_id == CustomerAlias.id)\
                .outerjoin(ProfessionalAlias, ServiceRequest.professional_id == ProfessionalAlias.id)\
                .all()

            result = []
            for req in requests:
                service = Service.query.get(req.service_id)
                customer = CustomerAlias.query.get(req.customer_id)
                professional = ProfessionalAlias.query.get(req.professional_id) if req.professional_id else None

                # For accepted requests, use date_of_request as acceptance date
                acceptance_date = None
                if req.service_status == 'accepted':
                    acceptance_date = req.date_of_request.isoformat() if req.date_of_request else None

                request_data = {
                    "id": req.id,
                    "service_name": service.name if service else "Unknown Service",
                    "customer_name": customer.name if customer else "Unknown Customer",
                    "professional_name": professional.name if professional else None,
                    "status": req.service_status,
                    "date_of_request": req.date_of_request.isoformat() if req.date_of_request else None,
                    "date_of_acceptance": acceptance_date,  # Use the acceptance date we determined
                    "date_of_completion": req.date_of_completion.isoformat() if req.date_of_completion else None,
                    "rating": req.rating,
                    "remarks": req.remarks
                }
                result.append(request_data)

            print(f"Found {len(result)} service requests")  # Debug print
            return {"requests": result}, 200

        except Exception as e:
            print("Error fetching service requests:", str(e))
            import traceback
            traceback.print_exc()  # Print full stack trace
            return {"message": "Error fetching service requests"}, 500

# Add to your routes
api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(AdminDashboard, '/admin/dashboard')
api.add_resource(CreateService, '/admin/service')
api.add_resource(EditService, '/admin/service/<int:service_id>')
api.add_resource(DeleteService, '/admin/service/<int:service_id>')
api.add_resource(ListAllUsers, '/admin/users')
api.add_resource(ListServiceProfessionals, '/admin/service-professionals')
api.add_resource(BlockServiceProfessional, '/admin/professional/<int:professional_id>/block')
api.add_resource(ServiceRequestResource, '/customer/service_request', '/customer/service_request/<int:request_id>')
api.add_resource(SummaryData, '/admin/summary')
api.add_resource(SearchServiceRequests, '/admin/search-requests', endpoint='searchservicerequests')
api.add_resource(Logout, '/logout')
api.add_resource(ApproveService, '/admin/services/<int:service_id>/approve')
api.add_resource(RejectService, '/admin/services/<int:service_id>/reject')
api.add_resource(UserInfo, '/api/user-info')
api.add_resource(ListServices, '/admin/listservices')
api.add_resource(ToggleProfessionalBlock, '/admin/professional/<int:professional_id>/<string:action>/block')
api.add_resource(CreateInitialAdmin, '/create-initial-admin')
api.add_resource(GetDocument, '/uploads/<path:filename>')
api.add_resource(ApproveProfessional, '/admin/professional/<int:professional_id>/approve')
api.add_resource(TestProfessionals, '/test/professionals')
api.add_resource(ToggleUserBlock, '/admin/user/<int:user_id>/<string:action>')
api.add_resource(ApproveUser, '/admin/user/<int:user_id>/approve')
api.add_resource(ToggleProfessionalApproval, '/admin/professional/<int:professional_id>/<string:action>/approval')
api.add_resource(ToggleUserApproval, '/admin/user/<int:user_id>/<string:action>', endpoint='toggle_user_approval')
api.add_resource(ProfessionalServiceRequests, '/professional/service-requests')
api.add_resource(HandleServiceRequest, '/professional/service-request/<int:request_id>/<string:action>')
api.add_resource(CustomerRequests, '/customer/my-requests')
api.add_resource(CompleteServiceRequest, '/customer/service_request/<int:request_id>/complete')
api.add_resource(CloseServiceRequest, '/customer/close_service')
api.add_resource(ServiceProviders, '/service/<int:service_id>/providers')
api.add_resource(CustomerProfile, '/customer/profile')
api.add_resource(ProfessionalProfile, '/professional/profile', '/admin/professional/<int:professional_id>/profile')
api.add_resource(CustomerServiceHistory, '/customer/service_history')
api.add_resource(UserProfile, '/admin/user/<int:user_id>/profile')
api.add_resource(AdminServiceRequests, '/admin/service-requests')