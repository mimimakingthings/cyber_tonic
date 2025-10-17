# Cyber Tonic Cybersecurity Compliance Hub

A comprehensive Streamlit-based application for cybersecurity compliance consulting with an organized, professional structure.

## 🏗️ Project Structure

```
Cyber Tonic/
├── 📁 apps/                    # Streamlit Applications
│   ├── 🐍 main.py             # Home page with launch buttons
│   ├── 🐍 client_portal.py    # Client management & NIST CSF assessment
│   └── 🐍 standards_navigator.py  # Standards research tool
├── 📁 src/                    # Core Modules & Utilities
│   ├── 🐍 standards_loader.py # Standards data loader
│   ├── 🐍 utils.py            # Validation, file handling, visualization
│   ├── 🐍 data_persistence.py # Data persistence and storage management
│   ├── 🐍 sidebar_component.py # Enhanced sidebar navigation component
│   └── 🐍 assessment_enhancements.py # Advanced assessment features
├── 📁 data/                   # Data Files & Standards
│   ├── 📁 standards_data/     # Standards JSON data files
│   │   └── 📄 nist-csf-2.0.json  # NIST Cybersecurity Framework 2.0
│   ├── 📁 storage/            # Persistent data storage
│   │   ├── 📄 clients.json    # Client data
│   │   ├── 📄 assessments.json # Assessment data
│   │   ├── 📄 evidence_files.json # Evidence file references
│   │   └── 📁 backups/        # Automatic backups
│   └── 📁 schemas/            # Data schemas
│       └── 📄 assessment_schema_v2.json # Assessment data schema
├── 📁 assets/                 # Static Assets
│   └── 🎨 style.css           # Custom CSS styling
├── 📁 docs/                   # Documentation
│   ├── 📄 CLIENT_PORTAL_README.md  # Client portal docs
│   ├── 📄 LAUNCH_GUIDE.md    # Launch instructions
│   ├── 📄 DATA_PERSISTENCE.md # Data persistence documentation
│   ├── 📄 ENHANCED_SIDEBAR.md # Enhanced sidebar component docs
│   ├── 📄 ASSESSMENT_ENHANCEMENTS_SUMMARY.md # Assessment features summary
│   └── 📄 VISUAL_ENHANCEMENTS_IMPLEMENTATION.md # Visual enhancements guide
├── 📁 tests/                  # Test Files
│   └── 🧪 test_assessment_enhancements.py # Unit tests
├── 🚀 launch.py              # Master launcher (Python)
├── 🚀 launch.sh              # Master launcher (Shell)
├── 📄 requirements.txt       # Python dependencies
└── 📄 README.md             # This file
```


## 🚀 Quick Start

### Easy Launch Options

#### Option 1: Master Launcher (Recommended)
```bash
python launch.py                    # Launch main app only
python launch.py --all              # Launch all apps simultaneously
python launch.py --setup            # Set up virtual environment
python launch.py --clean            # Clean up temporary files
```

#### Option 2: Shell Script (Unix/Mac)
```bash
./launch.sh                         # Launch main app only
./launch.sh --all                   # Launch all apps simultaneously
./launch.sh --setup                 # Set up virtual environment
./launch.sh --clean                 # Clean up temporary files
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
- **🔒 Security Assessment**: Maturity scoring (0-10) for each subcategory
- **📊 Enhanced Interactive Visualizations**: 
  - Professional Plotly charts with pastel color scheme
  - Individual chart components (pie, bar, histogram, urgency)
  - Improved spacing and no text overlaps
  - Responsive design with proper margins
- **📋 Professional Reports**: Markdown, PDF, and CSV export options
- **🎲 Simulation Mode**: Generate test clients for demonstration
- **💾 Advanced Data Persistence**: 
  - Automatic save/load across sessions
  - Real-time data backup system
  - Manual save controls and storage info
  - Comprehensive export/import options
- **🔍 Enhanced Gap Analysis Dashboard**:
  - **Pastel Color Scheme**: Color-blind friendly priority visualization
  - **Advanced Filtering**: Multi-criteria filtering with expandable UI
  - **Individual Chart Components**: Separate charts for better analysis
  - **Professional Styling**: Executive-grade visualizations
  - **Priority-based Color Coding**: Critical, High, Medium, Low with distinct colors
  - **Scrollable Tables**: Fixed height with proper text wrapping
- **📁 Evidence Management**: Upload and track supporting documents with tagging
- **⚖️ Weights Configuration**: Customizable scoring weights for NIST functions
- **🎨 Enhanced Sidebar Navigation**:
  - Clear client context with industry icons
  - Active page indicators and search functionality
  - Responsive design with mobile optimization
  - Accessibility features and keyboard navigation

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.9+
- Virtual environment (recommended)

### Installation
1. Clone the repository
2. Set up the environment automatically:
   ```bash
   python launch.py --setup
   ```
   
   Or manually:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
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

## 💾 Data Persistence

### Automatic Features
- **Auto-Save**: Data is automatically saved when you add clients or update assessments
- **Auto-Load**: All data is automatically loaded when you start the application
- **Change Detection**: Only saves when data actually changes to optimize performance
- **Backup System**: Automatic backups created before each save operation

### Manual Controls
- **Save All Data**: Manual save button in the sidebar
- **Storage Info**: View storage details and file information
- **Export Options**: Export all data or specific data types
- **Last Save Indicator**: Shows when data was last saved

### Data Safety
- **JSON Storage**: Human-readable format in `data/storage/` directory
- **Backup Retention**: Keeps the 10 most recent backups automatically
- **Error Recovery**: Graceful handling of data loading/saving errors
- **Export/Import**: Full data export for backup and migration

For detailed information, see [DATA_PERSISTENCE.md](docs/DATA_PERSISTENCE.md).

## 📊 Current Standards Coverage

### Available Standards
- **NIST CSF 2.0**: Complete implementation with 6 functions and 106 subcategories

### Coming Soon
- ISO 27001:2022
- GDPR
- CMMC 2.0
- EU NIS2
- UK NIS Regulations

## 🎨 Visual Enhancements

### Gap Analysis Dashboard Improvements
- **Pastel Color Scheme**: 
  - Critical: `#FF9999` (Pastel Red)
  - High: `#FFCC99` (Pastel Orange)
  - Medium: `#FFFF99` (Pastel Yellow)
  - Low: `#99FF99` (Pastel Green)
- **Enhanced Tab Spacing**: 32px gaps with professional styling
- **Text Overlap Fixes**: Proper margins and text wrapping
- **Individual Chart Components**: Separate methods for each visualization type
- **Professional Styling**: Executive-grade appearance suitable for client presentations

### Technical Improvements
- **Fixed Caching Issues**: Resolved UnhashableParamError in visualization methods
- **Improved Performance**: Optimized chart generation and rendering
- **Better Error Handling**: Graceful handling of missing data and edge cases
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🛠️ Technical Details

### Dependencies
- `streamlit>=1.28.0`: Web application framework
- `pandas>=2.0.0`: Data manipulation and CSV export
- `plotly>=5.15.0`: Interactive visualizations
- `fpdf2>=2.7.0`: PDF generation
- `PyPDF2>=3.0.0`: PDF processing
- `numpy>=1.24.0`: Numerical computations for trend analysis

### Architecture
- **Modular Design**: Separate applications for different use cases
- **Organized Structure**: Clean separation of apps, data, and utilities
- **Persistent Data Storage**: JSON-based file storage with automatic backups
- **Session State**: Enhanced session management with data persistence
- **Responsive UI**: Professional styling with custom CSS and pastel colors
- **Data Safety**: Automatic backup system and error recovery
- **Enhanced Navigation**: Modern sidebar component with client context
- **Accessibility**: WCAG compliant design with color-blind friendly palette
- **Visual Excellence**: Executive-grade dashboards with professional styling

## 🧹 Maintenance

### Cleanup
```bash
python launch.py --clean
```

### Development
- All applications are in the `apps/` directory
- Core modules are in the `src/` directory
- Data files are in the `data/` directory
- Use `launch.py` for all launching needs

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
5. Check data persistence logs in the application
6. Verify storage directory permissions in `data/storage/`

### Data Issues
- **Data not loading**: Check `data/storage/` directory and file permissions
- **Data not saving**: Verify write permissions and available disk space
- **Corrupted data**: Restore from backups in `data/storage/backups/`
- **Storage info**: Use the "Storage Info" button in the Client Portal sidebar

---

**Happy Consulting! 🛡️**
