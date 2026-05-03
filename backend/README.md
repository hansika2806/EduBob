# EduBob Backend

FastAPI backend with SQLite database for EduBob educational platform.

**Current Phase: Phase 3 - Code Review & Codebase Analysis**

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

### Assignments (Phase 2)
- **POST** `/api/assignments/generate` - Generate assignment from Bob IDE output
  ```json
  {
    "topic": "Python Functions",
    "difficulty": "beginner",
    "bob_output": "... Bob IDE session output ..."
  }
  ```

- **POST** `/assignments` - Create assignment manually
- **GET** `/assignments` - List all assignments
- **GET** `/assignments/{assignment_id}` - Get specific assignment

### Submissions (Phase 2)
- **POST** `/submissions` - Submit code for validation
  ```json
  {
    "student_id": 1,
    "assignment_id": 1,
    "code": "def add(a, b): return a + b"
  }
  ```

- **GET** `/submissions` - List submissions (filterable by student/assignment)
- **GET** `/submissions/{submission_id}` - Get specific submission

### Code Review (Phase 3) ⭐ NEW
- **POST** `/api/review/spec-check` - Review student code against specification
  ```json
  {
    "student_code": "def calculate_sum(numbers): ...",
    "assignment_spec": "Create a function that...",
    "bob_output": "... Bob IDE review output ..."
  }
  ```
  
  **Response:**
  ```json
  {
    "summary_feedback": "Overall assessment",
    "mistakes": ["List of identified mistakes"],
    "improvement_suggestions": ["List of suggestions"]
  }
  ```

### Codebase Analysis (Phase 3) ⭐ NEW
- **POST** `/api/codebase/analyze` - Analyze repository structure
  ```json
  {
    "repo_url": "https://github.com/user/repo",
    "bob_output": "... Bob IDE codebase analysis ..."
  }
  ```
  
  **Response:**
  ```json
  {
    "architecture_summary": "High-level architecture description",
    "key_files": [
      {"file": "app.py", "purpose": "Main entry point"}
    ],
    "tech_stack": ["Flask", "SQLAlchemy", "PostgreSQL"],
    "explanation": "Detailed explanation of codebase"
  }
  ```

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
- `test_results`: Text (JSON string)
- `passed_tests`: Integer
- `failed_tests`: Integer
- `total_tests`: Integer
- `error_message`: Text
- `review_feedback`: Text (JSON string) - **Phase 3**

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

## Testing Phase 3

Run the Phase 3 test suite:
```bash
python backend/test_phase3.py
```

This will test:
- Code review endpoint (`/api/review/spec-check`)
- Codebase analysis endpoint (`/api/codebase/analyze`)

## Implementation Phases

### Phase 1: Foundation ✅
- Basic FastAPI setup
- SQLite database with SQLAlchemy
- Core models (Student, Assignment, Submission, Mistake)
- Health check endpoint
- Student CRUD endpoints
- Environment configuration

### Phase 2: Assignment Generation & Validation ✅
- Bob IDE integration (manual output parsing)
- Assignment generation from Bob output
- Code validation engine with test cases
- Safe code execution with timeout protection
- Assignment and submission CRUD endpoints

### Phase 3: Code Review & Codebase Analysis ✅
- **Code Review System**: Analyze student submissions against specifications
- **Codebase Analyzer**: Analyze repository structure and architecture
- Bob IDE output parsing for intelligent feedback
- Review feedback storage in submissions
- Structured response schemas

## Important Notes

### Bob IDE Integration
All Bob IDE interactions are **manual**:
- Bob IDE output is obtained through Ask mode sessions
- Output is pasted into API requests as `bob_output` parameter
- No subprocess calls or CLI automation
- No external integrations or GitHub cloning

### Phase 3 Constraints
- ✅ No frontend required
- ✅ No GitHub cloning or gitpython
- ✅ No subprocess or CLI usage
- ✅ Uses existing project structure
- ✅ Manual Bob IDE output only