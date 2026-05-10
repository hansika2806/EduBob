# EduBob Backend

FastAPI backend with SQLite database for EduBob educational platform.

**Current Status: All Phases Complete ✅**

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   - Copy `.env` file and adjust settings if needed
   - Default database: `sqlite:///./edubob.db`
   - Optional: Add watsonx.ai credentials for AI pattern analysis

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
- **GET** `/health` - Returns server status and timestamp

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

### Code Review (Phase 3) ⭐
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

  **Note**: Code review results are generated from IBM Bob IDE Ask mode analysis output, ensuring accurate and context-aware feedback.

### Codebase Analysis (Phase 3) ⭐
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

### Dashboard (Phase 4) ⭐ NEW
- **GET** `/api/dashboard/class-stats` - Get class-wide statistics
  ```json
  {
    "total_submissions": 150,
    "common_errors": ["Missing base cases in recursive functions"],
    "struggling_concepts": ["Recursion", "List comprehensions"],
    "ai_reasoning": "Analysis of error patterns...",
    "analysis_method": "watsonx.ai granite-3-8b-instruct"
  }
  ```

- **GET** `/api/dashboard/assignment-stats/{assignment_id}` - Get assignment-specific statistics
  ```json
  {
    "assignment_id": 1,
    "total_submissions": 25,
    "passed": 15,
    "failed": 10,
    "average_score": 75.5,
    "common_mistakes": ["Off-by-one errors"]
  }
  ```

- **GET** `/api/dashboard/student-progress/{student_id}` - Get individual student progress
  ```json
  {
    "student_id": 1,
    "total_submissions": 12,
    "passed": 8,
    "failed": 4,
    "success_rate": 66.7,
    "recent_mistakes": ["Type errors", "Logic errors"],
    "recommendations": ["Focus on type checking", "Review conditional logic"]
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
- `starter_code`: Text
- `hints`: Text (JSON string)
- `topic`: String (100)
- `difficulty`: String (20)
- `created_at`: DateTime

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

## Services

### Bob Client (`services/bob_client.py`)
- Parses Bob IDE output for assignment generation
- Extracts structured data from Bob responses
- Manual integration (no subprocess calls)

### Validator (`services/validator.py`)
- Safe code execution with RestrictedPython
- Test case validation
- Timeout protection (5 seconds per test)
- Memory limit enforcement

### Review Service (`services/review_service.py`)
- Parses Bob IDE code review output
- Extracts feedback, mistakes, and suggestions
- Structured response formatting

### Codebase Service (`services/codebase_service.py`)
- Parses Bob IDE codebase analysis
- Extracts architecture, key files, and tech stack
- Repository understanding without cloning

### watsonx Client (`services/watsonx_client.py`) ⭐ NEW
- Integrates with watsonx.ai granite-3-8b-instruct model
- Analyzes error patterns from student submissions
- Provides AI-powered insights and recommendations
- Intelligent fallback when API not configured

## Middleware

### Security Headers (`middleware/security_headers.py`)
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security

### Rate Limiter (`middleware/rate_limiter.py`)
- 100 requests per minute per IP
- Prevents API abuse
- Configurable limits

### Authentication (`middleware/auth.py`)
- Simple role-based access control
- JWT token validation (future enhancement)

## Utilities

### Logging Filter (`utils/logging_filter.py`)
- Filters sensitive data from logs
- Redacts passwords, API keys, tokens
- Secure logging practices

### Backup (`utils/backup.py`)
- Automated database backups
- Gzip compression
- Backup on startup
- Stored in `backups/` directory

### Monitoring (`utils/monitoring.py`)
- Performance metrics
- Error tracking
- Health check monitoring

## Testing

Access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Test Scripts

Run the test suites:
```bash
python backend/test_phase2.py  # Assignment generation & validation
python backend/test_phase3.py  # Code review & codebase analysis
python backend/test_api.py     # General API endpoints
```

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

### Phase 4: Dashboard & Analytics ✅
- **watsonx.ai Integration**: Pattern analysis with granite-3-8b-instruct
- **Mistake Pattern Tracking**: Automatic error pattern detection
- **Class Dashboard**: Aggregate statistics and AI insights
- **Student Progress**: Individual tracking and recommendations
- **Intelligent Fallback**: Works without watsonx.ai API configured

## Important Notes

### Bob IDE Integration
All Bob IDE interactions are **manual**:
- Bob IDE output is obtained through Ask mode sessions
- Output is pasted into API requests as `bob_output` parameter
- No subprocess calls or CLI automation
- No external integrations or GitHub cloning

### watsonx.ai Integration
- Uses granite-3-8b-instruct model for pattern analysis
- Requires API key and project ID in `.env` file
- Intelligent fallback when API not configured
- Analyzes error messages to identify patterns
- Provides actionable recommendations

### Security Features
- Rate limiting on all endpoints
- Security headers middleware
- Safe code execution sandbox
- Input validation and sanitization
- Sensitive data filtering in logs
- Automated database backups

### Database Backups
- Automatic backup on server startup
- Backups stored in `backend/backups/`
- Gzip compressed for space efficiency
- Timestamped filenames

## Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=sqlite:///./edubob.db

# watsonx.ai (Optional)
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here

# Server
HOST=0.0.0.0
PORT=8000
```

## Performance Considerations

- SQLite suitable for < 1000 students
- Add indexes on foreign keys for better performance
- Consider PostgreSQL for production scale (> 5000 students)
- Rate limiting prevents API abuse
- Automated backups ensure data safety

## Future Enhancements

- JWT authentication system
- PostgreSQL migration for production
- Docker containerization
- Real-time WebSocket updates
- Enhanced caching layer
- Distributed task queue for long-running operations

## Troubleshooting

### Database Issues
- Check `edubob.db` file exists
- Verify write permissions
- Check backup files in `backups/` directory

### API Errors
- Check logs in console output
- Verify environment variables
- Test with Swagger UI at `/docs`

### watsonx.ai Issues
- Verify API key and project ID
- Check network connectivity
- System works with intelligent fallback if API unavailable

## Support

For detailed implementation information, see:
- [`../phases.md`](../phases.md) - Implementation plan
- [`../bob_sessions/`](../bob_sessions/) - Bob conversation exports
- [`../README.md`](../README.md) - Project overview