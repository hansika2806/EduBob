# EduBob Frontend

React frontend application for EduBob - an AI-powered educational platform for assignment generation, code review, and analytics.

## Tech Stack

- **React 18** - UI library with hooks
- **Vite** - Build tool and dev server
- **React Router v6** - Client-side routing
- **Axios** - HTTP client for API calls
- **Tailwind CSS** - Utility-first CSS framework

## Prerequisites

- Node.js 16+ and npm
- Backend server running on http://localhost:8000

## Installation

```bash
cd frontend
npm install
```

## Development

Start the development server:

```bash
npm run dev
```

The application will be available at http://localhost:5173

## Build for Production

```bash
npm run build
```

The production build will be in the `dist` directory.

## Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   ├── config.js          # Axios configuration
│   │   └── services.js        # API service functions
│   ├── pages/
│   │   ├── Login.jsx          # Login page
│   │   ├── TeacherDashboard.jsx    # Teacher dashboard with analytics
│   │   ├── StudentDashboard.jsx    # Student dashboard with progress
│   │   ├── AssignmentView.jsx      # Assignment view and submission
│   │   ├── AssignmentGenerator.jsx # Assignment creation
│   │   └── CodebaseAnalyzer.jsx    # Codebase analysis tool
│   ├── App.jsx                # Main app with routing
│   ├── main.jsx               # Entry point
│   └── index.css              # Global styles with Tailwind
├── public/                    # Static assets
├── index.html                 # HTML template
├── vite.config.js             # Vite configuration
├── tailwind.config.js         # Tailwind configuration
└── package.json               # Dependencies
```

## Features

### For Teachers

1. **Teacher Dashboard** (`/teacher`) ⭐
   - View all assignments with status
   - Class-wide statistics and analytics
   - AI-powered insights from watsonx.ai
   - Common error patterns across students
   - Struggling concepts identification
   - Quick access to Assignment Generator and Codebase Analyzer

2. **Assignment Generator** (`/generator`)
   - Create assignments from topics
   - Set difficulty levels (beginner/intermediate/advanced)
   - Paste Bob IDE output for context
   - Generate test cases automatically
   - Preview and edit before saving

3. **Codebase Analyzer** (`/analyzer`)
   - Analyze GitHub repositories
   - Get architecture summaries
   - Identify key files and tech stack
   - Understand project structure quickly

### For Students

1. **Student Dashboard** (`/student`) ⭐
   - View available assignments
   - See submission history and status
   - Track personal progress
   - View success rates
   - Get AI-powered recommendations
   - Identify areas for improvement

2. **Assignment View** (`/assignment/:id`)
   - View assignment details and requirements
   - Read starter code and hints
   - Write and submit Python code
   - Get instant test results
   - Receive AI-powered code review feedback
   - See detailed error messages
   - Track submission attempts

## Routes

- `/login` - Login page (email + role selection)
- `/teacher` - Teacher dashboard with analytics
- `/student` - Student dashboard with progress tracking
- `/assignment/:id` - Assignment view and submission
- `/generator` - Assignment generator
- `/analyzer` - Codebase analyzer

## API Integration

The frontend communicates with the backend API at `http://localhost:8000`:

### Core Endpoints
- `GET /assignments` - Fetch all assignments
- `POST /api/assignments/generate` - Generate new assignment
- `POST /submissions` - Submit assignment solution
- `POST /api/codebase/analyze` - Analyze codebase

### Dashboard Endpoints ⭐ NEW
- `GET /api/dashboard/class-stats` - Class-wide statistics
- `GET /api/dashboard/assignment-stats/{id}` - Assignment statistics
- `GET /api/dashboard/student-progress/{id}` - Student progress

## Pages Overview

### Login Page
- Simple email and role selection
- No password required (demo purposes)
- Stores credentials in localStorage
- Redirects to appropriate dashboard

### Teacher Dashboard
**Features:**
- Assignment list with creation dates
- Class statistics card showing:
  - Total submissions
  - Common errors across all students
  - Struggling concepts identified by AI
  - AI reasoning and analysis method
- Quick action buttons for:
  - Creating new assignments
  - Analyzing codebases
- Clean, professional UI with cards and sections

### Student Dashboard
**Features:**
- Available assignments list
- Personal statistics showing:
  - Total submissions
  - Success rate
  - Recent mistakes
  - AI-powered recommendations
- Assignment cards with:
  - Title and description
  - Difficulty level
  - Topic
  - Start button
- Progress tracking

### Assignment View
**Features:**
- Assignment details section:
  - Title and description
  - Difficulty and topic
  - Test cases preview
  - Starter code
  - Hints
- Code editor:
  - Syntax highlighting
  - Line numbers
  - Monospace font
- Submit button
- Results display:
  - Test results with pass/fail status
  - Expected vs actual output
  - Error messages
  - AI review feedback
  - Improvement suggestions

### Assignment Generator
**Features:**
- Topic input field
- Difficulty selector (beginner/intermediate/advanced)
- Bob output textarea
- Generate button
- Preview of generated assignment
- Save functionality

### Codebase Analyzer
**Features:**
- Repository URL input
- Bob output textarea
- Analyze button
- Results display:
  - Architecture summary
  - Key files with purposes
  - Tech stack identification
  - Detailed explanation

## Authentication

Simple localStorage-based authentication:
- Email and role stored in localStorage
- No backend authentication required (demo purposes)
- Logout clears localStorage
- Protected routes check for user data

## Styling

- Clean, minimal, professional UI
- Responsive design for all screen sizes
- Tailwind CSS utility classes
- Consistent color scheme:
  - Primary: Blue (#3B82F6)
  - Success: Green (#10B981)
  - Warning: Yellow (#F59E0B)
  - Error: Red (#EF4444)
- No animations (as per requirements)
- Card-based layouts
- Clear visual hierarchy

## State Management

- React hooks (useState, useEffect)
- No external state management library
- Local component state
- API calls with Axios
- Error handling with try-catch

## Error Handling

- API error messages displayed to users
- Loading states during API calls
- Fallback UI for errors
- Console logging for debugging

## Performance

- Vite for fast development and builds
- Code splitting with React Router
- Lazy loading (future enhancement)
- Optimized bundle size

## Development Notes

- Student ID is hardcoded to 1 for demo purposes
- No actual authentication backend implemented
- Focus on end-to-end demo flow
- Simple and working implementation without over-engineering

## Testing

### Manual Testing Checklist

**Login Flow:**
- [ ] Can login as teacher
- [ ] Can login as student
- [ ] Redirects to correct dashboard
- [ ] Logout works correctly

**Teacher Dashboard:**
- [ ] Displays all assignments
- [ ] Shows class statistics
- [ ] AI insights visible
- [ ] Navigation buttons work

**Student Dashboard:**
- [ ] Displays available assignments
- [ ] Shows personal statistics
- [ ] Recommendations visible
- [ ] Can navigate to assignments

**Assignment Flow:**
- [ ] Can view assignment details
- [ ] Can submit code
- [ ] Test results display correctly
- [ ] Review feedback shows up
- [ ] Multiple submissions work

**Assignment Generator:**
- [ ] Can input topic and difficulty
- [ ] Can paste Bob output
- [ ] Generate button works
- [ ] Preview displays correctly

**Codebase Analyzer:**
- [ ] Can input repository URL
- [ ] Can paste Bob output
- [ ] Analysis results display
- [ ] All sections visible

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Known Limitations

- No real authentication system
- Student ID hardcoded for demo
- No data persistence beyond backend
- No real-time updates
- No mobile optimization (works but not optimized)

## Future Enhancements

- Real authentication with JWT
- User profile management
- Real-time collaboration
- Mobile-responsive improvements
- Dark mode support
- Code editor with Monaco Editor
- Syntax highlighting improvements
- File upload for code submissions
- Assignment templates
- Bulk operations for teachers

## Troubleshooting

### Frontend Won't Start
- Check Node.js version (16+)
- Run `npm install` again
- Delete `node_modules` and reinstall
- Check port 5173 is available

### API Calls Failing
- Verify backend is running on port 8000
- Check CORS configuration
- Verify API endpoints in `src/api/config.js`
- Check browser console for errors

### Styling Issues
- Run `npm run build` to rebuild
- Clear browser cache
- Check Tailwind configuration
- Verify CSS imports

## Contributing

When making changes:
1. Follow existing code style
2. Test all user flows
3. Update documentation
4. Ensure responsive design
5. Check browser console for errors

## Support

For detailed implementation information, see:
- [`../backend/README.md`](../backend/README.md) - Backend API documentation
- [`../phases.md`](../phases.md) - Implementation plan
- [`../README.md`](../README.md) - Project overview
