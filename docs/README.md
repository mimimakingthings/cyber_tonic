# TCP Cybersecurity Compliance Hub

A comprehensive Streamlit-based application for cybersecurity compliance consulting with a simple home page interface.

## 🏠 Home Page (`main.py`)
Simple home page with two launch options that automatically start the respective applications.

## 🔍 Standards Navigator (`standards_navigator.py`)
Your personal cybersecurity standards repository and navigation tool for research and knowledge management.

## 🏢 Client Portal (`client_portal.py`)
Dedicated client management and security assessment platform for consulting work.

---

## 🚀 Quick Start

### Easy Launch Scripts
Use the provided launch scripts for the simplest experience:

#### For macOS/Linux Users
```bash
python run.py
```

#### For Windows Users
```batch
run.bat
```

### Manual Launch (Alternative)
```bash
streamlit run main.py
```

### What Happens
1. **Home page opens** at http://localhost:8501
2. **Click "Launch Standards Navigator"** - Opens the standards research tool
3. **Click "Launch Client Portal"** - Opens the client management tool
4. **Applications open automatically** in new browser tabs

**What the launch scripts do:**
1. ✅ **Check Prerequisites**: Verify Python 3 and pip are installed
2. 📦 **Create Virtual Environment**: Set up an isolated Python environment
3. 🔄 **Install Dependencies**: Install all required packages from `requirements.txt`
4. 🚀 **Launch Application**: Start the Streamlit app and open it in your browser

### Manual Setup (Alternative)
If you prefer to run manually:

#### Prerequisites
- Python 3.9+
- Virtual environment (recommended)

#### Installation
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

#### Running the Applications

##### Standards Navigator (Personal Use)
```bash
streamlit run main.py
```
- **Purpose**: Research, explore, and export cybersecurity standards
- **Features**: Search, filter, export controls and requirements
- **Use Case**: Building your knowledge base and preparing for client work

##### Client Portal (Client Work)
```bash
streamlit run client_portal.py
```
- **Purpose**: Manage clients and conduct security assessments
- **Features**: Client management, security evaluation, reporting
- **Use Case**: Taking on new clients and applying frameworks

### Troubleshooting

#### Common Issues
1. **"Permission denied" on macOS/Linux**
   ```bash
   chmod +x launch.sh
   ```

2. **Python not found**
   - Install Python 3.8+ from [python.org](https://python.org)
   - Make sure it's added to your PATH

3. **Virtual environment issues**
   - Delete the `venv` folder and run the script again
   - The script will recreate it automatically

4. **Port already in use**
   - The app runs on port 8501 by default
   - Close any other Streamlit apps or change the port

---

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

---

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

---

## 📁 Simple Project Structure
```
TCP/
├── main.py                 # Home page with launch buttons
├── standards_navigator.py  # Standards research tool
├── client_portal.py        # Client management tool
├── standards_loader.py     # Standards data loader
├── standards_data/         # Standards JSON data files
│   ├── nist_csf_2_0.json  # NIST CSF 2.0 data
│   ├── iso_27001_2022.json # ISO 27001:2022 data
│   ├── gdpr.json          # GDPR data
│   ├── cmmc_2_0.json      # CMMC 2.0 data
│   ├── eu_nis2.json       # EU NIS2 data
│   └── standards_index.json # Standards index
├── run.py                 # Launch script (macOS/Linux)
├── run.bat                # Launch script (Windows)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## 🔧 Configuration

### Standards Data
- Standards data is loaded from `standards_loader.py`
- Currently supports NIST CSF 2.0
- Additional standards can be added to the loader

### Client Data
- Client data is stored in Streamlit session state
- Export/import functionality for data persistence
- JSON format for easy backup and sharing

---

## 🎨 Customization

### Adding New Standards
1. Update `standards_loader.py` with new standard data
2. Add standard to the available standards list
3. Update implementation guidance sections

### Modifying Client Portal
1. Edit `client_portal.py` for client-specific features
2. Customize report templates and export formats
3. Add new evaluation criteria or scoring methods

---

## 📊 Current Standards Coverage

### Available Standards
- **NIST CSF 2.0**: Complete implementation with 6 functions and 106+ subcategories

### Coming Soon
- ISO 27001:2022
- GDPR
- CMMC 2.0
- EU NIS2
- UK NIS Regulations

---

## 🛠️ Technical Details

### Dependencies
- `streamlit>=1.28.0`: Web application framework
- `pandas>=2.0.0`: Data manipulation and CSV export
- `plotly>=5.15.0`: Interactive visualizations
- `fpdf2>=2.7.0`: PDF generation
- `PyPDF2>=3.0.0`: PDF processing

### Architecture
- **Modular Design**: Separate applications for different use cases
- **Session State**: Client data persistence within sessions
- **Caching**: Optimized data loading with Streamlit caching
- **Responsive UI**: Professional styling with custom CSS

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both applications
5. Submit a pull request

---

## 📄 License

This project is for educational and professional use in cybersecurity consulting.

---

## 🆘 Support

For issues or questions:
1. Check the documentation above
2. Review the code comments
3. Test with the simulation mode in Client Portal
4. Ensure all dependencies are installed correctly

---

**Happy Consulting! 🛡️**