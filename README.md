# HNG Stage 1 - Profile Management API

## 📋 Overview

This REST API integrates three external services (Genderize, Agify, and Nationalize) to predict gender, age, and nationality based on a person's name. All data is stored in a database with UUID v7 identifiers and UTC timestamps. The API provides endpoints for creating, retrieving, filtering, and deleting profiles with built-in idempotency.

## 🚀 Live API

- **Base URL**: `https://profileapi.pythonanywhere.com/`
- **Documentation**: `https://profileapi.pythonanywhere.com/`

## 📡 API Endpoints

### 1. Create Profile
**POST** `/api/profiles`

Creates a new profile by fetching data from Genderize, Agify, and Nationalize APIs.

**Request Body:**
```json
{
  "name": "Pearl"
}

Response (201 Created):

json
{
  "status": "success",
  "data": {
    "id": "e84b197e-94c9-4bb5-b8c4-26d19dab6201",
    "name": "pearl",
    "gender": "female",
    "gender_probability": 0.99,
    "sample_size": 97517,
    "age": 53,
    "age_group": "adult",
    "country_id": "CM",
    "country_probability": 0.0968,
    "created_at": "2026-04-16T11:04:30.200197Z"
  }
}
Response (200 OK - Profile already exists):

json
{
  "status": "success",
  "message": "Profile already exists",
  "data": { ... }
}
2. Get All Profiles
GET /api/profiles

Retrieves all profiles with optional filtering.
Query Parameters (all optional):
gender - Filter by gender (male/female) - case insensitive
country_id - Filter by country code (NG, US, etc.) - case insensitive
age_group - Filter by age group (child/teenager/adult/senior) - case insensitive

Examples:

text
GET /api/profiles?gender=male
GET /api/profiles?country_id=NG
GET /api/profiles?gender=female&age_group=adult
Response (200 OK):

json
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "id": "d7e2510a-7680-4268-a963-7e870bec229a",
      "name": "john",
      "gender": "male",
      "age": 75,
      "age_group": "senior",
      "country_id": "NG"
    },
    {
      "id": "e84b197e-94c9-4bb5-b8c4-26d19dab6201",
      "name": "ella",
      "gender": "female",
      "age": 53,
      "age_group": "adult",
      "country_id": "CM"
    }
  ]
}
3. Get Single Profile
GET /api/profiles/{id}

Retrieves a specific profile by its UUID.

Response (200 OK):

json
{
  "status": "success",
  "data": {
    "id": "e84b197e-94c9-4bb5-b8c4-26d19dab6201",
    "name": "ella",
    "gender": "female",
    "gender_probability": 0.99,
    "sample_size": 97517,
    "age": 53,
    "age_group": "adult",
    "country_id": "CM",
    "country_probability": 0.0968,
    "created_at": "2026-04-16T11:04:30.200197Z"
  }
}
4. Delete Profile
DELETE /api/profiles/{id}
Permanently removes a profile from the database.
Response: 204 No Content
```

##🔧 Classification Rules
Age Groups
Age Range	Age Group
0 - 12	child
13 - 19	teenager
20 - 59	adult
60+	senior
Nationality
Selects the country with the highest probability from the Nationalize API response.


## ⚠️ Error Responses
All errors follow this structure:

json
{
  "status": "error",
  "message": "<error message>"
}
Status Code	Meaning	Example
400	Missing or empty name	{"status": "error", "message": "Missing or empty name"}
422	Invalid type	{"status": "error", "message": "Invalid type"}
404	Profile not found	{"status": "error", "message": "Profile not found"}
502	External API error	{"status": "error", "message": "Genderize returned an invalid response"}
External API Error Messages
Genderize returned an invalid response

Agify returned an invalid response

Nationalize returned an invalid response

## 🛠️ Technology Stack
Framework: Django 6.0.4
API Framework: Django REST Framework 3.17.1
Database: SQLite (development) / PostgreSQL (production)
HTTP Client: Requests library
CORS: django-cors-headers
Server: Gunicorn (production)

## 📦 External APIs Used
API	Purpose	Endpoint
Genderize	Gender prediction	https://api.genderize.io
Agify	Age prediction	https://api.agify.io
Nationalize	Nationality prediction	https://api.nationalize.io
🚀 Local Development Setup
Prerequisites
Python 3.11 or higher

pip package manager

Installation Steps
Clone the repository

bash
```
git clone https://github.com/FavieCodes/Hng14_backend_python_task_zero.git
cd Hng14_backend_python_task_zero
Create and activate virtual environment

bash
# Windows
python -m venv env
env\Scripts\activate

# Linux/Mac
python3 -m venv env
source env/bin/activate
Install dependencies

bash
pip install -r requirements.txt
Run migrations

bash
python manage.py makemigrations profiles
python manage.py migrate
Start the development server

bash
python manage.py runserver
Test the API
```

```
bash
# Create a profile
curl -X POST http://127.0.0.1:8000/api/profiles \
  -H "Content-Type: application/json" \
  -d '{"name": "john"}'

# Get all profiles
curl http://127.0.0.1:8000/api/profiles

# Get single profile (replace {id} with actual ID)
curl http://127.0.0.1:8000/api/profiles/{id}

# Delete profile
curl -X DELETE http://127.0.0.1:8000/api/profiles/{id}
```
## 🌐 Deployment
Deploying to PythonAnywhere
Push code to GitHub

bash
git add .
git commit -m "Ready for deployment"
git push origin master
On PythonAnywhere:

Create a new web app with manual configuration
Clone your repository
Set up virtual environment
Configure WSGI file
Set static files path
Reload the web app
Run migrations on server

bash
```
cd ~/Hng14_backend_python_task_zero
python manage.py migrate
```

## 🧪 Testing
Sample Test Cases
bash
# Test creating a profile
curl -X POST https://yourapp.pythonanywhere.com/api/profiles \
  -H "Content-Type: application/json" \
  -d '{"name": "emmanuel"}'

# Test idempotency (same name again)
curl -X POST https://yourapp.pythonanywhere.com/api/profiles \
  -H "Content-Type: application/json" \
  -d '{"name": "emmanuel"}'

# Test filtering
curl "https://yourapp.pythonanywhere.com/api/profiles?gender=male"
curl "https://yourapp.pythonanywhere.com/api/profiles?country_id=NG"
curl "https://yourapp.pythonanywhere.com/api/profiles?age_group=adult"

# Test error handling
curl -X POST https://yourapp.pythonanywhere.com/api/profiles \
  -H "Content-Type: application/json" \
  -d '{"name": ""}'
```

## 📊 Database Schema

```python
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=20)
    gender_probability = models.FloatField()
    sample_size = models.IntegerField()
    age = models.IntegerField()
    age_group = models.CharField(max_length=20)
    country_id = models.CharField(max_length=5)
    country_probability = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
```

## 🔒 Environment Variables
For production deployment, set these environment variables:

bash
```
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.pythonanywhere.com
DATABASE_URL=postgresql://user:password@host:port/dbname
```

## 📝 Features Implemented
✅ Multi-API integration (Genderize, Agify, Nationalize)
✅ Data persistence with SQLite/PostgreSQL
✅ Idempotent profile creation (no duplicates)
✅ UUID v7 for unique identifiers
✅ UTC timestamps in ISO 8601 format
✅ Case-insensitive filtering
✅ Comprehensive error handling
✅ CORS enabled for cross-origin requests
✅ RESTful API design
✅ Interactive API documentation

## 🐛 Error Handling
The API handles various error scenarios:
Missing or empty name parameters
Invalid data types
External API failures (502 Bad Gateway)
Profile not found (404)
Duplicate profile creation (returns existing)

## 📄 License
MIT License - feel free to use this project for learning and development.

## 👨‍💻 Author
Imo Emmanuel Udoh - HNG Cohort 14 Backend Track

## 🙏 Acknowledgments
HNG Internship for the project requirements
Genderize.io, Agify.io, and Nationalize.io for their free APIs
Django REST Framework community

## 📞 Support
For issues or questions:
GitHub Issues: Create an issue
Email: [imo.e.udoh@gmail.com]
Built with ❤️ for HNG Cohort 14

