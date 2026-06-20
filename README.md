# Workout Tracker API

A RESTful Workout Tracker API built with FastAPI, PostgreSQL, SQLAlchemy, and JWT authentication. This API helps users create workout plans, schedule workouts, track progress, and generate workout reports.

Project idea from roadmap.sh:
https://roadmap.sh/projects/fitness-workout-tracker

- Language: Python (100%)
- Repo: bonaarhousell/workout-tracker
- Description: Project Workout Tracker using FastAPI

## Features

### Authentication
- User registration
- User login
- JWT authentication (access tokens)
- Protected routes and role-based (admin/user) access

### Exercise Management
- Seed exercise database
- Create exercise (admin only)
- Filter exercises by category

Supported categories:
- Chest
- Back
- Shoulder
- Arms
- Leg
- Core

### Workout Management
- Create, update, and delete workouts
- Update workout status
- Schedule workouts
- View workout details
- Add exercises (with sets/reps/weight) to workouts
- Filter workouts by status

Workout statuses:
- Pending
- Completed
- Cancelled

### Reports
Generate workout reports including:
- Total workouts
- Completed workouts
- Pending workouts
- Cancelled workouts

## Tech Stack
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT Authentication
- Pytest

## Database Schema

### Users
| Field         | Type    |
| ------------- | ------- |
| id_user       | Integer |
| username      | String  |
| email         | String  |
| password_hash | String  |
| role          | String  |

### Exercises
| Field       | Type    |
| ----------- | ------- |
| id_exercise | Integer |
| title       | String  |
| description | String  |
| category    | String  |

### Workouts
| Field       | Type     |
| ----------- | -------- |
| id_workout  | Integer  |
| id_user     | Integer  |
| title       | String   |
| schedule_at | DateTime |
| comment     | String   |
| status      | String   |
| created_at  | DateTime |
| update_at   | DateTime |

### Workout Exercises
| Field       | Type    |
| ----------- | ------- |
| id_workout  | Integer |
| id_exercise | Integer |
| sets        | Integer |
| reps        | Integer |
| weight      | Integer |

## Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL
- Git

### Clone repository
```bash
git clone https://github.com/bonaarhousell/workout-tracker.git
cd workout-tracker
```

### Create & activate virtual environment
```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Configure environment variables
Create a `.env` file in the project root with the following (example):
```env
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=workout_tracker
DB_PORT=5432
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Adjust values to your environment. For production, store secrets securely and do not commit `.env`.

### Database
Create the database in PostgreSQL before running the app:
```sql
CREATE DATABASE workout_tracker;
```

If using SQLAlchemy ORM migrations, consider adding Alembic for schema migrations (see Future Improvements).

### Run the application
```bash
uvicorn app.main:app --reload
```

Open the interactive API docs:
http://127.0.0.1:8000/docs

## Authentication & Example Requests

Register:
```bash
curl -X POST "http://127.0.0.1:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","email":"user1@example.com","password":"password123"}'
```

Login (get JWT):
```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user1&password=password123"
```

Use the access token for protected endpoints:
```bash
curl -H "Authorization: Bearer <ACCESS_TOKEN>" \
  http://127.0.0.1:8000/workouts
```

(Replace endpoint paths according to your implementation; check /docs for full spec.)

## Testing
Run tests with pytest:
```bash
pytest
```

Add tests for authentication flows, exercise seeding, workout lifecycle, and report generation.

## Deployment
Basic recommendations:
- Use environment variables for configuration
- Run behind a production server (e.g., Uvicorn + Gunicorn)
- Use a managed PostgreSQL or properly secured DB server
- Set up HTTPS (TLS/SSL)
- Add logging and monitoring

## Future Improvements / Roadmap
- Pagination for listing endpoints
- Refresh token / token rotation
- Docker + Docker Compose for local development and production
- CI/CD pipeline (GitHub Actions)
- Automated deployment (e.g., to Heroku, AWS, GCP)
- Alembic database migrations
- Rate limiting and brute-force protection
- API versioning and more granular role permissions

## Contributing
Contributions are welcome. Suggested workflow:
1. Fork the repo
2. Create a feature branch
3. Add tests for new behavior
4. Open a pull request describing the change

Please follow the repository code style and include tests for new features.

## Acknowledgements
Built with FastAPI and the excellent Python open-source ecosystem.
