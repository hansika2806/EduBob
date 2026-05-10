import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { analyzeCodebase } from '../api/services';

function CodebaseAnalyzer() {
  const [repoUrl, setRepoUrl] = useState('');
  const [bobAnalysis, setBobAnalysis] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      setError(null);
      setResult(null);

      const data = {
        repo_url: repoUrl,
        bob_analysis: bobAnalysis
      };

      const response = await analyzeCodebase(data);
      setResult(response);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze codebase');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Codebase Analyzer</h1>
          <button
            onClick={() => navigate('/teacher')}
            className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors"
          >
            Back to Dashboard
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <div className="bg-white rounded-lg shadow-md p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Analyze Repository</h2>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Repository URL Input */}
              <div>
                <label htmlFor="repoUrl" className="block text-sm font-medium text-gray-700 mb-2">
                  Repository URL
                </label>
                <input
                  type="url"
                  id="repoUrl"
                  value={repoUrl}
                  onChange={(e) => setRepoUrl(e.target.value)}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="https://github.com/username/repo"
                />
              </div>

              {/* Bob Analysis Textarea */}
              <div>
                <label htmlFor="bobAnalysis" className="block text-sm font-medium text-gray-700 mb-2">
                  Bob Analysis Output
                </label>
                <textarea
                  id="bobAnalysis"
                  value={bobAnalysis}
                  onChange={(e) => setBobAnalysis(e.target.value)}
                  required
                  rows={16}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                  placeholder="Paste Bob analysis output here..."
                />
              </div>

              {/* Error Message */}
              {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                  {error}
                </div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-green-600 text-white py-3 px-4 rounded-md hover:bg-green-700 transition-colors font-medium disabled:bg-green-400 disabled:cursor-not-allowed"
              >
                {loading ? 'Analyzing...' : 'Analyze Codebase'}
              </button>
            </form>
          </div>

          {/* Results Display */}
          <div className="bg-white rounded-lg shadow-md p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Analysis Results</h2>
            
            {!result && !loading && (
              <div className="text-center py-12">
                <p className="text-gray-500">Submit a repository for analysis to see results here.</p>
              </div>
            )}

            {loading && (
              <div className="text-center py-12">
                <p className="text-gray-600">Analyzing codebase...</p>
              </div>
            )}

            {result && (
              <div className="space-y-6">
                {/* Architecture Summary */}
                {result.architecture_summary && (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Architecture Summary</h3>
                    <p className="text-gray-700 whitespace-pre-wrap bg-gray-50 p-4 rounded-md">
                      {result.architecture_summary}
                    </p>
                  </div>
                )}

                {/* Key Files */}
                {result.key_files && result.key_files.length > 0 && (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Key Files</h3>
                    <ul className="bg-gray-50 p-4 rounded-md space-y-2">
                      {result.key_files.map((file, index) => (
                        <li key={index} className="flex items-start">
                          <span className="text-blue-600 mr-2">📄</span>
                          <span className="text-gray-700 font-mono text-sm">{file}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Tech Stack */}
                {result.tech_stack && result.tech_stack.length > 0 && (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Tech Stack</h3>
                    <div className="flex flex-wrap gap-2">
                      {result.tech_stack.map((tech, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
                        >
                          {tech}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Explanation */}
                {result.explanation && (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Detailed Explanation</h3>
                    <p className="text-gray-700 whitespace-pre-wrap bg-gray-50 p-4 rounded-md">
                      {result.explanation}
                    </p>
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

export default CodebaseAnalyzer;

// Made with Bob
