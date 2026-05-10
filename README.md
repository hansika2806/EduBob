# EduBob

AI-powered educational platform using IBM Bob for assignment generation, code review, and codebase analysis.

## Overview

EduBob is a comprehensive educational platform that leverages IBM Bob's AI capabilities to streamline the teaching and learning process. It enables teachers to generate assignments, review student code, and analyze codebases, while providing students with instant feedback and personalized learning insights.

## Problem Statement

- **Teachers**: Spend hours creating assignments and reviewing student code manually
- **Students**: Receive feedback too late to effectively learn from mistakes
- **Developers**: Struggle to understand complex codebases quickly

## Solution

EduBob integrates IBM Bob's AI capabilities to:
- **Generate assignments** from topics with automatic test case creation
- **Review student code** against specifications with detailed feedback
- **Analyze codebases** to provide architecture summaries and insights
- **Track mistake patterns** using watsonx.ai for personalized learning recommendations
- **Provide dashboards** with AI-powered class-wide analytics

## Features

### Core Features
- ✅ **Assignment Generator** - Create assignments from topics with AI-generated test cases
- ✅ **Code Validation Engine** - Automated testing with safe code execution
- ✅ **Code Review System** - AI-powered spec-based code review
- ✅ **Codebase Analyzer** - Analyze repository structure and architecture
- ✅ **Mistake Pattern Memory** - Track and analyze common student errors with watsonx.ai
- ✅ **Teacher Dashboard** - Class-wide statistics and AI insights
- ✅ **Student Dashboard** - Personal progress tracking and recommendations

### Technical Features
- Safe code execution with timeout protection
- Intelligent pattern analysis with watsonx.ai fallback
- Real-time feedback and validation
- Comprehensive error tracking
- Automated database backups
- Security middleware and rate limiting

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLite** - Lightweight database with SQLAlchemy ORM
- **IBM Bob** - AI-powered code generation and analysis
- **watsonx.ai** - Pattern analysis with granite-3-8b-instruct model
- **RestrictedPython** - Safe code execution sandbox

### Frontend
- **React 18** - Modern UI library
- **Vite** - Fast build tool and dev server
- **React Router v6** - Client-side routing
- **Axios** - HTTP client
- **Tailwind CSS** - Utility-first styling

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- IBM Bob CLI installed

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Backend runs on http://localhost:8000

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on http://localhost:5173

### Environment Configuration

Create a `.env` file in the backend directory:

```env
DATABASE_URL=sqlite:///./edubob.db
WATSONX_API_KEY=your_api_key_here  # Optional
WATSONX_PROJECT_ID=your_project_id  # Optional
```

## Project Structure

```
EduBob/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Database models
│   ├── schemas.py              # Pydantic schemas
│   ├── database.py             # Database configuration
│   ├── config.py               # Environment configuration
│   ├── services/               # Business logic
│   │   ├── bob_client.py       # Bob integration
│   │   ├── validator.py        # Code validation
│   │   ├── review_service.py   # Code review
│   │   ├── codebase_service.py # Codebase analysis
│   │   └── watsonx_client.py   # watsonx.ai integration
│   ├── middleware/             # Security & rate limiting
│   └── utils/                  # Logging, backup, monitoring
├── frontend/
│   ├── src/
│   │   ├── pages/              # React pages
│   │   ├── api/                # API services
│   │   └── App.jsx             # Main app component
│   └── public/                 # Static assets
└── bob_sessions/               # Bob conversation exports

```

## Implementation Phases

### ✅ Phase 1: Foundation (Completed)
- FastAPI backend with SQLite database
- Core models (Student, Assignment, Submission, Mistake)
- Basic CRUD operations
- Environment configuration

### ✅ Phase 2: Assignment Generation (Completed)
- Bob integration for assignment generation
- Code validation engine with test cases
- Safe code execution with RestrictedPython
- Assignment and submission management

### ✅ Phase 3: Code Review & Analysis (Completed)
- Code review system with spec-based analysis
- Codebase analyzer for repository understanding
- Bob Ask mode integration
- Review feedback storage

### ✅ Phase 4: Dashboard & Analytics (Completed)
- watsonx.ai integration for pattern analysis
- Mistake pattern tracking and recommendations
- Teacher dashboard with class statistics
- Student dashboard with progress tracking
- AI-powered insights and visualizations

## API Documentation

Interactive API documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Health & Status
- `GET /health` - Server health check

#### Students
- `GET /students` - List all students
- `POST /students` - Create new student
- `GET /students/{id}` - Get student details

#### Assignments
- `GET /assignments` - List all assignments
- `POST /api/assignments/generate` - Generate assignment with Bob
- `GET /assignments/{id}` - Get assignment details

#### Submissions
- `GET /submissions` - List submissions
- `POST /submissions` - Submit student code
- `GET /submissions/{id}` - Get submission details

#### Code Review
- `POST /api/review/spec-check` - Review code against specification

#### Codebase Analysis
- `POST /api/codebase/analyze` - Analyze repository structure

#### Dashboard
- `GET /api/dashboard/class-stats` - Class-wide statistics
- `GET /api/dashboard/assignment-stats/{id}` - Assignment statistics
- `GET /api/dashboard/student-progress/{id}` - Student progress

## Testing

### Backend Tests
```bash
cd backend
python test_phase2.py  # Test assignment generation
python test_phase3.py  # Test code review & analysis
python test_api.py     # Test API endpoints
```

### Frontend
Access the application at http://localhost:5173
- Login as teacher or student
- Test assignment creation and submission flow
- Verify dashboard displays correctly

## Security Features

- Rate limiting on API endpoints
- Security headers middleware
- Safe code execution sandbox
- Input validation and sanitization
- Sensitive data filtering in logs
- Automated database backups

## Bob Integration

EduBob uses IBM Bob in **manual mode**:
- Bob IDE output is obtained through Ask/Plan mode sessions
- Output is pasted into API requests as `bob_output` parameter
- No subprocess calls or CLI automation
- All Bob sessions are exported and stored in `bob_sessions/`

## watsonx.ai Integration

- Uses granite-3-8b-instruct model for pattern analysis
- Intelligent fallback when API is not configured
- Analyzes student errors to identify common patterns
- Provides actionable recommendations for improvement

## Database

- **SQLite** for development and small deployments
- Automated backups on startup
- Backup files stored in `backend/backups/`
- Migration path to PostgreSQL for production scale

## Current Status

**All Phases Complete** ✅

The EduBob platform is fully functional with:
- ✅ Backend API with all endpoints operational
- ✅ Frontend application with complete user flows
- ✅ Assignment generation and validation
- ✅ Code review and codebase analysis
- ✅ Dashboard with AI-powered insights
- ✅ Mistake pattern tracking with watsonx.ai
- ✅ Comprehensive documentation

## Future Enhancements

- Docker containerization for easy deployment
- PostgreSQL migration for production scale
- Enhanced security with JWT authentication
- Real-time collaboration features
- Mobile application
- Integration with popular LMS platforms

## Documentation

- [`backend/README.md`](backend/README.md) - Backend documentation
- [`frontend/README.md`](frontend/README.md) - Frontend documentation
- [`bob_sessions/README.md`](bob_sessions/README.md) - Bob session exports
- [`phases.md`](phases.md) - Detailed implementation plan
- [`BOB_USAGE.md`](BOB_USAGE.md) - Bob usage guidelines

## Contributing

This project was developed as part of an AI-assisted development workflow using IBM Bob. All Bob conversation sessions are exported and stored in the `bob_sessions/` directory for reference.

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions, please refer to the documentation in the respective README files for each component.
