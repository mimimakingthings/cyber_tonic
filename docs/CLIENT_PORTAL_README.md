# Cyber Tonic Client Portal

A comprehensive client management and NIST CSF 2.0 assessment platform built with Streamlit.

## Features

### 🏢 Client Onboarding
- **Wizard-style interface** with 4 steps: Basic Info, Documents, Notes, Review & Submit
- **Form validation** with real-time feedback
- **File upload support** for NDAs, contracts, and policies (PDF, DOCX)
- **Progress tracking** with visual progress bar
- **Data persistence** using Streamlit session state

### 📊 NIST CSF 2.0 Assessment
- **Comprehensive assessment interface** with all 6 functions (Govern, Identify, Protect, Detect, Respond, Recover)
- **Inline editing** with status selection and scoring (1-10 scale)
- **Evidence management** with file uploads and organization
- **Gap analysis** showing subcategories with scores < 5
- **Visual progress tracking** with completion percentages

### 📈 Analytics & Visualization
- **Assessment heatmap** using Plotly for visual score representation
- **Progress indicators** showing completion status
- **Gap analysis reports** with remediation recommendations
- **Evidence tracking** with search and filtering capabilities

### 💾 Data Management
- **JSON export** for clients and assessments
- **Session state persistence** for seamless user experience
- **Mock API integration** ready for backend implementation
- **Data validation** and error handling

## Quick Start

### Prerequisites
- Python 3.9+
- Streamlit 1.28.0+
- Pandas
- Plotly
- FPDF2 (for future report generation)

### Installation
1. Navigate to the project directory:
   ```bash
   cd /path/to/cyber_tonic
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
```bash
streamlit run apps/client_portal.py --server.port 8503
```

The application will be available at: http://localhost:8503

## Application Structure

```
cyber_tonic/
├── apps/
│   └── client_portal.py          # Main application file
├── src/
│   ├── utils.py                  # Helper functions and utilities
│   └── standards_loader.py       # Standards data loading
├── data/
│   └── nist-csf-2.0.json        # NIST CSF 2.0 framework data
├── assets/
│   └── style.css                # Professional styling
└── docs/
    └── CLIENT_PORTAL_README.md   # This file
```

## Usage Guide

### Client Onboarding
1. **Basic Information**: Enter client name, industry, contact details, and company size
2. **Documents**: Upload NDAs, contracts, or policies (optional, max 3 files, 10MB each)
3. **Notes**: Add initial observations or special requirements (optional, max 500 chars)
4. **Review & Submit**: Review all information and submit to add client

### Assessment Process
1. **Select Client**: Choose from the sidebar dropdown
2. **Navigate Functions**: Use expandable sections for each NIST CSF function
3. **Assess Subcategories**: Set status, score (1-10), add notes, and upload evidence
4. **Review Progress**: Monitor completion percentage and identify gaps
5. **Export Results**: Download assessments as JSON for reporting

### Gap Analysis
- Automatically identifies subcategories with scores < 5
- Provides remediation recommendations
- Exportable as CSV for further analysis

### Evidence Management
- Upload supporting documents (PDF, DOCX, PNG, JPG)
- Search and filter evidence by file name or subcategory
- Track upload dates and organize by assessment area

## Technical Features

### Accessibility
- **ARIA labels** for screen readers
- **Keyboard navigation** support
- **High contrast** mode compatibility
- **Responsive design** for mobile devices

### Security
- **File validation** with size and type restrictions
- **Session state** for data persistence (no sensitive data in frontend)
- **Mock API** structure ready for secure backend integration

### Performance
- **Lazy loading** of assessment data
- **Efficient file handling** with size validation
- **Optimized rendering** with Streamlit best practices

## Customization

### Styling
The application uses a professional CSS theme defined in `assets/style.css`:
- **Color scheme**: Blue primary with high contrast
- **Typography**: Sans-serif fonts for readability
- **Responsive design**: Mobile-friendly layout
- **Dark mode**: Automatic theme detection

### Data Structure
- **Clients**: Stored in `st.session_state.clients` as list of dictionaries
- **Assessments**: Stored in `st.session_state.assessments` as nested dictionaries
- **Evidence**: File names stored in `st.session_state.evidence_files`

### Adding New Standards
To add support for additional cybersecurity frameworks:
1. Create JSON file in `data/` directory
2. Update `src/utils.py` to load new framework
3. Modify assessment interface to handle new structure

## Future Enhancements

### Planned Features
- **PDF report generation** using FPDF2
- **Real-time collaboration** for team assessments
- **Advanced analytics** with trend analysis
- **Integration APIs** for external tools
- **Automated scoring** based on evidence analysis

### Backend Integration
The application is designed for easy backend integration:
- **REST API endpoints** for data persistence
- **File storage** for evidence management
- **User authentication** and authorization
- **Audit logging** for compliance tracking

## Troubleshooting

### Common Issues
1. **Import errors**: Ensure all dependencies are installed
2. **File upload issues**: Check file size and format restrictions
3. **Session state**: Refresh page if data appears inconsistent
4. **Port conflicts**: Use different port if 8503 is occupied

### Support
For technical support or feature requests, please refer to the main project documentation or create an issue in the project repository.

## License
This application is part of the Cyber Tonic cybersecurity compliance platform. Please refer to the main project license for usage terms.
