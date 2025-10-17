"""
Utility functions for the Cyber Tonic Client Portal application.

This module contains helper functions for validation, file handling, data management,
and visualization for the client onboarding and NIST CSF 2.0 assessment features.
"""

import re
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import streamlit as st

def validate_basic_info(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate basic client information.
    
    Args:
        data: Dictionary containing client information
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required fields
    if not data.get("name"):
        return False, "Name is required."
    
    if not data.get("industry"):
        return False, "Industry is required."
    
    # Check email in contact structure
    contact = data.get("contact", {})
    email = contact.get("email", "")
    if not email:
        return False, "Email is required."
    
    # Validate email format
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        return False, "Invalid email format."
    
    # Validate industry
    valid_industries = ["Finance", "Healthcare", "Manufacturing", "IT", "Government", "Education", "Retail", "Other"]
    if data.get("industry") not in valid_industries:
        return False, "Invalid industry selection."
    
    return True, ""

def handle_file_uploads(uploaded_files: List[Any], max_files: int = 3, max_size_mb: int = 10) -> Tuple[bool, str, List[str]]:
    """
    Handle file uploads with validation.
    
    Args:
        uploaded_files: List of uploaded file objects
        max_files: Maximum number of files allowed
        max_size_mb: Maximum file size in MB
        
    Returns:
        Tuple of (is_valid, error_message, file_names)
    """
    if not uploaded_files:
        return True, "", []
    
    # Check number of files
    if len(uploaded_files) > max_files:
        return False, f"Maximum {max_files} files allowed.", []
    
    # Check file sizes
    max_size_bytes = max_size_mb * 1024 * 1024
    total_size = sum(f.size for f in uploaded_files)
    
    if total_size > max_size_bytes:
        return False, f"Total file size exceeds {max_size_mb}MB limit.", []
    
    # Check individual file sizes
    for file in uploaded_files:
        if file.size > max_size_bytes:
            return False, f"File {file.name} exceeds {max_size_mb}MB limit.", []
    
    # Extract file names
    file_names = [f.name for f in uploaded_files]
    
    return True, "", file_names

def save_client(client_data: Dict[str, Any]) -> str:
    """
    Save client data (mock implementation).
    
    Args:
        client_data: Dictionary containing client information
        
    Returns:
        Client ID
    """
    # In a real implementation, this would save to a database
    # For now, we'll just return the client ID
    return client_data.get("id", "")

def load_nist_csf() -> Dict[str, Any]:
    """
    Load NIST CSF 2.0 data from JSON file.
    
    Returns:
        Dictionary containing NIST CSF 2.0 framework data
    """
    try:
        # Try to load from the standards_data directory
        data_path = Path(__file__).parent.parent / "data" / "standards_data" / "nist-csf-2.0.json"
        
        if not data_path.exists():
            # Fallback to a minimal structure if file doesn't exist
            return get_minimal_nist_csf()
        
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    except Exception as e:
        st.error(f"Error loading NIST CSF data: {e}")
        return get_minimal_nist_csf()

def get_minimal_nist_csf() -> Dict[str, Any]:
    """
    Get minimal NIST CSF 2.0 structure for fallback.
    
    Returns:
        Dictionary containing minimal NIST CSF 2.0 framework data
    """
    return {
        "framework": "NIST Cybersecurity Framework 2.0",
        "version": "2.0",
        "functions": [
            {
                "id": "GV",
                "name": "Govern",
                "description": "The Govern function provides organizational cybersecurity risk management strategy, expectations, and policy.",
                "categories": [
                    {
                        "id": "GV.OC",
                        "name": "Organizational Context",
                        "description": "The circumstances—mission, stakeholder expectations, dependencies, and legal, regulatory, and contractual requirements—surrounding the organization's cybersecurity risk management decisions are understood.",
                        "subcategories": [
                            {
                                "id": "GV.OC-01",
                                "description": "Legal, regulatory, and contractual requirements regarding cybersecurity—including privacy and civil liberties obligations—are understood and managed"
                            },
                            {
                                "id": "GV.OC-02",
                                "description": "The organization's role in the supply chain is understood and communicated"
                            }
                        ]
                    },
                    {
                        "id": "GV.RM",
                        "name": "Risk Management Strategy",
                        "description": "The organization's priorities, constraints, risk tolerances, and assumptions are established and used to support operational risk decisions.",
                        "subcategories": [
                            {
                                "id": "GV.RM-01",
                                "description": "Organizational cybersecurity risk management strategy is established"
                            },
                            {
                                "id": "GV.RM-02",
                                "description": "Organizational risk tolerance is determined and clearly expressed"
                            }
                        ]
                    }
                ]
            },
            {
                "id": "ID",
                "name": "Identify",
                "description": "The Identify function develops an organizational understanding to manage cybersecurity risk to systems, assets, data, and capabilities.",
                "categories": [
                    {
                        "id": "ID.AM",
                        "name": "Asset Management",
                        "description": "The data, personnel, devices, systems, and facilities that enable the organization to achieve business purposes are identified and managed consistent with their relative importance to organizational objectives and the organization's risk strategy.",
                        "subcategories": [
                            {
                                "id": "ID.AM-01",
                                "description": "Physical devices and systems within the organization are inventoried"
                            },
                            {
                                "id": "ID.AM-02",
                                "description": "Software platforms and applications within the organization are inventoried"
                            }
                        ]
                    },
                    {
                        "id": "ID.BE",
                        "name": "Business Environment",
                        "description": "The organization's mission, objectives, stakeholders, and activities are understood and prioritized; this information is used to inform cybersecurity roles, responsibilities, and risk management decisions.",
                        "subcategories": [
                            {
                                "id": "ID.BE-01",
                                "description": "The organization's role in the supply chain is identified and communicated"
                            },
                            {
                                "id": "ID.BE-02",
                                "description": "The organization's place in critical infrastructure and its industry sector is identified and communicated"
                            }
                        ]
                    }
                ]
            },
            {
                "id": "PR",
                "name": "Protect",
                "description": "The Protect function outlines appropriate safeguards to ensure delivery of critical infrastructure services.",
                "categories": [
                    {
                        "id": "PR.AC",
                        "name": "Identity Management, Authentication and Access Control",
                        "description": "Access to physical and logical assets and associated facilities is limited to authorized users, processes, or devices, and is managed consistent with the assessed risk of unauthorized access to authorized activities and transactions.",
                        "subcategories": [
                            {
                                "id": "PR.AC-01",
                                "description": "Identities and credentials are issued, managed, verified, revoked, and audited for authorized devices, users and processes"
                            },
                            {
                                "id": "PR.AC-02",
                                "description": "Physical access to assets is managed and protected"
                            }
                        ]
                    }
                ]
            },
            {
                "id": "DE",
                "name": "Detect",
                "description": "The Detect function defines the appropriate activities to identify the occurrence of a cybersecurity event.",
                "categories": [
                    {
                        "id": "DE.AE",
                        "name": "Anomalies and Events",
                        "description": "Anomalous activity is detected and the potential impact of events is understood.",
                        "subcategories": [
                            {
                                "id": "DE.AE-01",
                                "description": "A baseline of network operations and expected data flows for users and systems is established and managed"
                            },
                            {
                                "id": "DE.AE-02",
                                "description": "Detected events are analyzed to understand attack targets and methods"
                            }
                        ]
                    }
                ]
            },
            {
                "id": "RS",
                "name": "Respond",
                "description": "The Respond function includes appropriate activities to take action regarding a detected cybersecurity incident.",
                "categories": [
                    {
                        "id": "RS.RP",
                        "name": "Response Planning",
                        "description": "Response processes and procedures are executed and maintained, to ensure timely response to detected cybersecurity incidents.",
                        "subcategories": [
                            {
                                "id": "RS.RP-01",
                                "description": "Roles and responsibilities are assigned and communicated"
                            },
                            {
                                "id": "RS.RP-02",
                                "description": "Incident response personnel are provided with the necessary authority to act"
                            }
                        ]
                    }
                ]
            },
            {
                "id": "RC",
                "name": "Recover",
                "description": "The Recover function identifies appropriate activities to maintain plans for resilience and to restore any capabilities or services that were impaired due to a cybersecurity incident.",
                "categories": [
                    {
                        "id": "RC.RP",
                        "name": "Recovery Planning",
                        "description": "Recovery processes and procedures are executed and maintained to ensure timely restoration of systems or assets affected by cybersecurity incidents.",
                        "subcategories": [
                            {
                                "id": "RC.RP-01",
                                "description": "Recovery plans incorporate lessons learned"
                            },
                            {
                                "id": "RC.RP-02",
                                "description": "Recovery strategies are updated"
                            }
                        ]
                    }
                ]
            }
        ]
    }

def save_assessment(client_id: str, subcategory_id: str, assessment_data: Dict[str, Any]) -> bool:
    """
    Save assessment data (mock implementation).
    
    Args:
        client_id: Client identifier
        subcategory_id: Subcategory identifier
        assessment_data: Assessment data to save
        
    Returns:
        True if successful, False otherwise
    """
    # In a real implementation, this would save to a database
    # For now, we'll just return True
    return True

def render_heatmap(client_id: str, nist_data: Dict[str, Any]) -> go.Figure:
    """
    Render assessment heatmap visualization.
    
    Args:
        client_id: Client identifier
        nist_data: NIST CSF framework data
        
    Returns:
        Plotly figure object
    """
    # Prepare data for heatmap
    heatmap_data = []
    function_names = []
    category_names = []
    
    for function in nist_data["functions"]:
        for category in function["categories"]:
            for subcategory in category["subcategories"]:
                subcat_id = subcategory["id"]
                
                # Get assessment data
                score = 0
                if (client_id in st.session_state.assessments and 
                    subcat_id in st.session_state.assessments[client_id]):
                    score = st.session_state.assessments[client_id][subcat_id].get("score", 0)
                
                heatmap_data.append(score)
                function_names.append(function["name"])
                category_names.append(f"{category['id']} - {category['name']}")
    
    # Create DataFrame
    df = pd.DataFrame({
        "Function": function_names,
        "Category": category_names,
        "Score": heatmap_data
    })
    
    # Create pivot table for heatmap
    pivot_df = df.pivot_table(
        index="Function", 
        columns="Category", 
        values="Score", 
        aggfunc="mean"
    )
    
    # Create heatmap
    fig = px.imshow(
        pivot_df,
        color_continuous_scale="RdYlGn",
        aspect="auto",
        title="NIST CSF 2.0 Assessment Heatmap",
        labels={"color": "Average Score"}
    )
    
    fig.update_layout(
        height=600,
        xaxis_title="Categories",
        yaxis_title="Functions",
        font=dict(size=10)
    )
    
    return fig

def get_assessment_progress(client_id: str, nist_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate assessment progress for a client.
    
    Args:
        client_id: Client identifier
        nist_data: NIST CSF framework data
        
    Returns:
        Dictionary containing progress information
    """
    total_subcategories = 0
    completed_subcategories = 0
    
    for function in nist_data["functions"]:
        for category in function["categories"]:
            for subcategory in category["subcategories"]:
                total_subcategories += 1
                subcat_id = subcategory["id"]
                
                if (client_id in st.session_state.assessments and 
                    subcat_id in st.session_state.assessments[client_id]):
                    assessment = st.session_state.assessments[client_id][subcat_id]
                    if (assessment.get("status") != "Not Implemented" and 
                        assessment.get("score", 0) > 0):
                        completed_subcategories += 1
    
    completion_percentage = (completed_subcategories / total_subcategories * 100) if total_subcategories > 0 else 0
    
    return {
        "total_subcategories": total_subcategories,
        "completed_subcategories": completed_subcategories,
        "completion_percentage": completion_percentage
    }

def export_clients_json(clients: List[Dict[str, Any]]) -> str:
    """
    Export clients data as JSON string.
    
    Args:
        clients: List of client dictionaries
        
    Returns:
        JSON string representation
    """
    return json.dumps({"clients": clients}, indent=2, default=str)

def export_assessments_json(assessments: Dict[str, Any]) -> str:
    """
    Export assessments data as JSON string.
    
    Args:
        assessments: Dictionary of assessments
        
    Returns:
        JSON string representation
    """
    return json.dumps(assessments, indent=2, default=str)

def validate_email(email: str) -> bool:
    """
    Validate email format using regex.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

def get_remediation_tips() -> Dict[str, str]:
    """
    Get remediation tips for NIST CSF subcategories.
    
    Returns:
        Dictionary mapping subcategory IDs to remediation tips
    """
    return {
        "GV.OC-01": "Establish a legal and compliance review process for cybersecurity requirements. Create a compliance matrix and regular review schedule.",
        "GV.OC-02": "Document and communicate your organization's role in the supply chain. Create supply chain cybersecurity policies.",
        "GV.OC-03": "Create a critical infrastructure dependency inventory and prioritize based on business impact.",
        "GV.RM-01": "Develop a comprehensive cybersecurity risk management strategy document aligned with business objectives.",
        "GV.RM-02": "Define and document organizational risk tolerance levels with clear metrics and thresholds.",
        "GV.RM-03": "Conduct sector-specific risk analysis and incorporate into risk tolerance decisions.",
        "ID.AM-01": "Implement automated asset discovery and inventory management tools. Regular asset audits.",
        "ID.AM-02": "Deploy software asset management (SAM) solutions for comprehensive software inventory.",
        "ID.AM-03": "Create network diagrams and data flow documentation. Use automated mapping tools.",
        "ID.AM-04": "Maintain a catalog of external systems and their security requirements.",
        "ID.AM-05": "Implement asset classification and prioritization based on business value and risk.",
        "ID.AM-06": "Define and document cybersecurity roles and responsibilities matrix (RACI).",
        "ID.BE-01": "Document supply chain relationships and cybersecurity expectations in contracts.",
        "ID.BE-02": "Identify critical infrastructure dependencies and industry sector requirements.",
        "ID.BE-03": "Align cybersecurity priorities with business mission and objectives.",
        "ID.BE-04": "Map critical business functions and their dependencies.",
        "ID.BE-05": "Develop resilience requirements for different operational states (normal, under attack, recovery).",
        "ID.RA-01": "Implement vulnerability scanning and assessment tools. Regular vulnerability assessments.",
        "ID.RA-02": "Subscribe to threat intelligence feeds and information sharing forums.",
        "ID.RA-03": "Conduct threat modeling and maintain threat landscape documentation.",
        "ID.RA-04": "Perform business impact analysis for potential cybersecurity incidents.",
        "ID.RA-05": "Implement risk assessment methodology and tools. Regular risk assessments.",
        "ID.RA-06": "Develop risk response strategies and prioritization framework.",
        "PR.AC-01": "Implement identity and access management (IAM) solutions with proper lifecycle management.",
        "PR.AC-02": "Establish physical security controls and access management procedures.",
        "PR.AC-03": "Implement secure remote access solutions with multi-factor authentication.",
        "PR.AC-04": "Implement principle of least privilege and separation of duties in access controls.",
        "PR.AC-05": "Implement network segmentation and segregation controls.",
        "PR.AC-06": "Implement identity proofing and credential binding processes.",
        "PR.AC-07": "Implement risk-based authentication with appropriate factors.",
        "PR.AT-01": "Develop comprehensive cybersecurity awareness training program for all users.",
        "PR.AT-02": "Provide specialized training for privileged users on their security responsibilities.",
        "PR.AT-03": "Educate third-party stakeholders on their cybersecurity roles and responsibilities.",
        "PR.AT-04": "Provide executive cybersecurity training and awareness programs.",
        "PR.AT-05": "Provide specialized training for cybersecurity and physical security personnel.",
        "DE.AE-01": "Establish network baselines and implement continuous monitoring of data flows.",
        "DE.AE-02": "Implement security information and event management (SIEM) for event analysis.",
        "DE.AE-03": "Implement log aggregation and correlation across multiple sources.",
        "DE.AE-04": "Develop incident impact assessment procedures and tools.",
        "DE.AE-05": "Establish alert thresholds and escalation procedures.",
        "DE.CM-01": "Implement network monitoring and intrusion detection systems.",
        "DE.CM-02": "Implement physical security monitoring and environmental controls.",
        "DE.CM-03": "Implement user activity monitoring and behavioral analytics.",
        "DE.CM-04": "Implement malware detection and prevention solutions.",
        "DE.CM-05": "Implement mobile code detection and prevention controls.",
        "DE.CM-06": "Monitor external service provider activities and access.",
        "DE.CM-07": "Implement continuous monitoring for unauthorized access and devices.",
        "DE.CM-08": "Implement vulnerability scanning and assessment tools.",
        "RS.RP-01": "Define and communicate incident response roles and responsibilities.",
        "RS.RP-02": "Provide incident response personnel with necessary authority and resources.",
        "RS.RP-03": "Conduct regular incident response testing and tabletop exercises.",
        "RS.RP-04": "Implement lessons learned process and update response plans accordingly.",
        "RS.CO-01": "Develop incident response procedures and communication protocols.",
        "RS.CO-02": "Establish incident reporting criteria and procedures.",
        "RS.CO-03": "Implement information sharing procedures consistent with response plans.",
        "RS.CO-04": "Establish stakeholder coordination procedures for incident response.",
        "RS.CO-05": "Participate in information sharing initiatives and threat intelligence sharing.",
        "RC.RP-01": "Implement lessons learned process and update recovery plans accordingly.",
        "RC.RP-02": "Regularly review and update recovery strategies based on changing threats.",
        "RC.RP-03": "Incorporate third-party and dependency information into recovery plans.",
        "RC.IM-01": "Implement continuous improvement process for recovery capabilities.",
        "RC.IM-02": "Regularly update recovery strategies based on lessons learned and threat landscape."
    }
