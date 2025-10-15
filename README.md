# TCP Cybersecurity Compliance Hub

A comprehensive Streamlit-based application for cybersecurity compliance consulting with an organized, professional structure.

## 🏗️ Project Structure

```
TCP/
├── apps/                    # Streamlit applications
│   ├── main.py             # Home page with launch buttons
│   ├── standards_navigator.py  # Standards research tool
│   └── client_portal.py    # Client management tool
├── src/                    # Core modules and utilities
│   └── standards_loader.py # Standards data loader
├── data/                   # Data files and standards
│   └── standards_data/     # Standards JSON data files
├── scripts/                # Launch and utility scripts
│   ├── run.py             # Simple launch script
│   ├── launch_all.py      # Multi-app launcher
│   └── cleanup.py         # Cleanup utility
├── docs/                   # Documentation
│   ├── README.md          # Detailed documentation
│   └── LAUNCH_GUIDE.md    # Launch instructions
├── venv/                   # Virtual environment
├── main.py                 # Main entry point
├── run.py                  # Quick launch script
├── launch_all.py          # Multi-app launcher
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🚀 Quick Start

### Easy Launch Options

#### Option 1: Simple Launch
```bash
python run.py
```

#### Option 2: Launch All Apps
```bash
python launch_all.py
```

#### Option 3: Direct Streamlit
```bash
streamlit run apps/main.py
```

### What Happens
1. **Home page opens** at http://localhost:8501
2. **Click "Launch Standards Navigator"** - Opens the standards research tool
3. **Click "Launch Client Portal"** - Opens the client management tool
4. **Applications open automatically** in new browser tabs

## 📋 Features Overview

### Standards Navigator Features
- **🔍 Advanced Search**: Search across NIST CSF 2.0 controls, descriptions, and technologies
- **📊 Standards Browser**: Navigate through functions and subcategories
- **📥 Export Options**: CSV and PDF export for consulting materials
- **🎯 Implementation Guidance**: Consultant-focused recommendations
- **📚 Knowledge Repository**: Personal standards database

### Client Portal Features
- **👥 Client Management**: Create, manage, and track multiple clients
- **🔒 Security Assessment**: Maturity scoring (0-5) for each subcategory
- **📊 Interactive Visualizations**: Plotly charts for function-level scores
- **📋 Professional Reports**: Markdown, PDF, and CSV export options
- **🎲 Simulation Mode**: Generate test clients for demonstration
- **💾 Data Persistence**: Save/load client data across sessions

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.9+
- Virtual environment (recommended)

### Installation
1. Clone the repository
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Workflow

### Typical Consulting Workflow
1. **Research Phase** (Standards Navigator):
   - Search for relevant controls and requirements
   - Export standard data for analysis
   - Build your knowledge base

2. **Client Work Phase** (Client Portal):
   - Create new client profiles
   - Conduct security posture evaluations
   - Generate professional reports
   - Export deliverables

3. **Reference Phase** (Both Applications):
   - Keep Standards Navigator open for quick reference
   - Switch between applications as needed
   - Maintain separate workspaces for personal vs. client work

## 📊 Current Standards Coverage

### Available Standards
- **NIST CSF 2.0**: Complete implementation with 6 functions and 106+ subcategories

### Coming Soon
- ISO 27001:2022
- GDPR
- CMMC 2.0
- EU NIS2
- UK NIS Regulations

## 🛠️ Technical Details

### Dependencies
- `streamlit>=1.28.0`: Web application framework
- `pandas>=2.0.0`: Data manipulation and CSV export
- `plotly>=5.15.0`: Interactive visualizations
- `fpdf2>=2.7.0`: PDF generation
- `PyPDF2>=3.0.0`: PDF processing

### Architecture
- **Modular Design**: Separate applications for different use cases
- **Organized Structure**: Clean separation of apps, data, and utilities
- **Session State**: Client data persistence within sessions
- **Caching**: Optimized data loading with Streamlit caching
- **Responsive UI**: Professional styling with custom CSS

## 🧹 Maintenance

### Cleanup
```bash
python scripts/cleanup.py
```

### Development
- All applications are in the `apps/` directory
- Core modules are in the `src/` directory
- Data files are in the `data/` directory
- Launch scripts are in the `scripts/` directory

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both applications
5. Submit a pull request

## 📄 License

This project is for educational and professional use in cybersecurity consulting.

## 🆘 Support

For issues or questions:
1. Check the documentation in `docs/`
2. Review the code comments
3. Test with the simulation mode in Client Portal
4. Ensure all dependencies are installed correctly

---

**Happy Consulting! 🛡️**
