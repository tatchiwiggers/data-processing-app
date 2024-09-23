import sys
import os

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up two levels from the current directory
parent_dir = os.path.dirname(os.path.dirname(current_dir))

# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)

# Now you can import the module
from src.webscraping_ml import schema

# Use the module as needed
print(parent_dir)
