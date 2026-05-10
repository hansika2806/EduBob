import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAssignments, getSubmissions } from '../api/services';

function StudentDashboard() {
  const [assignments, setAssignments] = useState([]);
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // Hardcoded student ID for demo (in production, get from auth context)
  const studentId = 1;

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [assignmentsData, submissionsData] = await Promise.all([
        getAssignments(),
        getSubmissions({ student_id: studentId })
      ]);
      setAssignments(assignmentsData);
      setSubmissions(submissionsData);
      setError(null);
    } catch (err) {
      setError('Failed to fetch dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('email');
    localStorage.removeItem('role');
    navigate('/login');
  };

  const handleAssignmentClick = (assignmentId) => {
    navigate(`/assignment/${assignmentId}`);
  };

  // Calculate student statistics
  const totalAttempts = submissions.length;
  const passedAttempts = submissions.filter(s => s.status === 'passed').length;
  const successRate = totalAttempts > 0 ? Math.round((passedAttempts / totalAttempts) * 100) : 0;
  const aiReviews = submissions.filter(s => s.review_feedback).length;

  // Get completed assignment IDs
  const completedAssignmentIds = new Set(
    submissions.filter(s => s.status === 'passed').map(s => s.assignment_id)
  );

  // Analyze mistake patterns from AI reviews
  const mistakePatterns = [];
  const improvementSuggestions = [];
  submissions.forEach(sub => {
    if (sub.review_feedback) {
      if (sub.review_feedback.mistakes) {
        mistakePatterns.push(...sub.review_feedback.mistakes);
      }
      if (sub.review_feedback.improvement_suggestions) {
        improvementSuggestions.push(...sub.review_feedback.improvement_suggestions);
      }
    }
  });

  // Get unique patterns (limit to 5)
  const uniqueMistakes = [...new Set(mistakePatterns)].slice(0, 5);
  const uniqueSuggestions = [...new Set(improvementSuggestions)].slice(0, 5);

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Student Dashboard</h1>
            <p className="text-sm text-gray-600 mt-1">Your personalized learning journey with AI</p>
          </div>
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {loading && (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="text-gray-600 mt-4">Loading your dashboard...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {!loading && !error && (
          <div className="space-y-8">
            {/* Progress Statistics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Assignments</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{assignments.length}</p>
                  </div>
                  <div className="text-4xl">📚</div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Completed</p>
                    <p className="text-3xl font-bold text-green-600 mt-2">{completedAssignmentIds.size}</p>
                  </div>
                  <div className="text-4xl">✅</div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Success Rate</p>
                    <p className="text-3xl font-bold text-blue-600 mt-2">{successRate}%</p>
                  </div>
                  <div className="text-4xl">📊</div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">AI Reviews</p>
                    <p className="text-3xl font-bold text-purple-600 mt-2">{aiReviews}</p>
                  </div>
                  <div className="text-4xl">🤖</div>
                </div>
              </div>
            </div>

            {/* AI Learning Insights */}
            {(uniqueMistakes.length > 0 || uniqueSuggestions.length > 0) && (
              <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg shadow-lg p-6 border-2 border-purple-200">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                    <span className="mr-2">🎯</span>
                    Your AI Learning Insights
                  </h2>
                  <span className="text-xs bg-gradient-to-r from-purple-600 to-pink-600 text-white px-3 py-1 rounded-full font-medium">
                    Powered by IBM Bob
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Common Mistakes */}
                  {uniqueMistakes.length > 0 && (
                    <div className="bg-white rounded-lg p-5 shadow-sm">
                      <h3 className="font-semibold text-lg mb-3 flex items-center text-red-700">
                        <span className="mr-2">⚠️</span>
                        Areas to Improve
                      </h3>
                      <ul className="space-y-2">
                        {uniqueMistakes.map((mistake, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-red-500 mr-2 mt-1">•</span>
                            <span className="text-gray-700 text-sm">{mistake}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Improvement Suggestions */}
                  {uniqueSuggestions.length > 0 && (
                    <div className="bg-white rounded-lg p-5 shadow-sm">
                      <h3 className="font-semibold text-lg mb-3 flex items-center text-green-700">
                        <span className="mr-2">💡</span>
                        AI Recommendations
                      </h3>
                      <ul className="space-y-2">
                        {uniqueSuggestions.map((suggestion, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-green-500 mr-2 mt-1">•</span>
                            <span className="text-gray-700 text-sm">{suggestion}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                <div className="mt-4 bg-purple-100 border border-purple-300 rounded-lg p-4">
                  <p className="text-sm text-purple-900">
                    <strong>💡 Keep Learning:</strong> These insights are generated by IBM Bob's AI analysis of your code submissions. 
                    Focus on these areas to improve your programming skills!
                  </p>
                </div>
              </div>
            )}

            {/* Recent Submissions */}
            {submissions.length > 0 && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
                  <span className="mr-2">📝</span>
                  Your Recent Submissions
                </h2>
                <div className="space-y-3">
                  {submissions.slice(0, 5).map((submission) => {
                    const assignment = assignments.find(a => a.id === submission.assignment_id);
                    return (
                      <div key={submission.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                        <div className="flex items-center justify-between">
                          <div className="flex-1">
                            <h3 className="font-semibold text-gray-900">
                              {assignment?.title || `Assignment ${submission.assignment_id}`}
                            </h3>
                            <div className="flex items-center gap-4 mt-2 text-sm text-gray-600">
                              <span className="flex items-center">
                                <span className="mr-1">📅</span>
                                {new Date(submission.timestamp).toLocaleDateString()}
                              </span>
                              <span className="flex items-center">
                                <span className="mr-1">✓</span>
                                {submission.passed_tests}/{submission.total_tests} tests
                              </span>
                              {submission.review_feedback && (
                                <span className="flex items-center text-blue-600">
                                  <span className="mr-1">🤖</span>
                                  AI Reviewed
                                </span>
                              )}
                            </div>
                          </div>
                          <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                            submission.status === 'passed' 
                              ? 'bg-green-100 text-green-800' 
                              : submission.status === 'failed'
                              ? 'bg-red-100 text-red-800'
                              : 'bg-yellow-100 text-yellow-800'
                          }`}>
                            {submission.status}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Available Assignments */}
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
                <span className="mr-2">📚</span>
                Available Assignments
              </h2>
              
              {assignments.length === 0 && (
                <div className="text-center py-8 bg-white rounded-lg shadow-md">
                  <p className="text-gray-600">No assignments available at the moment.</p>
                </div>
              )}

              {assignments.length > 0 && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {assignments.map((assignment) => {
                    const isCompleted = completedAssignmentIds.has(assignment.id);
                    return (
                      <div
                        key={assignment.id}
                        onClick={() => handleAssignmentClick(assignment.id)}
                        className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer relative"
                      >
                        {isCompleted && (
                          <div className="absolute top-4 right-4">
                            <span className="text-2xl">✅</span>
                          </div>
                        )}
                        <h3 className="text-xl font-semibold text-gray-900 mb-2 pr-8">
                          {assignment.title}
                        </h3>
                        <div className="mb-4">
                          <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${
                            assignment.difficulty === 'beginner' ? 'bg-green-100 text-green-800' :
                            assignment.difficulty === 'intermediate' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-red-100 text-red-800'
                          }`}>
                            {assignment.difficulty}
                          </span>
                        </div>
                        <p className="text-gray-600 text-sm line-clamp-3 mb-4">
                          {assignment.description}
                        </p>
                        <button className={`w-full py-2 px-4 rounded-md transition-colors font-medium ${
                          isCompleted 
                            ? 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                            : 'bg-blue-600 text-white hover:bg-blue-700'
                        }`}>
                          {isCompleted ? 'Review Assignment' : 'Start Assignment'}
                        </button>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="flex items-center justify-center space-x-6 text-sm text-gray-600">
            <span className="flex items-center">
              <span className="mr-2">🤖</span>
              AI-Powered Learning with <strong className="ml-1 text-blue-600">IBM Bob</strong>
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default StudentDashboard;

// Made with Bob
