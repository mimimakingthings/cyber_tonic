import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from standards_loader import StandardsLoader

# Page configuration
st.set_page_config(
    page_title="Standards Navigator",
    page_icon="🔍",
    layout="wide"
)

# Initialize standards loader
@st.cache_resource
def get_standards_loader():
    return StandardsLoader()

standards_loader = get_standards_loader()

# Load available standards
@st.cache_data
def get_available_standards():
    try:
        index = standards_loader.load_index()
        return {std_id: std_info for std_id, std_info in index["standards"].items()}
    except Exception as e:
        st.error(f"Error loading standards index: {e}")
        return {}

def main():
    st.title("🔍 Standards Navigator")
    
    # Simple navigation
    if st.button("🏠 Back to Dashboard"):
        st.markdown("**[🛡️ Main Dashboard](http://localhost:8501)**")
    
    st.markdown("**Your comprehensive guide to cybersecurity standards**")
    
    # Get available standards
    available_standards = get_available_standards()
    
    if not available_standards:
        st.error("No standards are available. Please check your standards data configuration.")
        return
    
    # Standard selection dropdown
    st.markdown("## 📋 Select a Standard")
    standard_options = {std_id: f"{std_info['name']} ({std_info.get('version', 'N/A')})" 
                       for std_id, std_info in available_standards.items()}
    
    selected_standard_id = st.selectbox(
        "Choose a cybersecurity standard to explore:",
        options=list(standard_options.keys()),
        format_func=lambda x: standard_options[x],
        help="Select a standard from the dropdown to view its details and controls"
    )
    
    if not selected_standard_id:
        st.info("Please select a standard from the dropdown above to get started.")
        return
    
    # Load the selected standard
    try:
        selected_standard_data = standards_loader.load_standard(selected_standard_id)
        selected_standard_info = available_standards[selected_standard_id]
    except Exception as e:
        st.error(f"Error loading standard {selected_standard_id}: {e}")
        return
    
    # Display standard overview
    st.markdown("## 📊 Standard Overview")
    
    # Header with title and basic info
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"### {selected_standard_info['name']}")
        st.markdown(f"**Version:** {selected_standard_info.get('version', 'N/A')}")
        st.markdown(f"**Type:** {selected_standard_info.get('type', 'N/A')}")
        st.markdown(f"**Region:** {selected_standard_info.get('region', 'N/A')}")
        st.markdown(f"**Status:** {selected_standard_info.get('status', 'N/A')}")
    
    with col2:
        # Official documentation link
        if selected_standard_info.get('official_url'):
            st.markdown("### 📚 Official Resources")
            st.markdown(f"[🌐 Official Website]({selected_standard_info['official_url']})")
            st.markdown(f"[📄 Framework Documentation]({selected_standard_info['official_url']}/framework)")
            st.markdown(f"[📋 Implementation Guide]({selected_standard_info['official_url']}/implementation)")
    
    # Description
    st.markdown("### 📝 Description")
    st.markdown(selected_standard_info.get('description', 'N/A'))
    
    # Calculate real-time statistics
    functions = selected_standard_data.get('functions', [])
    total_functions = len(functions)
    total_categories = sum(len(func.get('categories', [])) for func in functions)
    total_subcategories = sum(
        len(cat.get('subcategories', [])) 
        for func in functions 
        for cat in func.get('categories', [])
    )
    
    # Statistics section
    st.markdown("### 📈 Framework Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Functions",
            value=total_functions,
            help="High-level cybersecurity outcomes"
        )
    with col2:
        st.metric(
            label="Categories", 
            value=total_categories,
            help="Groups of cybersecurity outcomes"
        )
    with col3:
        st.metric(
            label="Subcategories",
            value=total_subcategories,
            help="Specific cybersecurity outcomes"
        )
    with col4:
        st.metric(
            label="Last Updated",
            value=selected_standard_info.get('last_updated', 'N/A'),
            help="Framework version date"
        )
    
    # Additional information
    st.markdown("### ℹ️ Additional Information")
    
    # Function breakdown
    if functions:
        st.markdown("**Function Breakdown:**")
        for func in functions:
            func_id = func.get('id', '')
            func_name = func.get('name', '')
            func_categories = len(func.get('categories', []))
            func_subcategories = sum(len(cat.get('subcategories', [])) for cat in func.get('categories', []))
            st.markdown(f"- **{func_id} - {func_name}**: {func_categories} categories, {func_subcategories} subcategories")
    
    # Key features and benefits
    st.markdown("### 🎯 Key Features")
    key_features = [
        "**Risk-based approach** - Focuses on managing cybersecurity risks",
        "**Flexible implementation** - Adaptable to any organization size or sector", 
        "**Outcome-focused** - Emphasizes cybersecurity outcomes over specific technologies",
        "**Continuous improvement** - Supports ongoing cybersecurity program development",
        "**Stakeholder communication** - Helps communicate cybersecurity efforts to stakeholders"
    ]
    for feature in key_features:
        st.markdown(f"- {feature}")
    
    # Implementation guidance
    st.markdown("### 🚀 Getting Started")
    implementation_steps = [
        "**Assess current state** - Understand your organization's cybersecurity posture",
        "**Define target state** - Establish cybersecurity goals and objectives", 
        "**Identify gaps** - Compare current and target states to find improvement opportunities",
        "**Prioritize actions** - Focus on high-impact, high-priority cybersecurity improvements",
        "**Implement improvements** - Execute prioritized cybersecurity enhancements",
        "**Monitor progress** - Continuously assess and improve cybersecurity outcomes"
    ]
    for step in implementation_steps:
        st.markdown(f"- {step}")
    
    # Comparison section (useful for future standards)
    if len(available_standards) > 1:
        st.markdown("### ⚖️ Standards Comparison")
        st.info("💡 **Tip**: When you have multiple standards available, you'll be able to compare their scope, coverage, and complexity here.")
    
    # Technical details
    st.markdown("### 🔧 Technical Details")
    tech_details = [
        f"**Framework ID**: {selected_standard_id}",
        f"**Data Format**: JSON",
        f"**Schema Version**: {selected_standard_info.get('version', 'N/A')}",
        f"**Index Version**: {standards_loader.load_index().get('version', 'N/A')}",
        f"**Last Index Update**: {standards_loader.load_index().get('last_updated', 'N/A')}"
    ]
    for detail in tech_details:
        st.markdown(f"- {detail}")
    
    # Search functionality for the selected standard
    st.markdown("## 🔍 Search Controls")
    search_term = st.text_input("Search controls:", placeholder="Enter keywords...", key="search_input")
    
    if search_term:
        # Perform manual search since the standards_loader expects different data structure
        search_results = []
        
        # Search through functions, categories, and subcategories
        for func in selected_standard_data.get('functions', []):
            for cat in func.get('categories', []):
                for subcat in cat.get('subcategories', []):
                    searchable_text = f"{subcat.get('id', '')} {subcat.get('description', '')}".lower()
                    if search_term.lower() in searchable_text:
                        search_results.append({
                            'function': func.get('name', func.get('id', '')),
                            'category': cat.get('name', cat.get('id', '')),
                            'subcategory': subcat
                        })
        
        if search_results:
            st.markdown(f"### 📋 Found {len(search_results)} results")
            for result in search_results:
                subcat = result['subcategory']
                with st.expander(f"**{subcat.get('id', '')}** - {subcat.get('description', '')[:100]}..."):
                    st.markdown(f"**Function:** {result['function']}")
                    st.markdown(f"**Category:** {result['category']}")
                    st.markdown(f"**Description:** {subcat.get('description', '')}")
                    if subcat.get('examples'):
                        st.markdown(f"**Examples:** {subcat.get('examples', '')}")
                    if subcat.get('use_cases'):
                        st.markdown(f"**Use Cases:** {subcat.get('use_cases', '')}")
                    if subcat.get('tech_recommendations'):
                        st.markdown("**Technical Recommendations:**")
                        for rec in subcat.get('tech_recommendations', []):
                            st.markdown(f"- {rec}")
        else:
            st.warning("No results found.")
    
    # Display standard structure
    st.markdown("## 🏗️ Standard Structure")
        
        # Function selection
    functions = selected_standard_data.get('functions', [])
    if functions:
        # Create function options for multiselect
        function_options = {func.get('id', ''): f"{func.get('id', '')} - {func.get('name', '')}" 
                           for func in functions}
        selected_function_ids = st.multiselect(
            "Select functions to display:", 
            options=list(function_options.keys()),
            format_func=lambda x: function_options[x],
            default=list(function_options.keys()),
            help="Choose which functions to display in detail"
        )
        
        # Display selected functions
        for func in functions:
            func_id = func.get('id', '')
            if func_id in selected_function_ids:
                st.markdown(f"#### {func_id} - {func.get('name', func_id)}")
                st.markdown(func.get('description', ''))
                
                # Display categories and subcategories
                categories = func.get('categories', [])
                for cat in categories:
                    cat_id = cat.get('id', '')
                    st.markdown(f"**{cat_id} - {cat.get('name', cat_id)}**")
                    st.markdown(f"*{cat.get('description', '')}*")
                    
                    # Display subcategories
                    subcategories = cat.get('subcategories', [])
                    for subcat in subcategories:
                        subcat_id = subcat.get('id', '')
                        subcat_desc = subcat.get('description', '')
                        with st.expander(f"**{subcat_id}** - {subcat_desc[:100]}..."):
                            st.markdown(f"**Description:** {subcat_desc}")
                            if subcat.get('examples'):
                                st.markdown(f"**Examples:** {subcat.get('examples', '')}")
                            if subcat.get('use_cases'):
                                st.markdown(f"**Use Cases:** {subcat.get('use_cases', '')}")
                            if subcat.get('tech_recommendations'):
                                st.markdown("**Technical Recommendations:**")
                                for rec in subcat.get('tech_recommendations', []):
                                    st.markdown(f"- {rec}")
    else:
        st.warning("No functions found in this standard.")

if __name__ == "__main__":
    main()
