// src/pages/ChatPage.jsx
import { useState, useEffect } from 'react';
import ChatInterface from '../components/features/ChatInterface';
import useStore from '../store/useStore';

const API_BASE_URL = 'http://127.0.0.1:8000';

const ChatPage = () => {
  const [isLoading, setIsLoading] = useState(false);
  // isPdfReady prop is assumed true for now, or handled by routing/global state
  // const { currentConversation, setCurrentConversation, addMessage } = useStore();
  const store = useStore(); // Get the whole store instance

  useEffect(() => {
    // Create a new conversation if none exists or if current one is null
    if (!store.currentConversation) {
      const newConversation = {
        id: Date.now().toString(), // Ensure ID is string for consistency
        title: 'New Conversation',
        messages: [],
        lastMessage: '',
        timestamp: new Date().toISOString()
      };
      store.setCurrentConversation(newConversation);
    }
  }, [store.currentConversation, store.setCurrentConversation]);

  const handleSendMessage = async (messageContent) => {
    if (!messageContent.trim()) {
      alert('Please enter a question.');
      return;
    }

    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: messageContent,
      timestamp: new Date().toISOString()
    };
    store.addMessage(userMessage);

    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: messageContent }),
      });

      const result = await response.json();

      if (response.ok) {
        const assistantMessage = {
          id: (Date.now() + 1).toString(), // Ensure unique ID and string format
          role: 'assistant',
          content: result.answer,
          timestamp: new Date().toISOString(),
          // sources: result.sources, // If API provides sources in the future
        };
        store.addMessage(assistantMessage);
      } else {
        // Display error to the user, e.g., by adding an error message to the chat
        const errorMessage = {
          id: (Date.now() + 1).toString(),
          role: 'system', // Or 'error' if you have specific styling
          content: `Error: ${result.detail || 'Failed to get answer.'} (Status: ${response.status})`,
          timestamp: new Date().toISOString(),
        };
        store.addMessage(errorMessage);
        console.error('API Error:', result.detail || response.statusText);
        // alert(`Error: ${result.detail || 'Failed to get answer.'}`);
      }
    } catch (error) {
      console.error('Network error:', error);
      const networkErrorMessage = {
        id: (Date.now() + 1).toString(),
        role: 'system',
        content: `Network Error: ${error.message || 'Could not connect to server.'}`,
        timestamp: new Date().toISOString(),
      };
      store.addMessage(networkErrorMessage);
      // alert(`Network Error: ${error.message || 'Could not connect to server.'}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 min-h-0">
        {store.currentConversation && (
          <ChatInterface
            messages={store.currentConversation.messages}
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
            // Pass a prop like isPdfReady if needed for UI changes
          />
        )}
      </div>
      {/* Footer nằm ngoài ChatInterface, dính đáy page */}
      <footer className="border-t border-gray-200 dark:border-gray-700 text-center py-2 text-sm text-gray-500 dark:text-gray-400 mt-auto">
        © RAGvLangChain_demo v1
      </footer>
    </div>
  );
};

export default ChatPage;