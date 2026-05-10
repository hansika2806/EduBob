import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { generateAssignment } from '../api/services';

function AssignmentGenerator() {
  const [topic, setTopic] = useState('');
  const [difficulty, setDifficulty] = useState('beginner');
  const [bobOutput, setBobOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(null);
  const [error, setError] = useState(null);
  const [generatingAI, setGeneratingAI] = useState(false);
  const navigate = useNavigate();

  // Suggested topics for quick start
  const suggestedTopics = [
    'Python Functions',
    'Data Structures - Lists',
    'Loops and Iterations',
    'Object-Oriented Programming',
    'File Handling',
    'Error Handling'
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      setGeneratingAI(true);
      setError(null);
      setSuccess(null);

      // Simulate AI generation delay for demo effect
      await new Promise(resolve => setTimeout(resolve, 1500));

      const data = {
        topic,
        difficulty,
        bob_output: bobOutput
      };

      const result = await generateAssignment(data);
      setSuccess(`✅ Assignment created successfully! ID: ${result.id}`);
      setGeneratingAI(false);
      
      // Clear form
      setTopic('');
      setDifficulty('beginner');
      setBobOutput('');

      // Redirect to teacher dashboard after 2 seconds
      setTimeout(() => {
        navigate('/teacher');
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate assignment');
      setGeneratingAI(false);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleTopicSuggestion = (suggestedTopic) => {
    setTopic(suggestedTopic);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 flex items-center">
              <span className="mr-2">🤖</span>
              AI Assignment Generator
            </h1>
            <p className="text-sm text-gray-600 mt-1">Powered by IBM Bob Plan Mode</p>
          </div>
          <button
            onClick={() => navigate('/teacher')}
            className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors"
          >
            Back to Dashboard
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* AI Generation Status */}
        {generatingAI && (
          <div className="mb-6 bg-blue-50 border-2 border-blue-200 rounded-lg p-6 animate-pulse">
            <div className="flex items-center justify-center space-x-3">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <div>
                <p className="text-blue-900 font-semibold">IBM Bob is generating your assignment...</p>
                <p className="text-blue-700 text-sm">Analyzing requirements and creating test cases</p>
              </div>
            </div>
          </div>
        )}

        <div className="bg-white rounded-lg shadow-md p-8">
          {/* Info Banner */}
          <div className="mb-6 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-start">
              <span className="text-2xl mr-3">💡</span>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">How it works</h3>
                <p className="text-sm text-gray-700">
                  Use IBM Bob in Plan mode to generate assignment specifications, then paste the output here. 
                  Bob will automatically create structured assignments with test cases and requirements.
                </p>
              </div>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Topic Input with Suggestions */}
            <div>
              <label htmlFor="topic" className="block text-sm font-medium text-gray-700 mb-2">
                Topic <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                id="topic"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., Python Functions, Data Structures, etc."
              />
              
              {/* Quick Topic Suggestions */}
              <div className="mt-3">
                <p className="text-xs text-gray-600 mb-2">Quick suggestions:</p>
                <div className="flex flex-wrap gap-2">
                  {suggestedTopics.map((suggestedTopic, index) => (
                    <button
                      key={index}
                      type="button"
                      onClick={() => handleTopicSuggestion(suggestedTopic)}
                      className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs hover:bg-blue-200 transition-colors"
                    >
                      {suggestedTopic}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Difficulty Dropdown */}
            <div>
              <label htmlFor="difficulty" className="block text-sm font-medium text-gray-700 mb-2">
                Difficulty Level <span className="text-red-500">*</span>
              </label>
              <select
                id="difficulty"
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="beginner">🟢 Beginner - Basic concepts</option>
                <option value="intermediate">🟡 Intermediate - Applied knowledge</option>
                <option value="advanced">🔴 Advanced - Complex problems</option>
              </select>
            </div>

            {/* Bob Output Textarea */}
            <div>
              <label htmlFor="bobOutput" className="block text-sm font-medium text-gray-700 mb-2 flex items-center justify-between">
                <span>
                  IBM Bob Output <span className="text-red-500">*</span>
                </span>
                <span className="text-xs bg-blue-600 text-white px-2 py-1 rounded-full">
                  Powered by IBM Bob
                </span>
              </label>
              <textarea
                id="bobOutput"
                value={bobOutput}
                onChange={(e) => setBobOutput(e.target.value)}
                required
                rows={12}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                placeholder='Paste Bob IDE output here (JSON format expected)...

Example:
{
  "title": "Python Functions Basics",
  "description": "Learn to create and use functions...",
  "test_cases": [...],
  "starter_code": "def example():\n    pass"
}'
              />
              <p className="mt-2 text-xs text-gray-500">
                💡 Tip: Use Bob Plan mode with a prompt like "Create a {difficulty} Python assignment about {topic}"
              </p>
            </div>

            {/* Success Message */}
            {success && (
              <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded flex items-center">
                <span className="mr-2">✅</span>
                <div>
                  <p className="font-semibold">{success}</p>
                  <p className="text-sm">Redirecting to dashboard...</p>
                </div>
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded flex items-center">
                <span className="mr-2">❌</span>
                <p>{error}</p>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-3 px-4 rounded-md hover:from-blue-700 hover:to-indigo-700 transition-all font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Generating with AI...
                </>
              ) : (
                <>
                  <span className="mr-2">🤖</span>
                  Generate Assignment with IBM Bob
                </>
              )}
            </button>
          </form>

          {/* Stats Footer */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <p className="text-2xl font-bold text-blue-600">AI</p>
                <p className="text-xs text-gray-600">Powered</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-green-600">Auto</p>
                <p className="text-xs text-gray-600">Test Cases</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-purple-600">Smart</p>
                <p className="text-xs text-gray-600">Validation</p>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="flex items-center justify-center text-sm text-gray-600">
            <span className="flex items-center">
              <span className="mr-2">🤖</span>
              Assignment Generation powered by <strong className="ml-1 text-blue-600">IBM Bob Plan Mode</strong>
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default AssignmentGenerator;

// Made with Bob
