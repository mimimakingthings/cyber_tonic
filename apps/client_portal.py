"""
Client Portal Application for Cyber Tonic

A comprehensive client management and NIST CSF 2.0 assessment platform built with Streamlit.
Features client onboarding wizard and cybersecurity assessment dashboard.
"""

import streamlit as st
import pandas as pd
import uuid
import re
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import (
    validate_basic_info, 
    handle_file_uploads, 
    save_client, 
    load_nist_csf, 
    save_assessment, 
    render_heatmap,
    get_assessment_progress,
    get_remediation_tips
)
from data_persistence import (
    data_persistence,
    save_session_data,
    load_session_data,
    auto_save_data
)
from sidebar_component import render_enhanced_sidebar
from assessment_enhancements import (
    assessment_weights,
    evidence_manager,
    gap_analyzer
)

# Page configuration
st.set_page_config(
    page_title="Cyber Tonic - Client Portal",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
def load_css():
    """Load custom CSS for enhanced visual styling with pastel colors and improved spacing."""
    st.markdown("""
    <style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Enhanced tab spacing and styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 32px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        font-size: 15px;
        border-radius: 8px;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6;
        color: white;
        border-color: #3b82f6;
    }
    
    /* Element container spacing */
    .element-container {
        margin-bottom: 24px;
    }
    
    /* DataFrame styling with pastel colors and text wrapping */
    .stDataFrame td, .stDataFrame th {
        padding: 10px;
        white-space: pre-wrap;
        font-size: 14px;
        text-align: left;
    }
    
    /* Pastel priority color coding */
    .priority-critical {
        background-color: #FF9999 !important;
        color: black !important;
        border-left: 4px solid #FF6666;
    }
    
    .priority-high {
        background-color: #FFCC99 !important;
        color: black !important;
        border-left: 4px solid #FFAA66;
    }
    
    .priority-medium {
        background-color: #FFFF99 !important;
        color: black !important;
        border-left: 4px solid #FFFF66;
    }
    
    .priority-low {
        background-color: #99FF99 !important;
        color: black !important;
        border-left: 4px solid #66FF66;
    }
    
    /* KPI cards with better spacing */
    [data-testid="metric-container"] {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Enhanced expander styling */
    .streamlit-expanderHeader {
        background-color: #f1f5f9;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #3b82f6, #1d4ed8);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    /* Success message styling */
    .stSuccess {
        background-color: #D1FAE5;
        border: 1px solid #10B981;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Info message styling */
    .stInfo {
        background-color: #DBEAFE;
        border: 1px solid #3B82F6;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Warning message styling */
    .stWarning {
        background-color: #FEF3C7;
        border: 1px solid #F59E0B;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Chart container styling */
    .js-plotly-plot {
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Scrollable table container */
    .stDataFrame > div {
        max-height: 400px;
        overflow-y: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# Load CSS
load_css()

# Caching for performance
@st.cache_data
def get_cached_nist_data():
    """Cache NIST data for better performance."""
    return load_nist_csf()

@st.cache_data
def get_cached_gap_analysis(assessments_hash, weights_hash, nist_hash):
    """Cache gap analysis results for better performance."""
    # This will be implemented when we have the actual data
    pass

def initialize_session_state():
    """Initialize session state variables and load persistent data."""
    # Initialize basic session state variables
    if "onboarding_step" not in st.session_state:
        st.session_state.onboarding_step = 0
    if "client_form_data" not in st.session_state:
        st.session_state.client_form_data = {}
    if "selected_client" not in st.session_state:
        st.session_state.selected_client = None
    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = False
    if "last_save_time" not in st.session_state:
        st.session_state.last_save_time = None
    if "data_hash" not in st.session_state:
        st.session_state.data_hash = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Assessment Dashboard"
    
    # Load persistent data if not already loaded
    if not st.session_state.data_loaded:
        with st.spinner("Loading saved data..."):
            if load_session_data():
                st.success("✅ Data loaded successfully!")
            else:
                # Initialize with empty data if loading fails
                st.session_state.clients = []
                st.session_state.assessments = {}
                st.session_state.evidence_files = {}
                st.warning("⚠️ Could not load saved data. Starting with empty data.")
        
        st.session_state.data_loaded = True

def client_onboarding():
    """Client onboarding wizard with 4 steps."""
    st.title("🛡️ Cyber Tonic - Client Portal")
    
    # Check if we're in edit mode
    is_editing = st.session_state.get("editing_client", False)
    editing_client_id = st.session_state.get("editing_client_id", None)
    
    if is_editing:
        st.markdown('<h2 aria-label="Edit Client">✏️ Edit Client</h2>', unsafe_allow_html=True)
    else:
        st.markdown('<h2 aria-label="Client Onboarding">Client Onboarding</h2>', unsafe_allow_html=True)
    
    steps = ["Basic Info", "Documents", "Notes", "Review & Submit"]
    current_step = st.session_state.onboarding_step
    
    # Progress bar
    progress = current_step / len(steps)
    st.progress(progress)
    st.markdown(f"**Step {current_step + 1} of {len(steps)}: {steps[current_step]}**")
    
    # Step 1: Basic Information
    if current_step == 0:
        st.markdown('<h3 aria-label="Basic Information">Basic Information</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Client Name *", 
                value=st.session_state.client_form_data.get("name", ""),
                help="Enter the full legal name of the client organization"
            )
            industry = st.selectbox(
                "Industry *",
                ["Finance", "Healthcare", "Manufacturing", "IT", "Government", "Education", "Retail", "Other"],
                index=["Finance", "Healthcare", "Manufacturing", "IT", "Government", "Education", "Retail", "Other"].index(st.session_state.client_form_data.get("industry", "Finance")) if st.session_state.client_form_data.get("industry") in ["Finance", "Healthcare", "Manufacturing", "IT", "Government", "Education", "Retail", "Other"] else 0,
                help="Select the primary industry sector"
            )
            email = st.text_input(
                "Email *",
                value=st.session_state.client_form_data.get("contact", {}).get("email", ""),
                help="Primary contact email address"
            )
        
        with col2:
            phone = st.text_input(
                "Phone",
                value=st.session_state.client_form_data.get("contact", {}).get("phone", ""),
                help="Primary contact phone number"
            )
            primary_contact = st.text_input(
                "Primary Contact Name",
                value=st.session_state.client_form_data.get("contact", {}).get("primary", ""),
                help="Name of the primary contact person"
            )
            company_size = st.selectbox(
                "Company Size",
                ["Small (<50)", "Medium (50-500)", "Large (>500)", "Enterprise (>1000)"],
                index=["Small (<50)", "Medium (50-500)", "Large (>500)", "Enterprise (>1000)"].index(st.session_state.client_form_data.get("size", "Small (<50)")) if st.session_state.client_form_data.get("size") in ["Small (<50)", "Medium (50-500)", "Large (>500)", "Enterprise (>1000)"] else 0,
                help="Approximate number of employees"
            )
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Next →", type="primary", width='stretch'):
                # Validate and save data
                data = {
                    "name": name,
                    "industry": industry,
                    "contact": {
                        "email": email,
                        "phone": phone,
                        "primary": primary_contact
                    },
                    "size": company_size
                }
                
                valid, error = validate_basic_info(data)
                if valid:
                    st.session_state.client_form_data.update(data)
                    st.session_state.onboarding_step += 1
                    st.rerun()
                else:
                    st.error(error)
    
    # Step 2: Documents
    elif current_step == 1:
        st.markdown('<h3 aria-label="Initial Documents">Initial Documents</h3>', unsafe_allow_html=True)
        st.markdown("Upload NDAs, contracts, or policies (optional)")
        
        uploaded_files = st.file_uploader(
            "Upload Documents",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            help="Upload up to 3 files, maximum 10MB each. Supported formats: PDF, DOCX"
        )
        
        if uploaded_files:
            if len(uploaded_files) > 3:
                st.error("Maximum 3 files allowed")
            else:
                # Check file sizes
                total_size = sum(f.size for f in uploaded_files)
                if total_size > 10 * 1024 * 1024:  # 10MB
                    st.error("Total file size exceeds 10MB limit")
                else:
                    file_names = [f.name for f in uploaded_files]
                    st.session_state.client_form_data["documents"] = file_names
                    
                    st.success(f"Uploaded {len(uploaded_files)} file(s)")
                    for file in uploaded_files:
                        st.write(f"📄 {file.name} ({file.size / 1024:.1f} KB)")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("← Previous", width='stretch'):
                st.session_state.onboarding_step -= 1
                st.rerun()
        with col3:
            if st.button("Next →", type="primary", width='stretch'):
                st.session_state.onboarding_step += 1
                st.rerun()
    
    # Step 3: Notes
    elif current_step == 2:
        st.markdown('<h3 aria-label="Initial Notes">Initial Notes</h3>', unsafe_allow_html=True)
        st.markdown("Add any initial notes or observations (optional)")
        
        notes = st.text_area(
            "Notes",
            value=st.session_state.client_form_data.get("notes", ""),
            max_chars=500,
            help="Maximum 500 characters",
            placeholder="Enter any initial observations, special requirements, or notes about this client..."
        )
        
        # Character counter
        char_count = len(notes)
        st.markdown(f"**Characters: {char_count}/500**")
        
        if char_count > 500:
            st.error("Character limit exceeded")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("← Previous", width='stretch'):
                st.session_state.onboarding_step -= 1
                st.rerun()
        with col3:
            if st.button("Next →", type="primary", width='stretch'):
                st.session_state.client_form_data["notes"] = notes
                st.session_state.onboarding_step += 1
                st.rerun()
    
    # Step 4: Review & Submit
    elif current_step == 3:
        st.markdown('<h3 aria-label="Review and Submit">Review & Submit</h3>', unsafe_allow_html=True)
        st.markdown("Please review the client information before submitting.")
        
        # Display summary
        with st.expander("📋 Client Information Summary", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Basic Information**")
                st.write(f"**Name:** {st.session_state.client_form_data.get('name', 'N/A')}")
                st.write(f"**Industry:** {st.session_state.client_form_data.get('industry', 'N/A')}")
                st.write(f"**Company Size:** {st.session_state.client_form_data.get('size', 'N/A')}")
            
            with col2:
                st.markdown("**Contact Information**")
                contact = st.session_state.client_form_data.get('contact', {})
                st.write(f"**Email:** {contact.get('email', 'N/A')}")
                st.write(f"**Phone:** {contact.get('phone', 'N/A')}")
                st.write(f"**Primary Contact:** {contact.get('primary', 'N/A')}")
            
            # Documents
            documents = st.session_state.client_form_data.get('documents', [])
            if documents:
                st.markdown("**Documents**")
                for doc in documents:
                    st.write(f"📄 {doc}")
            
            # Notes
            notes = st.session_state.client_form_data.get('notes', '')
            if notes:
                st.markdown("**Notes**")
                st.write(notes)
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("← Previous", width='stretch'):
                st.session_state.onboarding_step -= 1
                st.rerun()
        with col2:
            if st.button("Edit Information", width='stretch'):
                st.session_state.onboarding_step = 0
                st.rerun()
        with col3:
            # Check if we're in edit mode
            is_editing = st.session_state.get("editing_client", False)
            editing_client_id = st.session_state.get("editing_client_id", None)
            
            if is_editing:
                button_text = "✅ Update Client"
            else:
                button_text = "✅ Submit Client"
                
            if st.button(button_text, type="primary", width='stretch'):
                # Save client
                client = st.session_state.client_form_data.copy()
                
                if is_editing and editing_client_id:
                    # Update existing client
                    client["id"] = editing_client_id
                    client["updated_date"] = datetime.now().isoformat()
                    
                    # Find and update the client in the list
                    for i, existing_client in enumerate(st.session_state.clients):
                        if existing_client.get("id") == editing_client_id:
                            st.session_state.clients[i] = client
                            break
                    
                    # Save data automatically
                    if save_session_data():
                        st.success("✅ Client updated and saved successfully!")
                    else:
                        st.success("✅ Client updated successfully!")
                        st.warning("⚠️ Data could not be saved automatically. Please use the manual save option.")
                    
                    # Reset edit mode
                    st.session_state.editing_client = False
                    st.session_state.editing_client_id = None
                    
                    # Show success options
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 Edit Another Client", width='stretch'):
                            st.session_state.onboarding_step = 0
                            st.session_state.client_form_data = {}
                            st.rerun()
                    with col2:
                        if st.button("📊 Go to Assessment", width='stretch'):
                            st.session_state.selected_client = client["id"]
                            st.session_state.current_page = "Assessment Dashboard"
                            st.rerun()
                else:
                    # Create new client
                    client["id"] = str(uuid.uuid4())
                    client["created_date"] = datetime.now().isoformat()
                    
                    st.session_state.clients.append(client)
                    
                    # Save data automatically
                    if save_session_data():
                        st.success("✅ Client added and saved successfully!")
                    else:
                        st.success("✅ Client added successfully!")
                        st.warning("⚠️ Data could not be saved automatically. Please use the manual save option.")
                    
                    # Reset form
                    st.session_state.onboarding_step = 0
                    st.session_state.client_form_data = {}
                    
                    # Show success options
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 Add Another Client", width='stretch'):
                            st.rerun()
                    with col2:
                        if st.button("📊 Go to Assessment", width='stretch'):
                            st.session_state.selected_client = client["id"]
                            st.session_state.current_page = "Assessment Dashboard"
                            st.rerun()

def assessment_dashboard():
    """NIST CSF 2.0 Assessment Dashboard."""
    st.title("🛡️ Cyber Tonic - Client Portal")
    st.markdown('<h2 aria-label="NIST CSF 2.0 Assessment">NIST CSF 2.0 Assessment</h2>', unsafe_allow_html=True)
    
    # Check if clients are available
    if not st.session_state.clients:
        st.warning("No clients available. Please add a client first.")
        if st.button("➕ Add New Client"):
            st.session_state.onboarding_step = 0
            st.session_state.current_page = "Client Onboarding"
            st.rerun()
        return
    
    # Ensure a client is selected
    if not st.session_state.selected_client:
        st.session_state.selected_client = st.session_state.clients[0]["id"] if st.session_state.clients else None
    
    # Main assessment interface
    if not st.session_state.selected_client:
        st.info("Please select a client from the sidebar to begin assessment.")
        return
    
    # Load NIST CSF data with caching
    try:
        nist_data = get_cached_nist_data()
    except Exception as e:
        st.error(f"Error loading NIST CSF data: {e}")
        return
    
    # Initialize assessment data
    client_id = st.session_state.selected_client
    if client_id not in st.session_state.assessments:
        st.session_state.assessments[client_id] = {}
    
    # Assessment tabs with enhanced features
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Assessment", "⚖️ Weights", "🔍 Gap Analysis", "📁 Evidence"])
    
    with tab1:
        assessment_interface(nist_data, client_id)
    
    with tab2:
        weights_interface(client_id)
    
    with tab3:
        enhanced_gap_analysis_interface(nist_data, client_id)
    
    with tab4:
        enhanced_evidence_interface(client_id)

def assessment_interface(nist_data, client_id):
    """Main assessment interface with expandable functions and categories."""
    st.markdown("### Assessment Interface")
    
    # Progress indicator
    progress = get_assessment_progress(client_id, nist_data)
    st.progress(progress["completion_percentage"] / 100)
    st.markdown(f"**Progress: {progress['completed_subcategories']}/{progress['total_subcategories']} subcategories completed ({progress['completion_percentage']:.1f}%)**")
    
    # Assessment form
    for function in nist_data["functions"]:
        with st.expander(f"**{function['id']} - {function['name']}**", expanded=False):
            st.markdown(f"*{function['description']}*")
            
            for category in function["categories"]:
                with st.expander(f"**{category['id']} - {category['name']}**", expanded=False):
                    st.markdown(f"*{category['description']}*")
                    
                    for subcategory in category["subcategories"]:
                        subcat_id = subcategory["id"]
                        
                        # Initialize subcategory data if not exists
                        if subcat_id not in st.session_state.assessments[client_id]:
                            st.session_state.assessments[client_id][subcat_id] = {
                                "status": "Not Implemented",
                                "score": 0,
                                "notes": "",
                                "evidence": []
                            }
                        
                        st.markdown(f"**{subcat_id}**")
                        st.markdown(f"*{subcategory['description']}*")
                        
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            # Status selection
                            status = st.selectbox(
                                "Status",
                                ["Not Implemented", "Partially Implemented", "Fully Implemented", "Not Applicable"],
                                index=["Not Implemented", "Partially Implemented", "Fully Implemented", "Not Applicable"].index(st.session_state.assessments[client_id][subcat_id]["status"]),
                                key=f"status_{subcat_id}"
                            )
                            
                            # Score input
                            score = st.number_input(
                                "Score (1-10)",
                                min_value=0,
                                max_value=10,
                                value=st.session_state.assessments[client_id][subcat_id]["score"],
                                step=1,
                                key=f"score_{subcat_id}"
                            )
                            
                            # Notes
                            notes = st.text_area(
                                "Notes",
                                value=st.session_state.assessments[client_id][subcat_id]["notes"],
                                key=f"notes_{subcat_id}",
                                placeholder="Enter assessment notes, observations, or recommendations..."
                            )
                        
                        with col2:
                            # Enhanced evidence management
                            evidence_metadata = evidence_manager.render_evidence_interface(client_id, subcat_id)
                            
                            if evidence_metadata:
                                # Store enhanced evidence metadata
                                st.session_state.assessments[client_id][subcat_id]["evidence_metadata"] = evidence_metadata
                                
                                # Also store in legacy format for compatibility
                                st.session_state.assessments[client_id][subcat_id]["evidence"] = evidence_metadata["files"]
                                
                                # Store in evidence files
                                if client_id not in st.session_state.evidence_files:
                                    st.session_state.evidence_files[client_id] = {}
                                st.session_state.evidence_files[client_id][subcat_id] = evidence_metadata["files"]
                            
                            # Save button
                            if st.button("💾 Save", key=f"save_{subcat_id}"):
                                st.session_state.assessments[client_id][subcat_id].update({
                                    "status": status,
                                    "score": score,
                                    "notes": notes
                                })
                                
                                # Auto-save data
                                if save_session_data():
                                    st.success("Assessment saved and data persisted!")
                                else:
                                    st.success("Assessment saved!")
                                    st.warning("⚠️ Data could not be saved automatically.")
                        
                        st.divider()

def gap_analysis_interface(nist_data, client_id):
    """Gap analysis interface showing subcategories that need attention based on assessment criteria."""
    st.markdown("### Gap Analysis")
    
    if client_id not in st.session_state.assessments:
        st.info("No assessment data available. Please complete assessments first.")
        return
    
    # Gap analysis criteria configuration
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Gap Criteria**")
        include_not_implemented = st.checkbox("Include 'Not Implemented'", value=True)
        include_partial = st.checkbox("Include 'Partially Implemented'", value=True)
        include_low_scores = st.checkbox("Include Low Scores", value=True)
    
    with col2:
        st.markdown("**Score Threshold**")
        score_threshold = st.slider("Minimum Score", 1, 10, 5, help="Subcategories with scores below this will be flagged as gaps")
    
    with col3:
        st.markdown("**Priority Levels**")
        show_high_priority = st.checkbox("High Priority (Score < 3)", value=True)
        show_medium_priority = st.checkbox("Medium Priority (Score 3-4)", value=True)
        show_low_priority = st.checkbox("Low Priority (Score 5-6)", value=False)
    
    # Collect gap data based on criteria
    gap_data = []
    high_priority_count = 0
    medium_priority_count = 0
    low_priority_count = 0
    
    for function in nist_data["functions"]:
        for category in function["categories"]:
            for subcategory in category["subcategories"]:
                subcat_id = subcategory["id"]
                if subcat_id in st.session_state.assessments[client_id]:
                    assessment = st.session_state.assessments[client_id][subcat_id]
                    status = assessment["status"]
                    score = assessment["score"]
                    
                    # Determine if this is a gap based on criteria
                    is_gap = False
                    priority = "Low"
                    
                    # Check status-based gaps
                    if include_not_implemented and status == "Not Implemented":
                        is_gap = True
                        priority = "High"
                    elif include_partial and status == "Partially Implemented":
                        is_gap = True
                        priority = "Medium"
                    
                    # Check score-based gaps
                    if include_low_scores and score < score_threshold:
                        is_gap = True
                        if score < 3:
                            priority = "High"
                        elif score < 5:
                            priority = "Medium"
                        else:
                            priority = "Low"
                    
                    # Apply priority filters
                    if is_gap:
                        if priority == "High" and not show_high_priority:
                            continue
                        elif priority == "Medium" and not show_medium_priority:
                            continue
                        elif priority == "Low" and not show_low_priority:
                            continue
                        
                        # Count priorities
                        if priority == "High":
                            high_priority_count += 1
                        elif priority == "Medium":
                            medium_priority_count += 1
                        else:
                            low_priority_count += 1
                        
                        # Get remediation tip
                        remediation_tips = get_remediation_tips()
                        remediation = remediation_tips.get(subcat_id, "Review current implementation and identify improvement opportunities.")
                        
                        gap_data.append({
                            "Priority": priority,
                            "Function": function["name"],
                            "Category": category["name"],
                            "Subcategory ID": subcat_id,
                            "Description": subcategory["description"],
                            "Current Status": status,
                            "Current Score": score,
                            "Remediation": remediation,
                            "Notes": assessment.get("notes", "")
                        })
    
    # Display summary
    if gap_data:
        st.markdown("### Gap Summary")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Gaps", len(gap_data))
        with col2:
            st.metric("High Priority", high_priority_count, delta=None, delta_color="inverse")
        with col3:
            st.metric("Medium Priority", medium_priority_count, delta=None, delta_color="off")
        with col4:
            st.metric("Low Priority", low_priority_count, delta=None, delta_color="off")
        
        # Sort by priority and score
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        gap_data.sort(key=lambda x: (priority_order[x["Priority"]], x["Current Score"]))
        
        # Display gap data
        st.markdown("### Detailed Gap Analysis")
        df = pd.DataFrame(gap_data)
        
        # Color code the dataframe
        def highlight_priority(row):
            if row["Priority"] == "High":
                return ['background-color: #ffebee'] * len(row)
            elif row["Priority"] == "Medium":
                return ['background-color: #fff3e0'] * len(row)
            else:
                return ['background-color: #f3e5f5'] * len(row)
        
        styled_df = df.style.apply(highlight_priority, axis=1)
        st.dataframe(styled_df, width='stretch')
        
        # Export gap analysis
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Download Gap Analysis",
            data=csv,
            file_name=f"gap_analysis_{client_id}.csv",
            mime="text/csv"
        )
    else:
        st.success("🎉 No gaps found based on your current criteria!")
        st.info("Try adjusting the gap criteria above to see different results.")

def weights_interface(client_id):
    """Weights configuration interface."""
    st.markdown("### ⚖️ Assessment Weights Configuration")
    
    # Get client information
    selected_client = next((c for c in st.session_state.clients if c["id"] == client_id), None)
    if not selected_client:
        st.error("Client not found")
        return
    
    client_industry = selected_client.get("industry", "Other")
    
    # Load current weights
    current_weights = data_persistence.load_assessment_weights(client_id)
    
    # Render weights interface
    new_weights = assessment_weights.render_weights_interface(client_industry, current_weights)
    
    # Save weights
    if st.button("💾 Save Weights", key="save_weights", width='stretch'):
        if data_persistence.save_assessment_weights(client_id, new_weights):
            st.success("✅ Weights saved successfully!")
            # Update session state
            if client_id not in st.session_state.assessments:
                st.session_state.assessments[client_id] = {}
            st.session_state.assessments[client_id]["weights"] = new_weights
        else:
            st.error("❌ Failed to save weights")
    
    # Display current weights summary
    if new_weights:
        st.markdown("#### Current Weights Summary")
        weights_df = pd.DataFrame([
            {"Function": "Govern", "Weight": new_weights.get("GV", 1.0)},
            {"Function": "Identify", "Weight": new_weights.get("ID", 1.0)},
            {"Function": "Protect", "Weight": new_weights.get("PR", 1.0)},
            {"Function": "Detect", "Weight": new_weights.get("DE", 1.0)},
            {"Function": "Respond", "Weight": new_weights.get("RS", 1.0)},
            {"Function": "Recover", "Weight": new_weights.get("RC", 1.0)}
        ])
        
        # Create weights visualization
        fig = px.bar(
            weights_df,
            x="Function",
            y="Weight",
            title="Function Weights",
            color="Weight",
            color_continuous_scale="RdYlGn"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, config={'displayModeBar': False})

def enhanced_gap_analysis_interface(nist_data, client_id):
    """Enhanced gap analysis interface with weights, prioritization, and advanced visualizations."""
    st.markdown("### 🔍 Enhanced Gap Analysis Dashboard")
    
    if client_id not in st.session_state.assessments:
        st.info("No assessment data available. Please complete assessments first.")
        return
    
    # Load weights
    weights = data_persistence.load_assessment_weights(client_id)
    if not weights:
        st.warning("⚠️ No weights configured. Using default weights (1.0 for all functions).")
        weights = assessment_weights.default_function_weights
    
    # Get assessments
    assessments = st.session_state.assessments[client_id]
    
    # Analyze gaps with weights
    gap_data = gap_analyzer.analyze_gaps_with_weights(assessments, weights, nist_data)
    
    # Enhanced filtering with expanders
    with st.expander("🔧 Advanced Filters & Settings", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Priority Filter**")
            priority_filter = st.multiselect(
                "Select Priorities",
                options=["Critical", "High", "Medium", "Low"],
                default=["Critical", "High"],
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown("**Urgency Filter**")
            urgency_filter = st.multiselect(
                "Select Urgency Levels",
                options=["Immediate", "High", "Medium", "Low"],
                default=["Immediate", "High"],
                label_visibility="collapsed"
            )
            
        with col3:
            st.markdown("**Function Filter**")
            available_functions = list(set([gap["Function"] for gap in gap_data])) if gap_data else []
            function_filter = st.multiselect(
                "Select Functions",
                options=available_functions,
                default=available_functions,
                label_visibility="collapsed"
            )
    
    if gap_data:
        # Apply filters
        filtered_gap_data = [
            gap for gap in gap_data 
            if gap["Priority"] in priority_filter 
            and gap["Remediation_Urgency"] in urgency_filter
            and gap["Function"] in function_filter
        ]
        
        # Enhanced KPI Summary with pastel color coding
        st.markdown("#### 📊 Security Posture Summary")
        gap_df = pd.DataFrame(filtered_gap_data)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_gaps = len(filtered_gap_data)
            # Use pastel red for high gap counts
            delta_color = "inverse" if total_gaps > 20 else "off" if total_gaps > 10 else "normal"
            st.metric("Total Gaps", total_gaps, delta=None, delta_color=delta_color)
        
        with col2:
            critical_gaps = len(gap_df[gap_df["Priority"] == "Critical"]) if not gap_df.empty else 0
            # Use pastel red for critical gaps
            delta_color = "inverse" if critical_gaps > 5 else "off" if critical_gaps > 0 else "normal"
            st.metric("Critical", critical_gaps, delta=None, delta_color=delta_color)
        
        with col3:
            high_gaps = len(gap_df[gap_df["Priority"] == "High"]) if not gap_df.empty else 0
            # Use pastel orange for high priority gaps
            delta_color = "inverse" if high_gaps > 10 else "off" if high_gaps > 5 else "normal"
            st.metric("High Priority", high_gaps, delta=None, delta_color=delta_color)
        
        with col4:
            avg_score = gap_df["Current_Score"].mean() if not gap_df.empty else 0
            # Use pastel green for good scores, pastel red for poor scores
            delta_color = "inverse" if avg_score < 3 else "off" if avg_score < 5 else "normal"
            st.metric("Avg Score", f"{avg_score:.1f}", delta=None, delta_color=delta_color)
        
        # Calculate overall maturity score for summary report
        all_scores = [assessment.get("score", 0) for assessment in assessments.values()]
        overall_maturity = sum(all_scores) / len(all_scores) if all_scores else 0
        
        # Visualization Tabs with improved spacing
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Gap Analysis", "🎯 NIST Maturity", "💧 Remediation Impact", "📈 Trends"])
        
        with tab1:
            # Enhanced gap analysis chart with improved layout
            col1, col2 = st.columns([1, 1], gap="large")
            
            with col1:
                # Priority Distribution and Score Distribution
                fig_priority = gap_analyzer.create_priority_pie_chart(filtered_gap_data)
                st.plotly_chart(fig_priority, config={'displayModeBar': False})
                
                fig_score = gap_analyzer.create_score_histogram(filtered_gap_data)
                st.plotly_chart(fig_score, config={'displayModeBar': False})
            
            with col2:
                # Function Gaps and Remediation Urgency
                fig_function = gap_analyzer.create_function_bar_chart(filtered_gap_data)
                st.plotly_chart(fig_function, config={'displayModeBar': False})
                
                fig_urgency = gap_analyzer.create_urgency_bar_chart(filtered_gap_data)
                st.plotly_chart(fig_urgency, config={'displayModeBar': False})
        
        with tab2:
            # NIST Maturity Radar Chart
            radar_fig = gap_analyzer.create_nist_maturity_radar(assessments, nist_data)
            st.plotly_chart(radar_fig, config={'displayModeBar': False})
        
        with tab3:
            # Remediation Waterfall Chart
            waterfall_fig = gap_analyzer.create_remediation_waterfall(filtered_gap_data)
            st.plotly_chart(waterfall_fig, config={'displayModeBar': False})
        
        with tab4:
            # Trend Analysis (placeholder for now)
            st.info("📈 Trend analysis will be available once multiple assessments are completed.")
            # TODO: Implement trend analysis when assessment history is available
        
        # Detailed gap table with enhanced styling
        st.markdown("#### 📋 Detailed Gap Analysis")
        
        if not gap_df.empty:
            # Display filtered results with enhanced styling
            display_df = gap_df[["Priority", "Function", "Subcategory_ID", "Description", 
                               "Current_Score", "Weighted_Score", "Remediation_Urgency", "Notes"]].copy()
            
            # Pastel color-coded priority highlighting
            def color_by_priority(val):
                color_map = {
                    'Critical': 'background-color: #FF9999; color: black;',
                    'High': 'background-color: #FFCC99; color: black;',
                    'Medium': 'background-color: #FFFF99; color: black;',
                    'Low': 'background-color: #99FF99; color: black;'
                }
                return color_map.get(val, '')
            
            styled_df = display_df.style.map(
                color_by_priority, 
                subset=['Priority']
            ).set_properties(**{
                'text-align': 'left', 
                'padding': '10px', 
                'white-space': 'pre-wrap', 
                'font-size': '14px'
            })
            
            st.dataframe(
                styled_df,
                width='stretch',
                height=400,
                column_config={
                    "Priority": st.column_config.TextColumn("Priority", width="small"),
                    "Function": st.column_config.TextColumn("Function", width="medium"),
                    "Subcategory_ID": st.column_config.TextColumn("Subcategory", width="small"),
                    "Description": st.column_config.TextColumn("Description", width="large"),
                    "Current_Score": st.column_config.NumberColumn("Score", width="small", format="%.1f"),
                    "Weighted_Score": st.column_config.NumberColumn("Weighted", width="small", format="%.1f"),
                    "Remediation_Urgency": st.column_config.TextColumn("Urgency", width="small"),
                    "Notes": st.column_config.TextColumn("Notes", width="medium")
                }
            )
            
            # Enhanced export options
            col1, col2 = st.columns(2)
            with col1:
                csv = gap_df.to_csv(index=False)
            st.download_button(
                    "📥 Download Gap Analysis (CSV)",
                data=csv,
                file_name=f"gap_analysis_{client_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    width='stretch'
                )
            
            with col2:
                # Export summary report
                summary_report = f"""
# Gap Analysis Summary Report
**Client:** {client_id}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
- **Total Gaps Identified:** {len(filtered_gap_data)}
- **Critical Priority:** {critical_gaps}
- **High Priority:** {high_gaps}
- **Average Score:** {avg_score:.1f}
- **Overall Maturity:** {overall_maturity:.1f}

## Priority Breakdown
{chr(10).join([f"- {priority}: {len(gap_df[gap_df['Priority'] == priority])} gaps" for priority in ['Critical', 'High', 'Medium', 'Low'] if len(gap_df[gap_df['Priority'] == priority]) > 0])}

## Recommendations
1. Address all Critical priority gaps immediately
2. Focus on High priority gaps within 30 days
3. Plan Medium priority gaps for next quarter
4. Monitor Low priority gaps for future planning
"""
                st.download_button(
                    "📄 Download Summary Report",
                    data=summary_report,
                    file_name=f"gap_analysis_summary_{client_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                    width='stretch'
            )
        else:
            st.info("No gaps match the selected filters.")
    else:
        st.success("🎉 No gaps found! Your security posture looks excellent!")
        
        # Show NIST maturity radar even when no gaps
        radar_fig = gap_analyzer.create_nist_maturity_radar(assessments, nist_data)
        st.plotly_chart(radar_fig, config={'displayModeBar': False})

def enhanced_evidence_interface(client_id):
    """Enhanced evidence management interface with search and tagging."""
    st.markdown("### 📁 Enhanced Evidence Management")
    
    if client_id not in st.session_state.assessments:
        st.info("No assessment data available.")
        return
    
    # Collect evidence data with metadata
    evidence_data = {}
    for subcat_id, assessment in st.session_state.assessments[client_id].items():
        if subcat_id == "weights":  # Skip weights data
            continue
        
        if "evidence_metadata" in assessment:
            evidence_data[subcat_id] = assessment["evidence_metadata"]
        elif "evidence" in assessment and assessment["evidence"]:
            # Convert legacy format
            evidence_data[subcat_id] = {
                "files": assessment["evidence"],
                "tags": [],
                "upload_date": datetime.now().isoformat(),
                "subcategory_id": subcat_id
            }
    
    if not evidence_data:
        st.info("No evidence files uploaded yet.")
        return
    
    # Create evidence DataFrame
    evidence_df = evidence_manager.create_evidence_dataframe({client_id: evidence_data})
    
    # Render evidence search interface
    evidence_manager.render_evidence_search(evidence_df)
    
    # Evidence statistics
    st.markdown("#### Evidence Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_files = len(evidence_df)
        st.metric("Total Files", total_files)
    
    with col2:
        unique_tags = len(evidence_df["Tags"].str.split(", ").explode().unique()) if not evidence_df.empty else 0
        st.metric("Unique Tags", unique_tags)
    
    with col3:
        subcategories_with_evidence = len(evidence_df["Subcategory"].unique()) if not evidence_df.empty else 0
        st.metric("Subcategories", subcategories_with_evidence)

def evidence_interface(client_id):
    """Legacy evidence management interface (kept for compatibility)."""
    st.markdown("### Evidence Management")
    
    if client_id not in st.session_state.evidence_files or not st.session_state.evidence_files[client_id]:
        st.info("No evidence files uploaded yet.")
        return
    
    # Collect evidence data
    evidence_data = []
    for subcat_id, files in st.session_state.evidence_files[client_id].items():
        for file_name in files:
            evidence_data.append({
                "File Name": file_name,
                "Subcategory ID": subcat_id,
                "Upload Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    if evidence_data:
        df = pd.DataFrame(evidence_data)
        st.dataframe(df, width='stretch')
        
        # Search functionality
        search_term = st.text_input("Search files or subcategories", placeholder="Enter search term...")
        if search_term:
            filtered_df = df[
                df["File Name"].str.contains(search_term, case=False, na=False) |
                df["Subcategory ID"].str.contains(search_term, case=False, na=False)
            ]
            st.dataframe(filtered_df, width='stretch')
        
        # Export evidence list
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Download Evidence List",
            data=csv,
            file_name=f"evidence_list_{client_id}.csv",
            mime="text/csv"
        )

def main():
    """Main application function."""
    # Load CSS and initialize session state
    load_css()
    initialize_session_state()
    
    # Auto-save data if changes detected
    auto_save_data()
    
    # Enhanced Sidebar
    with st.sidebar:
        # Determine current page
        current_page = st.session_state.get("current_page", "Assessment Dashboard")
        render_enhanced_sidebar(current_page)
    
    # Page navigation logic
    page = st.session_state.get("current_page", "Assessment Dashboard")
    
    # Render selected page
    if page == "Client Onboarding":
        client_onboarding()
    elif page == "Assessment Dashboard":
        assessment_dashboard()

if __name__ == "__main__":
    main()
