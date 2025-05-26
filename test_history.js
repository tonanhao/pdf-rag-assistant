// Test script to check chat history functionality
const API_URL = 'http://localhost:8001';

async function testConversationsAPI() {
  console.log('Testing conversations API...');
  
  try {
    const response = await fetch(`${API_URL}/conversations`);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const conversations = await response.json();
    console.log(`✅ Successfully fetched ${conversations.length} conversations`);
    
    if (conversations.length > 0) {
      console.log('📝 Sample conversation:');
      console.log(JSON.stringify(conversations[0], null, 2));
    } else {
      console.log('📭 No conversations found');
    }
    
    return conversations;
  } catch (error) {
    if (error.code === 'ECONNREFUSED') {
      console.error('❌ Backend server is not running on port 8001');
      console.log('💡 Start the backend with: cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8001');
    } else {
      console.error('❌ Error:', error.message);
    }
    return null;
  }
}

// Run the test
testConversationsAPI(); 