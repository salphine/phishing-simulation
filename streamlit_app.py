import streamlit as st
import sys
from pathlib import Path

# Add frontend directory to path
frontend_path = Path(__file__).parent / 'frontend'
sys.path.append(str(frontend_path))

# Run the main app
exec(open(frontend_path / 'app.py').read())
