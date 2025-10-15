#!/usr/bin/env python3
"""
TCP Cybersecurity Compliance Hub - Quick Launch Script
Simple script to run the home page application.
"""

import subprocess
import sys
import platform
from pathlib import Path

def main():
    """Launch the TCP Cybersecurity Compliance Hub home page."""
    print("🛡️ TCP Cybersecurity Compliance Hub")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("apps/main.py").exists():
        print("❌ Error: apps/main.py not found. Please run this script from the TCP directory.")
        return 1
    
    # Check if virtual environment exists
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ Error: Virtual environment not found.")
        print("💡 Please set up the environment first:")
        print("   python -m venv venv")
        print("   source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print("   pip install -r requirements.txt")
        return 1
    
    # Get the appropriate streamlit command
    if platform.system() == "Windows":
        streamlit_cmd = venv_path / "Scripts" / "streamlit.exe"
    else:
        streamlit_cmd = venv_path / "bin" / "streamlit"
    
    if not streamlit_cmd.exists():
        print("❌ Error: Streamlit not found in virtual environment.")
        print("💡 Please install dependencies: pip install -r requirements.txt")
        return 1
    
    print("🚀 Launching TCP Cybersecurity Compliance Hub...")
    print("🌐 The application will open in your browser at http://localhost:8501")
    print("📝 Press Ctrl+C to stop the application")
    print()
    
    try:
        # Launch the application
        subprocess.run([str(streamlit_cmd), "run", "apps/main.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user. Goodbye!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching application: {e}")
        return 1
    except FileNotFoundError:
        print("❌ Error: Streamlit command not found.")
        print("💡 Please ensure the virtual environment is properly set up.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
