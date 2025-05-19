import axios from 'axios';

const API_URL = 'http://localhost:8001';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Conversations API
export const getConversations = async () => {
  const response = await apiClient.get('/conversations');
  return response.data;
};

export const getConversation = async (id) => {
  const response = await apiClient.get(`/conversations/${id}`);
  return response.data;
};

export const createConversation = async (title, lastMessage, pdfFile = null) => {
  const formData = new FormData();
  formData.append('title', title);
  formData.append('last_message', lastMessage);
  
  if (pdfFile) {
    formData.append('pdf_file', pdfFile);
  }
  
  const response = await apiClient.post('/conversations', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const updateConversation = async (id, data) => {
  // Ensure the data is in the right format
  const payload = {
    ...data,
    // If messages are present, make sure they're properly formatted with string IDs
    messages: data.messages?.map(msg => ({
      id: String(msg.id), // Convert ID to string
      role: msg.role,
      content: msg.content,
      timestamp: msg.timestamp
    }))
  };
  
  const response = await apiClient.put(`/conversations/${id}`, payload);
  return response.data;
};

export const deleteConversation = async (id) => {
  const response = await apiClient.delete(`/conversations/${id}`);
  return response.data;
};

// Documents API
export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await apiClient.post('/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const getDocument = async (id) => {
  const response = await apiClient.get(`/documents/${id}`, {
    responseType: 'blob',
  });
  
  return response.data;
};

export const deleteDocument = async (id) => {
  const response = await apiClient.delete(`/documents/${id}`);
  return response.data;
};

export default apiClient; 