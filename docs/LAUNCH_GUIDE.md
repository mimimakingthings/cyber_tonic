# 🚀 TCP Launch Guide

## Quick Start Options

### Option 1: Launch All Applications (Recommended)
```bash
# macOS/Linux
python3 launch_all.py

# Windows
launch_all.bat
```

### Option 2: Individual Application Launch
```bash
# Main application (launcher)
streamlit run main.py

# Standards Navigator
streamlit run standards_navigator.py

# Client Portal  
streamlit run client_portal.py
```

## 🛠️ Available Scripts

### `launch_all.py` - Multi-App Launcher
- **Purpose**: Launches all three applications simultaneously
- **Features**:
  - ✅ Prerequisites checking
  - ✅ Automatic port assignment (8501, 8502, 8503)
  - ✅ Browser auto-opening
  - ✅ Graceful shutdown with Ctrl+C
  - ✅ Process monitoring

### `launch_all.bat` - Windows Batch Launcher
- **Purpose**: Windows-compatible version of the multi-app launcher
- **Features**: Same as Python version but optimized for Windows

### `cleanup.py` - Project Cleanup
- **Purpose**: Removes unnecessary files and cache
- **Usage**:
  ```bash
  # Dry run (see what would be cleaned)
  python3 cleanup.py --dry-run
  
  # Actual cleanup
  python3 cleanup.py
  ```

## 🌐 Application URLs

When all applications are running:

- **Main Application**: http://localhost:8501
- **Standards Navigator**: http://localhost:8502  
- **Client Portal**: http://localhost:8503

## 📋 Prerequisites

1. **Python 3.9+** installed
2. **Virtual environment** set up:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Dependencies** installed:
   ```bash
   pip install -r requirements.txt
   ```

## 🛑 Stopping Applications

### From Launch Script
- Press **Ctrl+C** in the terminal running `launch_all.py`

### Manual Stop
```bash
# Stop all Streamlit processes
pkill -f streamlit  # macOS/Linux
taskkill /F /IM streamlit.exe  # Windows
```

## 🔧 Troubleshooting

### Port Already in Use
If you get port conflicts:
1. Stop existing applications
2. Run cleanup: `python3 cleanup.py`
3. Restart with launch script

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Permission Issues (macOS/Linux)
```bash
# Make scripts executable
chmod +x launch_all.py cleanup.py
```

## 🎯 Best Practices

1. **Use the launch script** for the best experience
2. **Keep the terminal open** while applications are running
3. **Run cleanup periodically** to free up disk space
4. **Use the main application** to navigate between apps
5. **Check prerequisites** if applications fail to start

## 📊 What the Cleanup Script Removes

- Python cache files (`__pycache__`, `*.pyc`)
- Temporary files (`*.tmp`, `*.log`)
- System files (`.DS_Store`, `Thumbs.db`)
- Test files and development artifacts
- Build and distribution directories

**Note**: The cleanup script preserves all your source code and data files.
