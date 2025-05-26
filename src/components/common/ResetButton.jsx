import React from 'react';

const ResetButton = () => {
  const handleReset = () => {
    console.log('Resetting application state...');
    localStorage.removeItem('token');
    window.location.href = '/auth';
  };

  return (
    <button
      onClick={handleReset}
      style={{
        position: 'fixed',
        bottom: '20px',
        left: '20px',
        zIndex: 9999,
        padding: '8px 12px',
        backgroundColor: '#f44336',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '12px',
      }}
    >
      Reset App
    </button>
  );
};

export default ResetButton;
