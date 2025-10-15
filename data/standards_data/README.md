# Cybersecurity Standards Database

This directory contains the structured database of cybersecurity standards and frameworks used by the Cybersecurity Compliance Hub application.

## 📁 Directory Structure

```
standards_data/
├── README.md                    # This file
├── standards_index.json         # Master index of all standards
├── nist_csf_2_0.json          # NIST Cybersecurity Framework 2.0
├── iso_27001_2022.json        # ISO/IEC 27001:2022
├── gdpr.json                   # General Data Protection Regulation
├── cmmc_2_0.json              # Cybersecurity Maturity Model Certification 2.0
└── eu_nis2.json               # EU NIS2 Directive
```

## 📋 Standards Index

The `standards_index.json` file serves as the master index and contains:

- **Metadata**: Version, last updated date, total standards count
- **Standards List**: All available standards with their metadata
- **Categories**: Standards grouped by type (Framework, Standard, Regulation, etc.)
- **Regions**: Standards grouped by regional applicability

## 🔧 Adding New Standards

### 1. Create the Standard JSON File

Create a new JSON file following this structure:

```json
{
  "standard_id": "UNIQUE_ID",
  "name": "Full Standard Name",
  "version": "Version Number",
  "overview": "Brief description of the standard",
  "region": "Regional applicability",
  "type": "Framework|Standard|Regulation|Certification|Directive",
  "last_updated": "YYYY-MM-DD",
  "official_url": "https://official-url.com",
  "functions": {
    "Function_Name": {
      "description": "Function description",
      "categories": ["Category1", "Category2"],
      "subcategories": {
        "CONTROL-01": {
          "description": "Control description",
          "examples": "Implementation examples",
          "use_cases": "Practical use cases",
          "regional_relevance": ["USA", "EU", "UK"],
          "tech_recommendations": ["Technology1", "Technology2"],
          "mappings": {
            "Other_Standard": "CONTROL-X"
          }
        }
      }
    }
  }
}
```

### 2. Update the Standards Index

Add your new standard to `standards_index.json`:

```json
{
  "standards": {
    "YOUR_STANDARD_ID": {
      "file": "your_standard_file.json",
      "name": "Your Standard Name",
      "type": "Standard",
      "region": "Global",
      "status": "Active",
      "priority": "High"
    }
  },
  "categories": {
    "Standards": ["ISO_27001_2022", "YOUR_STANDARD_ID"]
  },
  "regions": {
    "Global": ["ISO_27001_2022", "YOUR_STANDARD_ID"]
  }
}
```

### 3. Update Metadata

Update the metadata section in `standards_index.json`:

```json
{
  "metadata": {
    "version": "1.0",
    "last_updated": "2024-10-15",
    "description": "Master index of cybersecurity standards and frameworks",
    "total_standards": 6
  }
}
```

## 🔍 Cross-Mapping Standards

Cross-mappings allow you to link controls between different standards. Add mappings in the `mappings` field of each control:

```json
{
  "mappings": {
    "NIST_CSF_2.0": "PR.AC-01",
    "ISO_27001_2022": "A.9.1.1",
    "GDPR": "Article 32"
  }
}
```

## 🧪 Validation

Use the validation script to check your standards data:

```bash
python3 validate_standards.py
```

This will:
- ✅ Validate JSON structure
- ✅ Check required fields
- ✅ Verify cross-mappings
- ✅ Generate statistics
- ✅ Test search functionality

## 📊 Current Standards

| Standard | Type | Region | Controls | Status |
|----------|------|--------|----------|--------|
| NIST CSF 2.0 | Framework | USA (Global) | 6+ | Active |
| ISO 27001:2022 | Standard | Global | 4+ | Active |
| GDPR | Regulation | EU/UK | 5 | Active |
| CMMC 2.0 | Certification | USA (DoD) | 4+ | Active |
| EU NIS2 | Directive | EU | 8+ | Active |

## 🔧 Data Management

### Loading Standards

The application uses the `standards_loader.py` module to load standards:

```python
from standards_loader import load_standard, load_all_standards

# Load a specific standard
nist_data = load_standard("NIST_CSF_2.0")

# Load all standards
all_standards = load_all_standards()
```

### Searching Controls

```python
from standards_loader import search_controls

# Search across all standards
results = search_controls("access control")

# Search specific standards
results = search_controls("encryption", ["NIST_CSF_2.0", "ISO_27001_2022"])
```

### Cross-Mapping Analysis

```python
from standards_loader import get_cross_mappings

# Get mappings for a specific control
mappings = get_cross_mappings("PR.AC-01", "NIST_CSF_2.0")

# Get all cross-mappings
all_mappings = standards_loader.get_all_cross_mappings()
```

## 🚀 Best Practices

1. **Consistent Naming**: Use consistent naming conventions for control IDs
2. **Complete Data**: Fill in all required fields for each control
3. **Cross-Mappings**: Add cross-mappings to related standards
4. **Regular Updates**: Keep standards data current with official updates
5. **Validation**: Always validate data after making changes
6. **Documentation**: Update this README when adding new standards

## 🔄 Version Control

- Each standard file includes a `last_updated` field
- The master index tracks the overall database version
- Use semantic versioning for major updates
- Document changes in commit messages

## 📞 Support

For questions about the standards database:
1. Check this README
2. Review the validation script output
3. Examine existing standards for examples
4. Test with the validation script before deploying

---

**Last Updated**: 2024-10-15  
**Database Version**: 1.0  
**Total Standards**: 5
