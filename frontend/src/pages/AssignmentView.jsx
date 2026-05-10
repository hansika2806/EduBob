import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getAssignments, submitAssignment } from '../api/services';

function AssignmentView() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [assignment, setAssignment] = useState(null);
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAssignment();
  }, [id]);

  const fetchAssignment = async () => {
    try {
      setLoading(true);
      const data = await getAssignments();
      const foundAssignment = data.find(a => a.id === parseInt(id));
      
      if (foundAssignment) {
        setAssignment(foundAssignment);
      } else {
        setError('Assignment not found');
      }
    } catch (err) {
      setError('Failed to fetch assignment');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setSubmitting(true);
      setError(null);
      setResult(null);

      const data = {
        assignment_id: parseInt(id),
        student_id: 1, // Temporary student ID
        code: code
      };

      const response = await submitAssignment(data);
      setResult(response);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit assignment');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <p className="text-gray-600">Loading assignment...</p>
      </div>
    );
  }

  if (error && !assignment) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">{assignment?.title}</h1>
          <button
            onClick={() => navigate('/student')}
            className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors"
          >
            Back to Dashboard
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Assignment Details */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Assignment Details</h2>
            
            <div className="mb-4">
              <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${
                assignment?.difficulty === 'beginner' ? 'bg-green-100 text-green-800' :
                assignment?.difficulty === 'intermediate' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {assignment?.difficulty}
              </span>
            </div>

            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Description</h3>
              <p className="text-gray-700 whitespace-pre-wrap">{assignment?.description}</p>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Requirements</h3>
              <ul className="list-disc list-inside space-y-1 text-gray-700">
                {assignment?.requirements?.map((req, index) => (
                  <li key={index}>{req}</li>
                ))}
              </ul>
            </div>
          </div>

          {/* Code Editor and Submission */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Your Solution</h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="code" className="block text-sm font-medium text-gray-700 mb-2">
                  Python Code
                </label>
                <textarea
                  id="code"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  required
                  rows={20}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                  placeholder="Write your Python code here..."
                />
              </div>

              {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={submitting}
                className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 transition-colors font-medium disabled:bg-blue-400 disabled:cursor-not-allowed"
              >
                {submitting ? 'Submitting...' : 'Submit Assignment'}
              </button>
            </form>

            {/* Results */}
            {result && (
              <div className="mt-6 space-y-4">
                {/* Status Badge */}
                <div className={`p-4 rounded-md ${
                  result.status === 'passed' ? 'bg-green-100 border border-green-400' : 'bg-red-100 border border-red-400'
                }`}>
                  <h3 className="font-semibold mb-2">
                    {result.status === 'passed' ? '✓ All Tests Passed!' : '✗ Tests Failed'}
                  </h3>
                  <p className="text-sm">
                    {result.passed_tests} / {result.total_tests} tests passed
                  </p>
                </div>

                {/* Test Results */}
                {result.test_results && result.test_results.length > 0 && (
                  <div className="bg-gray-50 p-4 rounded-md border border-gray-200">
                    <h3 className="font-semibold mb-3 flex items-center">
                      <span className="mr-2">📋</span>
                      Test Results
                    </h3>
                    <ul className="space-y-2">
                      {result.test_results.map((test, index) => (
                        <li key={index} className="flex items-start">
                          <span className={`mr-2 ${test.passed ? 'text-green-600' : 'text-red-600'}`}>
                            {test.passed ? '✓' : '✗'}
                          </span>
                          <div className="flex-1">
                            <p className="font-medium">{test.name || `Test ${index + 1}`}</p>
                            {!test.passed && test.error && (
                              <p className="text-sm text-red-600 mt-1 font-mono bg-red-50 p-2 rounded">{test.error}</p>
                            )}
                          </div>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* AI Review Feedback - Powered by IBM Bob */}
                {result.review_feedback && (
                  <div className="bg-blue-50 p-4 rounded-md border-2 border-blue-200">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="font-semibold flex items-center">
                        <span className="mr-2">🤖</span>
                        AI Code Review
                      </h3>
                      <span className="text-xs bg-blue-600 text-white px-2 py-1 rounded-full">
                        Powered by IBM Bob
                      </span>
                    </div>
                    
                    {/* Summary Feedback */}
                    {result.review_feedback.summary_feedback && (
                      <div className="mb-4">
                        <h4 className="font-medium text-blue-900 mb-2">Summary</h4>
                        <p className="text-gray-700 bg-white p-3 rounded border border-blue-100">
                          {result.review_feedback.summary_feedback}
                        </p>
                      </div>
                    )}
                    
                    {/* Mistakes Found */}
                    {result.review_feedback.mistakes && result.review_feedback.mistakes.length > 0 && (
                      <div className="mb-4">
                        <h4 className="font-medium text-red-700 mb-2 flex items-center">
                          <span className="mr-1">⚠️</span>
                          Issues Found ({result.review_feedback.mistakes.length})
                        </h4>
                        <ul className="space-y-2">
                          {result.review_feedback.mistakes.map((mistake, index) => (
                            <li key={index} className="bg-red-50 p-3 rounded border border-red-200 text-sm">
                              <span className="text-red-600 font-medium">•</span> {mistake}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    
                    {/* Improvement Suggestions */}
                    {result.review_feedback.improvement_suggestions && result.review_feedback.improvement_suggestions.length > 0 && (
                      <div>
                        <h4 className="font-medium text-green-700 mb-2 flex items-center">
                          <span className="mr-1">💡</span>
                          Suggestions for Improvement
                        </h4>
                        <ul className="space-y-2">
                          {result.review_feedback.improvement_suggestions.map((suggestion, index) => (
                            <li key={index} className="bg-green-50 p-3 rounded border border-green-200 text-sm">
                              <span className="text-green-600 font-medium">•</span> {suggestion}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default AssignmentView;

// Made with Bob
