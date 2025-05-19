#!/bin/bash

# Activate conda environment
echo "Activating conda environment..."
eval "$(conda shell.bash hook)"
conda activate rag-demo || { echo "Failed to activate conda environment. Make sure it's created."; exit 1; }

# Start the backend server
echo "Starting backend server..."
cd backend
python run.py &
BACKEND_PID=$!

# Wait for the backend to start
sleep 3

# Start the frontend server
echo "Starting frontend server..."
cd ..
npm run dev &
FRONTEND_PID=$!

# Function to handle cleanup
cleanup() {
    echo "Shutting down servers..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit 0
}

# Register the cleanup function for when script is terminated
trap cleanup SIGINT SIGTERM

# Keep the script running
echo "Both servers are running. Press Ctrl+C to stop."
wait 