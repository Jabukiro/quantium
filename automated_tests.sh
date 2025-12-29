#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Run pytest
pytest -k 001

# Capture the exit code
exit_code=$?

# Return exit code (0 for success, 1 for failure)
if [ $exit_code -eq 0 ]; then
    exit 0
else
    exit 1
fi