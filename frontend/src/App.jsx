import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import TeacherDashboard from './pages/TeacherDashboard';
import StudentDashboard from './pages/StudentDashboard';
import AssignmentView from './pages/AssignmentView';
import AssignmentGenerator from './pages/AssignmentGenerator';
import CodebaseAnalyzer from './pages/CodebaseAnalyzer';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/teacher" element={<TeacherDashboard />} />
        <Route path="/student" element={<StudentDashboard />} />
        <Route path="/assignment/:id" element={<AssignmentView />} />
        <Route path="/generator" element={<AssignmentGenerator />} />
        <Route path="/analyzer" element={<CodebaseAnalyzer />} />
      </Routes>
    </Router>
  );
}

export default App;

// Made with Bob
