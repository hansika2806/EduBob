# EduBob Backend - Phase 1

FastAPI backend with SQLite database for EduBob educational platform.

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   - Copy `.env` file and adjust settings if needed
   - Default database: `sqlite:///./edubob.db`

3. **Run the server**:
   ```bash
   python main.py
   ```
   
   Or with uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### Health Check
- **GET** `/health` - Returns server status

### Students
- **POST** `/students` - Create a new student
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "role": "student"
  }
  ```

- **GET** `/students` - List all students (with pagination)
  - Query params: `skip` (default: 0), `limit` (default: 100)

- **GET** `/students/{student_id}` - Get specific student by ID

## Database Models

### Student
- `id`: Integer (Primary Key)
- `name`: String (100)
- `email`: String (100, Unique)
- `role`: String (20, default: "student")

### Assignment
- `id`: Integer (Primary Key)
- `title`: String (200)
- `description`: Text
- `test_cases`: Text (JSON string)

### Submission
- `id`: Integer (Primary Key)
- `student_id`: Integer (Foreign Key)
- `assignment_id`: Integer (Foreign Key)
- `code`: Text
- `status`: String (20, default: "pending")
- `timestamp`: DateTime

### Mistake
- `id`: Integer (Primary Key)
- `student_id`: Integer (Foreign Key)
- `pattern`: Text (JSON string)
- `count`: Integer (default: 1)
- `last_seen`: DateTime

## Testing

Access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Phase 1 Scope

✅ Basic FastAPI setup
✅ SQLite database with SQLAlchemy
✅ Core models (Student, Assignment, Submission, Mistake)
✅ Health check endpoint
✅ Student CRUD endpoints
✅ Environment configuration
✅ .gitignore setup

❌ Authentication (Phase 1+)
❌ Bob integration (Phase 2+)
❌ Code execution (Phase 2+)