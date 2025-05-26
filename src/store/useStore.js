// src/store/useStore.js
import { create } from 'zustand';
import { 
  getConversations, 
  getConversation, 
  createConversation, 
  updateConversation, 
  deleteConversation,
  deleteDocument
} from '../api/apiClient';
import i18n from '../i18n';

// Helper to check if a conversation is empty/worth saving
const isConversationEmpty = (conversation) => {
  // Check if there are no messages or only empty messages
  return !conversation.messages || 
    conversation.messages.length === 0 || 
    conversation.messages.every(msg => !msg.content || msg.content.trim() === '');
};

const useStore = create((set, get) => ({
  // Dashboard stats
  stats: {
    documentCount: 0,
    queryCount: 0,
    avgResponseTime: 0,
  },
  
  // Documents
  documents: [],
  
  // Chat history
  conversations: [],
  currentConversation: null,
  
  // Loading states
  isLoading: false,
  error: null,
  
  // Language settings
  language: localStorage.getItem('i18nextLng') || 'en',
  
  // Actions
  setStats: (stats) => set({ stats }),
  setDocuments: (documents) => set({ documents }),
  fetchDocuments: async () => {
    set({ isLoading: true, error: null });
    try {
      // Giả sử backend có endpoint /documents trả về danh sách file
      const response = await fetch('http://localhost:8001/documents');
      const docs = await response.json();
      set({ documents: docs, isLoading: false });
    } catch {
      set({ error: 'Failed to fetch documents', isLoading: false });
    }
  },
  addDocument: (document) => set((state) => ({ 
    documents: [...state.documents, document],
    stats: { 
      ...state.stats, 
      documentCount: state.stats.documentCount + 1 
    }
  })),
  removeDocument: async (id) => {
    set({ isLoading: true, error: null });
    try {
      await deleteDocument(id);
      set((state) => ({ 
        documents: state.documents.filter(doc => doc.id !== id),
        stats: { 
          ...state.stats, 
          documentCount: state.stats.documentCount - 1 
        },
        isLoading: false
      }));
    } catch {
      set({ error: 'Failed to delete document', isLoading: false });
    }
  },
  
  // Fetch conversations from API
  fetchConversations: async () => {
    set({ isLoading: true, error: null });
    try {
      console.log('Store: Fetching conversations from API...');
      const conversations = await getConversations();
      console.log('Store: Received conversations:', conversations.length, 'items');
      set({ conversations, isLoading: false });
    } catch (error) {
      console.error('Store: Error fetching conversations:', error);
      let errorMessage = 'Failed to fetch conversations';
      
      if (error.code === 'ECONNREFUSED') {
        errorMessage = 'Cannot connect to backend server. Please ensure the backend is running on port 8001.';
      } else if (error.response?.status === 401) {
        errorMessage = 'Authentication required. Please log in again.';
        // Clear invalid token
        localStorage.removeItem('token');
        window.location.href = '/auth';
      } else if (error.response?.status === 403) {
        errorMessage = 'Access denied. You don\'t have permission to view these conversations.';
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      }
      
      set({ error: errorMessage, isLoading: false });
    }
  },
  
  // Set conversations
  setConversations: (conversations) => set({ conversations }),
  
  // Fetch and set current conversation
  fetchConversation: async (id) => {
    set({ isLoading: true, error: null });
    try {
      const conversation = await getConversation(id);
      set({ currentConversation: conversation, isLoading: false });
      return conversation;
    } catch (error) {
      console.error('Error fetching conversation:', error);
      set({ error: 'Failed to fetch conversation', isLoading: false });
      return null;
    }
  },
  
  // Set current conversation
  setCurrentConversation: (conversation) => {
    set({ currentConversation: conversation });
    
    // If this is a new conversation that hasn't been saved to the backend yet
    // we'll sync it with the backend using the update endpoint
    if (conversation && 
        !get().conversations.some(conv => conv.id === conversation.id) && 
        !isConversationEmpty(conversation)) {
      updateConversation(conversation.id, {
        title: conversation.title || `Conversation ${conversation.id}`,
        lastMessage: conversation.lastMessage || "",
        messages: conversation.messages || [],
        timestamp: conversation.timestamp || new Date().toISOString()
      }).catch(err => console.error('Error syncing new conversation with backend:', err));
    }
  },
  
  // Create new conversation
  createNewConversation: async (title, lastMessage, pdfFile = null) => {
    set({ isLoading: true, error: null });
    
    // Don't create conversation if title and lastMessage are empty and no PDF
    if (!pdfFile && (!title || title.trim() === '') && (!lastMessage || lastMessage.trim() === '')) {
      console.log('Skipping empty conversation creation');
      return null;
    }
    
    try {
      const newConversation = await createConversation(title, lastMessage, pdfFile);
      set((state) => ({
        conversations: [...state.conversations, newConversation],
        currentConversation: newConversation,
        isLoading: false
      }));
      return newConversation;
    } catch (error) {
      console.error('Error creating conversation:', error);
      set({ error: 'Failed to create conversation', isLoading: false });
      return null;
    }
  },
  
  // Add message to current conversation
  addMessage: async (message) => {
    if (!get().currentConversation) {
      console.log('Store: No current conversation, cannot add message');
      return;
    }
    
    // Skip empty messages
    if (!message.content || message.content.trim() === '') {
      console.log('Store: Skipping empty message');
      return;
    }
    
    console.log('Store: Adding message to conversation:', get().currentConversation.id);
    
    const updatedConversation = {
      ...get().currentConversation,
      messages: [...get().currentConversation.messages, message],
      lastMessage: message.content,
      timestamp: new Date().toISOString()
    };
    
    set((state) => {
      const updatedConversations = state.conversations.map(conv => 
        conv.id === updatedConversation.id ? updatedConversation : conv
      );
      
      if (!updatedConversations.some(conv => conv.id === updatedConversation.id)) {
        updatedConversations.push(updatedConversation);
      }
      
      return {
        currentConversation: updatedConversation,
        conversations: updatedConversations,
        stats: {
          ...state.stats,
          queryCount: message.role === 'user' ? state.stats.queryCount + 1 : state.stats.queryCount
        }
      };
    });
    
    // Don't update empty conversations in the API
    if (isConversationEmpty(updatedConversation)) {
      console.log('Skipping API update for empty conversation');
      return;
    }
    
    // Update conversation in the API
    try {
      await updateConversation(updatedConversation.id, {
        messages: updatedConversation.messages,
        lastMessage: updatedConversation.lastMessage,
        timestamp: updatedConversation.timestamp
      });
    } catch (error) {
      console.error('Error updating conversation with new message:', error);
    }
  },
  
  // Delete conversation
  deleteConversation: async (id) => {
    set({ isLoading: true, error: null });
    try {
      await deleteConversation(id);
      set((state) => ({ 
        conversations: state.conversations.filter(conv => conv.id !== id),
        currentConversation: state.currentConversation?.id === id ? null : state.currentConversation,
        isLoading: false
      }));
    } catch (error) {
      console.error('Error deleting conversation:', error);
      set({ error: 'Failed to delete conversation', isLoading: false });
    }
  },

  // Clear user-specific data (call when user logs out)
  clearUserData: () => {
    set({
      conversations: [],
      currentConversation: null,
      documents: [],
      stats: {
        documentCount: 0,
        queryCount: 0,
        avgResponseTime: 0,
      },
      error: null
    });
  },

  // Language actions
  setLanguage: (lang) => {
    i18n.changeLanguage(lang);
    localStorage.setItem('i18nextLng', lang);
    set({ language: lang });
  }
}));

export default useStore;