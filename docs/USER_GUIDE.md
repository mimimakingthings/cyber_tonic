# Cyber Tonic User Guide

This comprehensive guide will help cybersecurity consultants effectively use Cyber Tonic for compliance assessments and client management.

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Standards Navigator](#standards-navigator)
3. [Client Portal](#client-portal)
4. [Workflow Examples](#workflow-examples)
5. [Troubleshooting](#troubleshooting)
6. [Best Practices](#best-practices)

## 🚀 Getting Started

### First Launch
1. **Install Dependencies**: Run `python launch.py --setup`
2. **Launch Application**: Run `python launch.py`
3. **Access Home Page**: Open http://localhost:8501
4. **Choose Your Tool**: Select Standards Navigator or Client Portal

### Understanding the Interface
- **Home Page**: Central hub with launch buttons for both applications
- **Standards Navigator**: Research and explore cybersecurity standards
- **Client Portal**: Manage clients and conduct assessments

## 🔍 Standards Navigator

### Purpose
Research cybersecurity standards, search controls, and build your knowledge base.

### Key Features

#### Advanced Search
- **Search Terms**: Enter keywords to find relevant controls
- **Search Scope**: Searches across descriptions, examples, and technologies
- **Results Display**: Organized by standard and function

#### Standards Browser
- **Function Navigation**: Browse through NIST CSF 2.0 functions
- **Subcategory Details**: View detailed control information
- **Implementation Guidance**: Get consultant-focused recommendations

#### Export Options
- **CSV Export**: Download search results for analysis
- **PDF Export**: Generate professional consulting materials
- **Knowledge Repository**: Build your personal standards database

### Step-by-Step Usage

1. **Launch Standards Navigator**
   ```
   Click "Launch Standards Navigator" from home page
   ```

2. **Search for Controls**
   ```
   Enter search term (e.g., "encryption", "access control")
   Review results organized by function
   Click on controls for detailed information
   ```

3. **Export Results**
   ```
   Select desired controls
   Choose export format (CSV/PDF)
   Download for client work
   ```

## 🏢 Client Portal

### Purpose
Manage client relationships, conduct assessments, and generate professional reports.

### Key Features

#### Client Management
- **Create Clients**: Add new client profiles with industry information
- **Client Context**: View client details in sidebar navigation
- **Industry Icons**: Visual indicators for different industries

#### Security Assessment
- **Maturity Scoring**: Rate each subcategory from 0-10
- **Gap Analysis**: Identify areas needing improvement
- **Priority Visualization**: Color-coded priority levels

#### Professional Reports
- **Multiple Formats**: Markdown, PDF, and CSV export options
- **Executive Dashboards**: Professional visualizations
- **Customizable Weights**: Adjust scoring weights for different functions

### Step-by-Step Usage

#### Creating a New Client
1. **Launch Client Portal**
   ```
   Click "Launch Client Portal" from home page
   ```

2. **Add Client Information**
   ```
   Click "Add New Client"
   Enter client name, industry, and contact details
   Save client profile
   ```

3. **Conduct Assessment**
   ```
   Select client from sidebar
   Navigate to "Security Assessment"
   Rate each subcategory (0-10 scale)
   Add evidence files as needed
   ```

#### Generating Reports
1. **Access Reports Section**
   ```
   Navigate to "Reports & Analytics"
   Select report type
   ```

2. **Customize Report**
   ```
   Choose visualization options
   Set priority thresholds
   Select export format
   ```

3. **Export and Share**
   ```
   Generate report
   Download in desired format
   Share with client
   ```

## 🔄 Workflow Examples

### Example 1: New Client Assessment

**Scenario**: You're starting work with a new healthcare client.

1. **Research Phase** (Standards Navigator)
   ```
   Search for "healthcare" and "HIPAA" controls
   Export relevant NIST CSF controls
   Build your assessment framework
   ```

2. **Client Setup** (Client Portal)
   ```
   Create client profile for healthcare organization
   Set industry to "Healthcare"
   Add initial contact information
   ```

3. **Assessment Phase** (Client Portal)
   ```
   Conduct initial security assessment
   Rate each NIST CSF subcategory
   Upload supporting evidence
   Generate gap analysis
   ```

4. **Reporting Phase** (Client Portal)
   ```
   Create executive summary
   Generate detailed assessment report
   Export in PDF format
   Present findings to client
   ```

### Example 2: Ongoing Compliance Monitoring

**Scenario**: Quarterly review for existing client.

1. **Data Review** (Client Portal)
   ```
   Load existing client data
   Review previous assessment scores
   Check for new evidence files
   ```

2. **Progress Assessment** (Client Portal)
   ```
   Update maturity scores
   Compare with previous quarter
   Identify improvements made
   ```

3. **Updated Reporting** (Client Portal)
   ```
   Generate progress report
   Highlight improvements
   Identify remaining gaps
   Export updated deliverables
   ```

## 🛠️ Troubleshooting

### Common Issues

#### Application Won't Launch
**Symptoms**: Error messages when running `python launch.py`

**Solutions**:
1. Check Python version: `python --version` (should be 3.9+)
2. Verify dependencies: `pip install -r requirements.txt`
3. Check port availability: Ensure ports 8501-8503 are free
4. Try manual launch: `streamlit run apps/main.py`

#### Data Not Loading
**Symptoms**: Empty client lists or missing assessment data

**Solutions**:
1. Check data directory: Verify `data/storage/` exists
2. Check file permissions: Ensure read/write access
3. Restore from backup: Use files in `data/storage/backups/`
4. Reset data: Delete storage files and start fresh

#### Performance Issues
**Symptoms**: Slow loading or unresponsive interface

**Solutions**:
1. Clear browser cache
2. Restart applications
3. Check system resources
4. Use simulation mode for testing

#### Export Problems
**Symptoms**: Reports not generating or corrupted files

**Solutions**:
1. Check disk space
2. Verify write permissions
3. Try different export format
4. Restart application

### Getting Help

1. **Check Documentation**: Review relevant docs in `docs/` directory
2. **Review Logs**: Check application console for error messages
3. **Test with Sample Data**: Use simulation mode to verify functionality
4. **Report Issues**: Create detailed issue report on GitHub

## 💡 Best Practices

### Data Management
- **Regular Backups**: Use the built-in backup system
- **Export Important Data**: Keep copies of critical assessments
- **Organize Evidence**: Use consistent naming for evidence files
- **Version Control**: Track changes in assessment scores

### Assessment Process
- **Consistent Scoring**: Use the same criteria across all assessments
- **Document Evidence**: Always link scores to supporting evidence
- **Regular Reviews**: Schedule periodic assessment updates
- **Client Communication**: Share progress reports regularly

### Performance Optimization
- **Use Simulation Mode**: Test features without affecting real data
- **Clear Cache**: Regularly clear browser cache for better performance
- **Organize Data**: Keep client data organized and up-to-date
- **Monitor Storage**: Check storage usage regularly

### Security Considerations
- **Local Storage**: Data is stored locally on your machine
- **Backup Security**: Secure your backup files appropriately
- **Access Control**: Limit access to assessment data
- **Regular Updates**: Keep the application updated

## 📞 Support

For additional help:
- **Documentation**: Check `docs/` directory for detailed guides
- **GitHub Issues**: Report bugs or request features
- **Community**: Join discussions and share experiences
- **Updates**: Stay informed about new features and improvements

---

**Happy Consulting! 🛡️**
