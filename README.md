# Household Services Management System

## Project Overview
A comprehensive web application for managing household services, connecting customers with service professionals, and handling service requests with real-time notifications.

## Features
- User Authentication & Authorization
- Multiple User Roles (Admin, Customer, Service Professional)
- Service Request Management
- Real-time Email Notifications
- Professional Rating System
- Admin Dashboard with Analytics
- Service Professional Approval System
- Customer Service History
- Asynchronous Task Processing

## Tech Stack
### Backend
- Flask (Python Web Framework)
- SQLAlchemy (ORM)
- Flask-RESTful (API Development)
- Flask-JWT-Extended (Authentication)
- Celery (Asynchronous Tasks)
- Redis (Message Broker)
- MailHog (Email Testing)

### Frontend
- Vue.js
- Vuetify
- Axios
- Vuex

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js
- Redis Server
- MailHog
- SQLite

### Backend Setup
1. Create virtual environment:

```bash
python -m venv myenv
source myenv 
