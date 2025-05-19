// src/pages/HistoryPage.jsx
import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { format } from 'date-fns';
import { Search, Trash2, MessageSquare, FileText, AlertCircle } from 'lucide-react';
import Card from '../components/common/Card';
import Input from '../components/common/Input';
import Button from '../components/common/Button';
import useStore from '../store/useStore';
import { useNavigate } from 'react-router-dom';

const HistoryPage = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [deleteInProgress, setDeleteInProgress] = useState(null);
  const [deleteError, setDeleteError] = useState(null);
  const { 
    conversations, 
    fetchConversations, 
    setCurrentConversation, 
    deleteConversation,
    isLoading,
    error
  } = useStore();
  const [filteredHistory, setFilteredHistory] = useState([]);
  
  // Fetch conversations when the component mounts
  useEffect(() => {
    fetchConversations();
  }, [fetchConversations]);
  
  useEffect(() => {
    // Filter conversations based on search term
    if (searchTerm.trim() === '') {
      setFilteredHistory(conversations);
    } else {
      const filtered = conversations.filter(conv => 
        conv.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        conv.lastMessage.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredHistory(filtered);
    }
  }, [searchTerm, conversations]);
  
  const handleConversationClick = (conversation) => {
    setCurrentConversation(conversation);
    navigate('/chat');
  };
  
  const handleDeleteConversation = async (e, id) => {
    e.stopPropagation();
    if (window.confirm(t('history.confirmDelete') || 'Are you sure you want to delete this conversation?')) {
      try {
        setDeleteInProgress(id);
        setDeleteError(null);
        await deleteConversation(id);
        // Show success feedback (handled by removing from list)
      } catch (err) {
        console.error('Failed to delete conversation:', err);
        setDeleteError('Failed to delete. Please try again.');
      } finally {
        setDeleteInProgress(null);
      }
    }
  };
  
  const openPdfFile = (e, pdfPath) => {
    e.stopPropagation();
    if (pdfPath) {
      // Extract file ID from the path
      const fileId = pdfPath.split('/').pop().split('.')[0];
      // Open document in a new tab
      window.open(`http://localhost:8001/documents/${fileId}`, '_blank');
    }
  };
  
  const clearAllHistory = async () => {
    if (window.confirm('Are you sure you want to clear all chat history? This cannot be undone.')) {
      const deletePromises = conversations.map(conv => deleteConversation(conv.id));
      try {
        await Promise.all(deletePromises);
        // All conversations deleted
      } catch (err) {
        console.error('Failed to clear all history:', err);
        setDeleteError('Failed to clear all history. Some conversations may remain.');
      }
    }
  };
  
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">{t('history.title')}</h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1">
            {t('history.description')}
          </p>
        </div>
        
        {conversations.length > 0 && (
          <Button 
            variant="destructive" 
            onClick={clearAllHistory}
            className="px-4 py-2"
          >
            Clear All History
          </Button>
        )}
      </div>
      
      {deleteError && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded flex items-center mb-4">
          <AlertCircle className="mr-2" size={18} />
          <span>{deleteError}</span>
          <button 
            onClick={() => setDeleteError(null)} 
            className="ml-auto text-red-700 hover:text-red-900"
          >
            &times;
          </button>
        </div>
      )}
      
      <Card>
        <div className="mb-4">
          <Input
            placeholder={t('history.searchPlaceholder')}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            icon={<Search size={18} />}
          />
        </div>
        
        {isLoading ? (
          <div className="py-6 text-center">
            <p className="text-gray-500">{t('common.loading')}</p>
          </div>
        ) : error ? (
          <div className="py-6 text-center">
            <p className="text-red-500">{error}</p>
          </div>
        ) : (
          <div className="space-y-2">
            {filteredHistory.length === 0 ? (
              <p className="text-center text-gray-500 py-4">{t('history.noResults')}</p>
            ) : (
              filteredHistory.map((conversation) => (
                <div 
                  key={conversation.id}
                  className="flex items-center justify-between p-3 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer"
                  onClick={() => handleConversationClick(conversation)}
                >
                  <div className="flex items-center">
                    <MessageSquare size={18} className="mr-3 text-gray-500" />
                    <div>
                      <h3 className="font-medium">{conversation.title}</h3>
                      <p className="text-sm text-gray-500">{conversation.lastMessage}</p>
                    </div>
                  </div>
                  <div className="flex items-center">
                    <span className="text-xs text-gray-500 mr-3">
                      {format(new Date(conversation.timestamp), 'MMM d, yyyy')}
                    </span>
                    
                    {conversation.pdf_file && (
                      <Button
                        variant="ghost"
                        size="sm"
                        icon={<FileText size={16} />}
                        className="mr-1"
                        onClick={(e) => openPdfFile(e, conversation.pdf_file)}
                        title="View PDF"
                      />
                    )}
                    
                    <Button
                      variant="destructive"
                      size="sm"
                      icon={<Trash2 size={16} />}
                      onClick={(e) => handleDeleteConversation(e, conversation.id)}
                      title="Delete conversation"
                      className="bg-red-600 hover:bg-red-700 text-white"
                    />
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </Card>
    </div>
  );
};

export default HistoryPage;