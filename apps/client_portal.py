import streamlit as st
import pandas as pd
import json
import random
from datetime import datetime
from fpdf import FPDF
import io
import plotly.express as px
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from standards_loader import load_all_standards, search_controls

# Page configuration
st.set_page_config(
    page_title="Client Portal",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .client-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
    .score-high {
        color: #28a745;
        font-weight: bold;
    }
    .score-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .score-low {
        color: #dc3545;
        font-weight: bold;
    }
    .risk-high {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.5rem;
        border-radius: 6px;
        border-left: 4px solid #dc3545;
    }
    .risk-medium {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.5rem;
        border-radius: 6px;
        border-left: 4px solid #ffc107;
    }
    .risk-low {
        background-color: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 6px;
        border-left: 4px solid #28a745;
    }
    .nav-button {
        background-color: #1f77b4;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        text-decoration: none;
        margin: 0.5rem;
        display: inline-block;
    }
    .nav-button:hover {
        background-color: #155a8a;
        color: white;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for client data
if 'clients' not in st.session_state:
    st.session_state.clients = {}
if 'current_client' not in st.session_state:
    st.session_state.current_client = None
if 'client_evaluations' not in st.session_state:
    st.session_state.client_evaluations = {}

# Load standards data from external database
@st.cache_data
def load_standards_data():
    """Load all standards data from the external database."""
    try:
        return load_all_standards()
    except Exception as e:
        st.error(f"Error loading standards data: {e}")
        return {}

# Get standards data
standards_data = load_standards_data()

class ClientPDFGenerator(FPDF):
    def __init__(self):
        super().__init__()
        self.add_page()
        self.set_font("Arial", size=12)
    
    def header(self):
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Client Security Posture Report", 0, 1, "C")
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")
    
    def add_client_section(self, title, content):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1)
        self.set_font("Arial", size=10)
        self.cell(0, 8, content, 0, 1)
        self.ln(5)

def generate_client_pdf(client_data, evaluation_data):
    """Generate PDF report for client evaluation"""
    pdf = ClientPDFGenerator()
    
    # Client details
    pdf.add_client_section("Client Information", 
                          f"Name: {client_data['name']}\n"
                          f"Industry: {client_data['industry']}\n"
                          f"Regions: {client_data['regions']}\n"
                          f"Size: {client_data['size']}\n"
                          f"Notes: {client_data['notes']}")
    
    # Overall score
    overall_score = evaluation_data.get('overall_score', 0)
    pdf.add_client_section("Overall Security Posture", f"Score: {overall_score:.1f}/5.0")
    
    # Function scores
    pdf.add_client_section("Function-Level Scores", "")
    for func_name, score in evaluation_data.get('function_scores', {}).items():
        pdf.cell(0, 8, f"{func_name}: {score:.1f}/5.0", 0, 1)
    
    # Gaps
    gaps = evaluation_data.get('gaps', [])
    if gaps:
        pdf.add_client_section("Identified Gaps", "")
        for gap in gaps[:10]:  # Limit to first 10 gaps
            pdf.cell(0, 8, f"• {gap}", 0, 1)
    
    # Recommendations
    recommendations = evaluation_data.get('recommendations', [])
    if recommendations:
        pdf.add_client_section("Recommendations", "")
        for rec in recommendations[:10]:  # Limit to first 10 recommendations
            pdf.cell(0, 8, f"• {rec}", 0, 1)
    
    return pdf.output(dest='S').encode('latin-1')

# Client Portal Functions
def display_client_form():
    """Display the client details form"""
    st.markdown("### 📋 Client Details")
    
    with st.form("client_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            client_name = st.text_input("Client Name", value=st.session_state.current_client.get('name', '') if st.session_state.current_client else '')
            industry = st.selectbox("Industry", 
                                  ["Select...", "Finance", "Healthcare", "Technology", "Manufacturing", 
                                   "Retail", "Education", "Government", "Energy", "Other"],
                                  index=0 if not st.session_state.current_client else 
                                  ["Select...", "Finance", "Healthcare", "Technology", "Manufacturing", 
                                   "Retail", "Education", "Government", "Energy", "Other"].index(st.session_state.current_client.get('industry', 'Select...')))
            size = st.selectbox("Organization Size", 
                              ["Select...", "Small (<100 employees)", "Medium (100-1000 employees)", "Large (>1000 employees)"],
                              index=0 if not st.session_state.current_client else 
                              ["Select...", "Small (<100 employees)", "Medium (100-1000 employees)", "Large (>1000 employees)"].index(st.session_state.current_client.get('size', 'Select...')))
        
        with col2:
            regions = st.multiselect("Operating Regions", 
                                   ["EU", "USA", "UK", "APAC", "Other"],
                                   default=st.session_state.current_client.get('regions', []) if st.session_state.current_client else [])
            notes = st.text_area("Custom Notes", 
                               value=st.session_state.current_client.get('notes', '') if st.session_state.current_client else '',
                               height=100)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            save_client = st.form_submit_button("💾 Save Client", type="primary")
        with col2:
            simulate_client = st.form_submit_button("🎲 Simulate Client")
        with col3:
            clear_form = st.form_submit_button("🗑️ Clear Form")
        
        if save_client:
            if client_name and industry != "Select..." and size != "Select...":
                client_id = client_name.lower().replace(' ', '_')
                st.session_state.clients[client_id] = {
                    'name': client_name,
                    'industry': industry,
                    'regions': regions,
                    'size': size,
                    'notes': notes,
                    'created': datetime.now().isoformat()
                }
                st.session_state.current_client = st.session_state.clients[client_id]
                st.success(f"Client '{client_name}' saved successfully!")
                st.rerun()
            else:
                st.error("Please fill in all required fields (Name, Industry, Size)")
        
        if simulate_client:
            simulate_client_data()
            st.rerun()
        
        if clear_form:
            st.session_state.current_client = None
            st.rerun()

def simulate_client_data():
    """Simulate client data for testing"""
    industries = ["Finance", "Healthcare", "Technology", "Manufacturing", "Retail"]
    sizes = ["Small (<100 employees)", "Medium (100-1000 employees)", "Large (>1000 employees)"]
    regions_options = [["EU"], ["USA"], ["UK"], ["EU", "USA"], ["EU", "UK"], ["USA", "UK"]]
    
    simulated_client = {
        'name': f"Demo Client {random.randint(1000, 9999)}",
        'industry': random.choice(industries),
        'regions': random.choice(regions_options),
        'size': random.choice(sizes),
        'notes': f"Simulated {random.choice(industries)} client for testing purposes. This is a demo client with mixed security posture.",
        'created': datetime.now().isoformat()
    }
    
    client_id = simulated_client['name'].lower().replace(' ', '_')
    st.session_state.clients[client_id] = simulated_client
    st.session_state.current_client = simulated_client
    
    # Generate simulated evaluation
    generate_simulated_evaluation(client_id)

def generate_simulated_evaluation(client_id):
    """Generate simulated security posture evaluation"""
    if "NIST_CSF_2.0" not in standards_data:
        return
    
    nist_data = standards_data["NIST_CSF_2.0"]
    evaluation = {}
    function_scores = {}
    gaps = []
    recommendations = []
    
    for func_name, func_data in nist_data['functions'].items():
        subcategory_scores = {}
        for subcat_id in func_data['subcategories'].keys():
            # Generate random scores with some bias toward lower scores for gaps
            score = random.uniform(1.5, 4.5)
            subcategory_scores[subcat_id] = round(score, 1)
            
            if score < 3.0:
                gaps.append(f"{subcat_id}: {func_data['subcategories'][subcat_id]['description'][:100]}...")
        
        # Calculate function average
        function_scores[func_name] = round(sum(subcategory_scores.values()) / len(subcategory_scores), 1)
        evaluation[func_name] = subcategory_scores
    
    # Generate recommendations based on gaps
    if gaps:
        recommendations = [
            "Implement comprehensive risk assessment framework",
            "Establish incident response procedures",
            "Deploy security monitoring tools",
            "Conduct regular security awareness training",
            "Implement data backup and recovery procedures"
        ]
    
    overall_score = round(sum(function_scores.values()) / len(function_scores), 1)
    
    st.session_state.client_evaluations[client_id] = {
        'overall_score': overall_score,
        'function_scores': function_scores,
        'subcategory_scores': evaluation,
        'gaps': gaps,
        'recommendations': recommendations,
        'evaluated_date': datetime.now().isoformat()
    }

def display_security_evaluation():
    """Display security posture evaluation interface"""
    if not st.session_state.current_client:
        st.info("Please create or select a client first.")
        return
    
    st.markdown("### 🔒 Security Posture Evaluation")
    
    # Standard selection
    available_standards = ["NIST_CSF_2.0"]  # Start with NIST CSF 2.0
    selected_standard = st.selectbox("Select Standard for Evaluation", available_standards)
    
    if selected_standard not in standards_data:
        st.error(f"Standard '{selected_standard}' not available.")
        return
    
    standard_data = standards_data[selected_standard]
    client_id = st.session_state.current_client['name'].lower().replace(' ', '_')
    
    # Check if evaluation exists
    if client_id not in st.session_state.client_evaluations:
        st.session_state.client_evaluations[client_id] = {
            'overall_score': 0,
            'function_scores': {},
            'subcategory_scores': {},
            'gaps': [],
            'recommendations': [],
            'evaluated_date': datetime.now().isoformat()
        }
    
    evaluation = st.session_state.client_evaluations[client_id]
    
    # Evaluation interface
    st.markdown("#### 📊 Maturity Assessment")
    st.markdown("Rate each subcategory on a scale of 0-5 (0=Not implemented, 5=Fully mature)")
    
    updated_scores = {}
    function_totals = {}
    function_counts = {}
    
    for func_name, func_data in standard_data['functions'].items():
        st.markdown(f"##### {func_name}")
        st.markdown(f"*{func_data['description']}*")
        
        function_totals[func_name] = 0
        function_counts[func_name] = 0
        
        for subcat_id, subcat_data in func_data['subcategories'].items():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{subcat_id}**")
                st.markdown(f"*{subcat_data['description'][:150]}...*")
            
            with col2:
                current_score = evaluation.get('subcategory_scores', {}).get(func_name, {}).get(subcat_id, 0)
                score = st.slider(
                    "Score",
                    min_value=0.0,
                    max_value=5.0,
                    value=current_score,
                    step=0.1,
                    key=f"{client_id}_{func_name}_{subcat_id}"
                )
                updated_scores.setdefault(func_name, {})[subcat_id] = score
                function_totals[func_name] += score
                function_counts[func_name] += 1
    
    # Calculate function scores
    for func_name in function_totals:
        if function_counts[func_name] > 0:
            function_totals[func_name] = round(function_totals[func_name] / function_counts[func_name], 1)
    
    # Update evaluation
    evaluation['subcategory_scores'] = updated_scores
    evaluation['function_scores'] = function_totals
    evaluation['overall_score'] = round(sum(function_totals.values()) / len(function_totals), 1)
    
    # Identify gaps
    gaps = []
    for func_name, subcat_scores in updated_scores.items():
        for subcat_id, score in subcat_scores.items():
            if score < 3.0:
                subcat_desc = standard_data['functions'][func_name]['subcategories'][subcat_id]['description']
                gaps.append(f"{subcat_id}: {subcat_desc[:100]}...")
    
    evaluation['gaps'] = gaps
    
    # Generate recommendations
    recommendations = []
    if evaluation['overall_score'] < 3.0:
        recommendations.extend([
            "Implement comprehensive cybersecurity framework",
            "Establish governance and risk management processes",
            "Deploy foundational security controls"
        ])
    
    low_functions = [func for func, score in function_totals.items() if score < 3.0]
    if low_functions:
        recommendations.append(f"Focus on improving {', '.join(low_functions)} functions")
    
    evaluation['recommendations'] = recommendations
    evaluation['evaluated_date'] = datetime.now().isoformat()
    
    # Save button
    if st.button("💾 Save Evaluation"):
        st.session_state.client_evaluations[client_id] = evaluation
        st.success("Evaluation saved successfully!")

def display_evaluation_results():
    """Display evaluation results and visualizations"""
    if not st.session_state.current_client:
        return
    
    client_id = st.session_state.current_client['name'].lower().replace(' ', '_')
    
    if client_id not in st.session_state.client_evaluations:
        st.info("No evaluation data available. Please complete the security posture evaluation.")
        return
    
    evaluation = st.session_state.client_evaluations[client_id]
    
    st.markdown("### 📈 Evaluation Results")
    
    # Overall score
    col1, col2, col3 = st.columns(3)
    with col1:
        overall_score = evaluation.get('overall_score', 0)
        score_color = "score-high" if overall_score >= 4.0 else "score-medium" if overall_score >= 3.0 else "score-low"
        st.markdown(f'<div class="client-card"><h3>Overall Score</h3><p class="{score_color}">{overall_score:.1f}/5.0</p></div>', unsafe_allow_html=True)
    
    with col2:
        gaps_count = len(evaluation.get('gaps', []))
        risk_level = "risk-low" if gaps_count < 5 else "risk-medium" if gaps_count < 15 else "risk-high"
        st.markdown(f'<div class="client-card"><h3>Identified Gaps</h3><p class="{risk_level}">{gaps_count} gaps</p></div>', unsafe_allow_html=True)
    
    with col3:
        recommendations_count = len(evaluation.get('recommendations', []))
        st.markdown(f'<div class="client-card"><h3>Recommendations</h3><p>{recommendations_count} recommendations</p></div>', unsafe_allow_html=True)
    
    # Function-level visualization
    st.markdown("#### 📊 Function-Level Scores")
    function_scores = evaluation.get('function_scores', {})
    
    if function_scores:
        # Create bar chart
        fig = px.bar(
            x=list(function_scores.keys()),
            y=list(function_scores.values()),
            title="Security Posture by Function",
            labels={'x': 'Function', 'y': 'Score (0-5)'},
            color=list(function_scores.values()),
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(height=400, yaxis_range=[0, 5])
        st.plotly_chart(fig, use_container_width=True)
        
        # Function details
        st.markdown("##### Function Details")
        for func_name, score in function_scores.items():
            score_class = "score-high" if score >= 4.0 else "score-medium" if score >= 3.0 else "score-low"
            st.markdown(f"**{func_name}**: <span class='{score_class}'>{score:.1f}/5.0</span>", unsafe_allow_html=True)
    
    # Gaps and recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⚠️ Identified Gaps")
        gaps = evaluation.get('gaps', [])
        if gaps:
            for i, gap in enumerate(gaps[:10]):  # Show first 10 gaps
                st.markdown(f"{i+1}. {gap}")
            if len(gaps) > 10:
                st.info(f"... and {len(gaps) - 10} more gaps")
        else:
            st.success("No significant gaps identified!")
    
    with col2:
        st.markdown("#### 💡 Recommendations")
        recommendations = evaluation.get('recommendations', [])
        if recommendations:
            for i, rec in enumerate(recommendations):
                st.markdown(f"{i+1}. {rec}")
        else:
            st.info("No specific recommendations at this time.")

def display_client_management():
    """Display client management interface"""
    st.markdown("### 👥 Client Management")
    
    # Client selection
    if st.session_state.clients:
        client_options = ["Select a client..."] + list(st.session_state.clients.keys())
        selected_client_id = st.selectbox("Select Client", client_options)
        
        if selected_client_id != "Select a client...":
            st.session_state.current_client = st.session_state.clients[selected_client_id]
            
            # Client actions
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📊 View Evaluation"):
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete Client"):
                    del st.session_state.clients[selected_client_id]
                    if selected_client_id in st.session_state.client_evaluations:
                        del st.session_state.client_evaluations[selected_client_id]
                    st.session_state.current_client = None
                    st.success("Client deleted successfully!")
                    st.rerun()
            with col3:
                if st.button("📥 Export Client Data"):
                    export_client_data(selected_client_id)
    else:
        st.info("No clients created yet. Use the form above to create your first client.")
    
    # Import/Export functionality
    st.markdown("#### 📁 Data Management")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Export All Data**")
        if st.button("📥 Export All Clients"):
            export_all_clients()
    
    with col2:
        st.markdown("**Import Data**")
        uploaded_file = st.file_uploader("Upload JSON file", type=['json'])
        if uploaded_file and st.button("📤 Import Clients"):
            import_clients(uploaded_file)

def export_client_data(client_id):
    """Export individual client data"""
    client_data = st.session_state.clients.get(client_id, {})
    evaluation_data = st.session_state.client_evaluations.get(client_id, {})
    
    export_data = {
        'client': client_data,
        'evaluation': evaluation_data,
        'export_date': datetime.now().isoformat()
    }
    
    json_str = json.dumps(export_data, indent=2)
    
    st.download_button(
        label="📥 Download Client Data (JSON)",
        data=json_str,
        file_name=f"client_{client_id}_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )

def export_all_clients():
    """Export all client data"""
    export_data = {
        'clients': st.session_state.clients,
        'evaluations': st.session_state.client_evaluations,
        'export_date': datetime.now().isoformat()
    }
    
    json_str = json.dumps(export_data, indent=2)
    
    st.download_button(
        label="📥 Download All Client Data (JSON)",
        data=json_str,
        file_name=f"all_clients_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )

def import_clients(uploaded_file):
    """Import client data from JSON file"""
    try:
        data = json.load(uploaded_file)
        
        if 'clients' in data:
            st.session_state.clients.update(data['clients'])
        if 'evaluations' in data:
            st.session_state.client_evaluations.update(data['evaluations'])
        
        st.success(f"Successfully imported {len(data.get('clients', {}))} clients!")
        st.rerun()
    except Exception as e:
        st.error(f"Error importing data: {str(e)}")

def generate_client_report():
    """Generate and display client report"""
    if not st.session_state.current_client:
        st.info("Please select a client first.")
        return
    
    client_id = st.session_state.current_client['name'].lower().replace(' ', '_')
    client_data = st.session_state.current_client
    evaluation_data = st.session_state.client_evaluations.get(client_id, {})
    
    st.markdown("### 📋 Current Profile Report")
    
    # Report content
    report_content = f"""
# Client Security Posture Report

## Client Information
- **Name**: {client_data['name']}
- **Industry**: {client_data['industry']}
- **Operating Regions**: {', '.join(client_data['regions'])}
- **Organization Size**: {client_data['size']}
- **Notes**: {client_data['notes']}
- **Report Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Security Posture Summary
- **Overall Score**: {evaluation_data.get('overall_score', 0):.1f}/5.0
- **Identified Gaps**: {len(evaluation_data.get('gaps', []))}
- **Recommendations**: {len(evaluation_data.get('recommendations', []))}

## Function-Level Assessment
"""
    
    # Add function scores
    for func_name, score in evaluation_data.get('function_scores', {}).items():
        report_content += f"- **{func_name}**: {score:.1f}/5.0\n"
    
    # Add gaps
    gaps = evaluation_data.get('gaps', [])
    if gaps:
        report_content += "\n## Identified Gaps\n"
        for i, gap in enumerate(gaps[:15], 1):  # Limit to first 15 gaps
            report_content += f"{i}. {gap}\n"
    
    # Add recommendations
    recommendations = evaluation_data.get('recommendations', [])
    if recommendations:
        report_content += "\n## Recommendations\n"
        for i, rec in enumerate(recommendations, 1):
            report_content += f"{i}. {rec}\n"
    
    # Display report
    st.markdown(report_content)
    
    # Export options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Export as Markdown"):
            st.download_button(
                label="Download Markdown Report",
                data=report_content,
                file_name=f"client_report_{client_id}_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )
    
    with col2:
        if st.button("📥 Export as PDF"):
            try:
                pdf_data = generate_client_pdf(client_data, evaluation_data)
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_data,
                    file_name=f"client_report_{client_id}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
    
    with col3:
        if st.button("📊 Export as CSV"):
            export_evaluation_csv(client_id, evaluation_data)

def export_evaluation_csv(client_id, evaluation_data):
    """Export evaluation data as CSV"""
    data = []
    
    for func_name, subcat_scores in evaluation_data.get('subcategory_scores', {}).items():
        for subcat_id, score in subcat_scores.items():
            data.append({
                'Client': st.session_state.current_client['name'],
                'Function': func_name,
                'Subcategory': subcat_id,
                'Score': score,
                'Status': 'Gap' if score < 3.0 else 'Adequate' if score < 4.0 else 'Strong'
            })
    
    if data:
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="📥 Download Evaluation CSV",
            data=csv,
            file_name=f"evaluation_{client_id}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

def main():
    # Header with navigation
    st.markdown('<h1 class="main-header">🏢 Client Portal</h1>', unsafe_allow_html=True)
    
    # Navigation back to home
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin: 1rem 0;">
            <a href="main.py" class="nav-button">🏠 Back to Home</a>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("**Manage client details and evaluate their security posture against cybersecurity standards.**")
    
    # Client portal tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Client Details", "🔒 Security Evaluation", "📊 Results & Reports", "👥 Client Management"])
    
    with tab1:
        display_client_form()
    
    with tab2:
        display_security_evaluation()
    
    with tab3:
        display_evaluation_results()
        st.markdown("---")
        generate_client_report()
    
    with tab4:
        display_client_management()

if __name__ == "__main__":
    main()