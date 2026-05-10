import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAssignments, getClassStats, getSubmissions } from '../api/services';

function TeacherDashboard() {
  const [assignments, setAssignments] = useState([]);
  const [classStats, setClassStats] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [aiAnalyzing, setAiAnalyzing] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setAiAnalyzing(true);
      
      // Fetch all data in parallel
      const [assignmentsData, statsData, submissionsData] = await Promise.all([
        getAssignments(),
        getClassStats(),
        getSubmissions()
      ]);
      
      setAssignments(assignmentsData);
      setClassStats(statsData);
      setSubmissions(submissionsData);
      setError(null);
      
      // Simulate AI analysis delay for demo effect
      setTimeout(() => setAiAnalyzing(false), 1000);
    } catch (err) {
      setError('Failed to fetch dashboard data');
      console.error(err);
      setAiAnalyzing(false);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('email');
    localStorage.removeItem('role');
    navigate('/login');
  };

  // Calculate statistics
  const totalSubmissions = submissions.length;
  const passedSubmissions = submissions.filter(s => s.status === 'passed').length;
  const successRate = totalSubmissions > 0 ? Math.round((passedSubmissions / totalSubmissions) * 100) : 0;

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Teacher Dashboard</h1>
            <p className="text-sm text-gray-600 mt-1">Powered by IBM Bob & watsonx.ai</p>
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
        {/* Action Buttons */}
        <div className="mb-8 flex gap-4">
          <button
            onClick={() => navigate('/generator')}
            className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors font-medium flex items-center"
          >
            <span className="mr-2">🤖</span>
            Assignment Generator
          </button>
          <button
            onClick={() => navigate('/analyzer')}
            className="px-6 py-3 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors font-medium flex items-center"
          >
            <span className="mr-2">📊</span>
            Codebase Analyzer
          </button>
        </div>

        {loading && (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="text-gray-600 mt-4">Loading dashboard...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {!loading && !error && (
          <div className="space-y-8">
            {/* Statistics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Total Assignments</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{assignments.length}</p>
                  </div>
                  <div className="text-4xl">📚</div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Total Submissions</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{totalSubmissions}</p>
                  </div>
                  <div className="text-4xl">📝</div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Success Rate</p>
                    <p className="text-3xl font-bold text-green-600 mt-2">{successRate}%</p>
                  </div>
                  <div className="text-4xl">✅</div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">AI Reviews</p>
                    <p className="text-3xl font-bold text-blue-600 mt-2">{submissions.filter(s => s.review_feedback).length}</p>
                  </div>
                  <div className="text-4xl">🤖</div>
                </div>
              </div>
            </div>

            {/* AI Insights Panel - Powered by watsonx.ai */}
            {classStats && (
              <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg shadow-lg p-6 border-2 border-blue-200">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                    <span className="mr-2">🧠</span>
                    AI-Powered Class Insights
                  </h2>
                  <div className="flex items-center gap-2">
                    {aiAnalyzing && (
                      <span className="text-sm text-blue-600 animate-pulse">Analyzing...</span>
                    )}
                    <span className="text-xs bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-3 py-1 rounded-full font-medium">
                      Powered by watsonx.ai granite-3-8b-instruct
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Common Errors */}
                  <div className="bg-white rounded-lg p-5 shadow-sm">
                    <h3 className="font-semibold text-lg mb-3 flex items-center text-red-700">
                      <span className="mr-2">⚠️</span>
                      Common Errors Detected
                    </h3>
                    {classStats.common_errors && classStats.common_errors.length > 0 ? (
                      <ul className="space-y-2">
                        {classStats.common_errors.map((error, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-red-500 mr-2 mt-1">•</span>
                            <span className="text-gray-700 text-sm">{error}</span>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-gray-500 text-sm italic">No error patterns detected yet</p>
                    )}
                  </div>

                  {/* Struggling Concepts */}
                  <div className="bg-white rounded-lg p-5 shadow-sm">
                    <h3 className="font-semibold text-lg mb-3 flex items-center text-orange-700">
                      <span className="mr-2">📖</span>
                      Concepts Students Struggle With
                    </h3>
                    {classStats.struggling_concepts && classStats.struggling_concepts.length > 0 ? (
                      <ul className="space-y-2">
                        {classStats.struggling_concepts.map((concept, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-orange-500 mr-2 mt-1">•</span>
                            <span className="text-gray-700 text-sm">{concept}</span>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-gray-500 text-sm italic">No struggling concepts identified yet</p>
                    )}
                  </div>
                </div>

                {/* AI Reasoning Section */}
                {classStats.ai_reasoning && (
                  <div className="mt-4 bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-300 rounded-lg p-4">
                    <div className="flex items-start">
                      <span className="text-2xl mr-3">🧠</span>
                      <div className="flex-1">
                        <h4 className="font-semibold text-blue-900 mb-2">AI Analysis Reasoning</h4>
                        <p className="text-sm text-blue-800 mb-3">{classStats.ai_reasoning}</p>
                        {classStats.analysis_method && (
                          <div className="flex items-center text-xs text-blue-700">
                            <span className="font-medium mr-2">Analysis Method:</span>
                            <span className="bg-blue-200 px-2 py-1 rounded">{classStats.analysis_method}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}

                {!classStats.ai_reasoning && (
                  <div className="mt-4 bg-blue-100 border border-blue-300 rounded-lg p-4">
                    <p className="text-sm text-blue-900">
                      <strong>💡 AI Recommendation:</strong> These insights are generated by analyzing student submission patterns.
                      Focus on addressing the most common errors in your next lesson.
                    </p>
                  </div>
                )}
              </div>
            )}

            {/* Recent Submissions */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
                <span className="mr-2">📊</span>
                Recent Submissions
              </h2>
              {submissions.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Student ID
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Assignment ID
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Status
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Tests
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          AI Review
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Date
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {submissions.slice(0, 10).map((submission) => (
                        <tr key={submission.id} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {submission.student_id}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {submission.assignment_id}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                              submission.status === 'passed' 
                                ? 'bg-green-100 text-green-800' 
                                : submission.status === 'failed'
                                ? 'bg-red-100 text-red-800'
                                : 'bg-yellow-100 text-yellow-800'
                            }`}>
                              {submission.status}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {submission.passed_tests}/{submission.total_tests}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm">
                            {submission.review_feedback ? (
                              <span className="text-blue-600 flex items-center">
                                <span className="mr-1">🤖</span>
                                Reviewed
                              </span>
                            ) : (
                              <span className="text-gray-400">-</span>
                            )}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {new Date(submission.timestamp).toLocaleDateString()}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p className="text-gray-500 text-center py-8">No submissions yet</p>
              )}
            </div>

            {/* Assignments Section */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
                <span className="mr-2">📚</span>
                Assignments
              </h2>
              
              {assignments.length === 0 && (
                <div className="text-center py-8">
                  <p className="text-gray-600">No assignments found. Create one using the Assignment Generator.</p>
                </div>
              )}

              {assignments.length > 0 && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {assignments.map((assignment) => (
                    <div
                      key={assignment.id}
                      className="bg-gray-50 rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow border border-gray-200"
                    >
                      <h3 className="text-xl font-semibold text-gray-900 mb-2">
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
                      <p className="text-gray-600 text-sm line-clamp-3 mb-3">
                        {assignment.description}
                      </p>
                      <div className="text-xs text-gray-500">
                        Created: {new Date(assignment.created_at).toLocaleDateString()}
                      </div>
                    </div>
                  ))}
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
              Powered by <strong className="ml-1 text-blue-600">IBM Bob</strong>
            </span>
            <span className="text-gray-400">|</span>
            <span className="flex items-center">
              <span className="mr-2">🧠</span>
              AI Insights by <strong className="ml-1 text-indigo-600">watsonx.ai</strong>
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default TeacherDashboard;

// Made with Bob
