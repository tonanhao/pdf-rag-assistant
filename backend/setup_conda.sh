#!/bin/bash

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Conda not found. Please install Miniconda or Anaconda first."
    exit 1
fi

ENV_NAME="rag-demo"

# Check if environment already exists
if conda info --envs | grep -q $ENV_NAME; then
    echo "Conda environment '$ENV_NAME' already exists."
    read -p "Do you want to update it? (y/n): " update_choice
    
    if [[ "$update_choice" == "y" || "$update_choice" == "Y" ]]; then
        echo "Updating conda environment..."
        conda env update -f environment.yml --prune
    else
        echo "Using existing environment without updating."
    fi
else
    # Create conda environment
    echo "Creating conda environment '$ENV_NAME'..."
    conda env create -f environment.yml
fi

# Activate the environment
echo "Activating conda environment..."
eval "$(conda shell.bash hook)"
conda activate $ENV_NAME

# Verify environment is active
if [[ $CONDA_DEFAULT_ENV == "$ENV_NAME" ]]; then
    echo "Conda environment '$ENV_NAME' is now active."
    echo "You can run the backend with 'python run.py'"
else
    echo "Failed to activate conda environment."
    echo "Try manually with: conda activate $ENV_NAME"
fi 