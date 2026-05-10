import api from './config';

// Assignment APIs
export const getAssignments = async () => {
  const response = await api.get('/assignments');
  return response.data;
};

export const generateAssignment = async (data) => {
  const response = await api.post('/api/assignments/generate', data);
  return response.data;
};

// Submission APIs
export const submitAssignment = async (data) => {
  const response = await api.post('/submissions', data);
  return response.data;
};

export const getSubmissions = async (params = {}) => {
  const response = await api.get('/submissions', { params });
  return response.data;
};

// Dashboard APIs
export const getClassStats = async () => {
  const response = await api.get('/api/dashboard/class-stats');
  return response.data;
};

// Codebase Analysis APIs
export const analyzeCodebase = async (data) => {
  const response = await api.post('/api/codebase/analyze', data);
  return response.data;
};

// Made with Bob
