"""
GST Legal Reply Generator - Entry Point
Run this file to launch the Streamlit application.
"""

import subprocess
import sys

if __name__ == "__main__":
    # Run the Streamlit app from the src directory
    subprocess.run([sys.executable, "-m", "streamlit", "run", "src/app.py"])
