#!/bin/bash
# Create venv if not exists
if [ ! -d "skills/self-learning-agent/venv" ]; then
    python3 -m venv skills/self-learning-agent/venv
fi

# Activate venv
source skills/self-learning-agent/venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r skills/self-learning-agent/requirements.txt

echo "Environment setup complete."
