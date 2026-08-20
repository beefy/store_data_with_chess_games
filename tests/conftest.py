"""Pytest configuration: add the src directory to the Python path."""
import os
import sys

# Add the src directory to the path so that `from utils import ...` works
SRC_DIR = os.path.join(os.path.dirname(__file__), "..", "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
