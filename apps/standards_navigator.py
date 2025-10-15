import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from standards_loader import load_all_standards, search_controls

# Page configuration
st.set_page_config(
    page_title="Standards Navigator",
    page_icon="🔍",
    layout="wide"
)

# Load standards data
@st.cache_data
def load_standards_data():
    try:
        return load_all_standards()
    except Exception as e:
        st.error(f"Error loading standards data: {e}")
        return {}

standards_data = load_standards_data()

def main():
    st.title("🔍 Standards Navigator")
    
    # Navigation back to home
    if st.button("🏠 Back to Home"):
        st.info("Return to main.py to access the home page")
    
    st.markdown("**Your comprehensive guide to cybersecurity standards**")
    
    # Search functionality
    st.markdown("## 🔍 Search NIST CSF 2.0")
    search_term = st.text_input("Search controls:", placeholder="Enter keywords...")
    
    if search_term:
        try:
            results = search_controls(search_term, ["NIST_CSF_2.0"])
            if results:
                for standard_name, standard_results in results.items():
                    st.markdown(f"### 📋 {standard_name}")
                    for func_name, func_results in standard_results.items():
                        st.markdown(f"#### {func_name}")
                        for control_id, control_data in func_results.items():
                            with st.expander(f"**{control_id}** - {control_data['description'][:100]}..."):
                                st.markdown(f"**Description:** {control_data['description']}")
                                st.markdown(f"**Examples:** {control_data['examples']}")
                                st.markdown(f"**Use Cases:** {control_data['use_cases']}")
            else:
                st.warning("No results found.")
        except Exception as e:
            st.error(f"Search error: {e}")
    
    # Standards overview
    st.markdown("## 📊 Available Standards")
    
    if "NIST_CSF_2.0" in standards_data:
        nist_data = standards_data["NIST_CSF_2.0"]
        st.markdown("### 🏛️ NIST Cybersecurity Framework 2.0")
        st.markdown(nist_data.get('overview', 'NIST CSF 2.0 framework'))
        
        # Function selection
        function_names = list(nist_data['functions'].keys())
        selected_functions = st.multiselect("Select functions:", function_names, default=function_names)
        
        # Display selected functions
        for func_name in selected_functions:
            if func_name in nist_data['functions']:
                func_data = nist_data['functions'][func_name]
                st.markdown(f"#### {func_name}")
                st.markdown(func_data['description'])
                
                # Display subcategories
                for subcat_id, subcat_data in func_data['subcategories'].items():
                    with st.expander(f"**{subcat_id}** - {subcat_data['description'][:100]}..."):
                        st.markdown(f"**Description:** {subcat_data['description']}")
                        st.markdown(f"**Examples:** {subcat_data['examples']}")
                        st.markdown(f"**Use Cases:** {subcat_data['use_cases']}")
                        st.markdown(f"**Regional Relevance:** {', '.join(subcat_data['regional_relevance'])}")
                        st.markdown("**Tech Recommendations:**")
                        for tech in subcat_data['tech_recommendations']:
                            st.markdown(f"• {tech}")

if __name__ == "__main__":
    main()
