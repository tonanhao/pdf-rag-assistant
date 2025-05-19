// src/store/useStore.js
import { create } from 'zustand';
import { 
  getConversations, 
  getConversation, 
  createConversation, 
  updateConversation, 
  deleteConversation 
} from '../api/apiClient';

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
  
  // Actions
  setStats: (stats) => set({ stats }),
  setDocuments: (documents) => set({ documents }),
  addDocument: (document) => set((state) => ({ 
    documents: [...state.documents, document],
    stats: { 
      ...state.stats, 
      documentCount: state.stats.documentCount + 1 
    }
  })),
  removeDocument: (id) => set((state) => ({ 
    documents: state.documents.filter(doc => doc.id !== id),
    stats: { 
      ...state.stats, 
      documentCount: state.stats.documentCount - 1 
    }
  })),
  
  // Fetch conversations from API
  fetchConversations: async () => {
    set({ isLoading: true, error: null });
    try {
      const conversations = await getConversations();
      set({ conversations, isLoading: false });
    } catch (error) {
      console.error('Error fetching conversations:', error);
      set({ error: 'Failed to fetch conversations', isLoading: false });
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
    if (!get().currentConversation) return;
    
    // Skip empty messages
    if (!message.content || message.content.trim() === '') {
      console.log('Skipping empty message');
      return;
    }
    
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
  }
}));

export default useStore;