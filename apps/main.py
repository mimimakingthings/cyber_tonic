import streamlit as st
import subprocess
import sys
import platform
import time
import webbrowser
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="TCP Cybersecurity Compliance Hub",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .app-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin: 1rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .app-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.2);
    }
    .app-title {
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .app-description {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-bottom: 1.5rem;
    }
    .launch-button {
        background: rgba(255,255,255,0.2);
        border: 2px solid rgba(255,255,255,0.3);
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .launch-button:hover {
        background: rgba(255,255,255,0.3);
        border-color: rgba(255,255,255,0.5);
        transform: scale(1.05);
    }
    .welcome-text {
        text-align: center;
        font-size: 1.3rem;
        color: #666;
        margin-bottom: 3rem;
        line-height: 1.6;
    }
    .status-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    .success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .info {
        background-color: #d1ecf1;
        color: #0c5460;
        border: 1px solid #bee5eb;
    }
</style>
""", unsafe_allow_html=True)

def get_streamlit_command():
    """Get the appropriate streamlit command for the current platform."""
    if platform.system() == "Windows":
        return Path("venv/Scripts/streamlit.exe")
    else:
        return Path("venv/bin/streamlit")

def launch_application(app_name, port):
    """Launch the specified application."""
    streamlit_cmd = get_streamlit_command()
    
    if not streamlit_cmd.exists():
        st.error("❌ Streamlit not found in virtual environment. Please run the setup first.")
        return False
    
    app_file = f"apps/{app_name}.py"
    if not Path(app_file).exists():
        st.error(f"❌ Application file {app_file} not found.")
        return False
    
    try:
        # Launch the application
        process = subprocess.Popen([
            str(streamlit_cmd), "run", app_file, 
            "--server.port", str(port),
            "--server.headless", "true"
        ], cwd=Path.cwd())
        
        # Wait a moment for the app to start
        time.sleep(2)
        
        # Open in browser
        url = f"http://localhost:{port}"
        webbrowser.open(url)
        
        return True, process
        
    except Exception as e:
        st.error(f"❌ Error launching {app_name}: {str(e)}")
        return False, None

def main():
    # Header
    st.markdown('<h1 class="main-header">🛡️ TCP Cybersecurity Compliance Hub</h1>', unsafe_allow_html=True)
    
    # Welcome text
    st.markdown("""
    <div class="welcome-text">
        Welcome to your comprehensive cybersecurity compliance consulting platform.<br>
        Choose an application to get started with your cybersecurity work.
    </div>
    """, unsafe_allow_html=True)
    
    # Application cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="app-card">
            <div class="app-title">🔍 Standards Navigator</div>
            <div class="app-description">
                Your personal cybersecurity standards repository.<br>
                Research, explore, and export cybersecurity frameworks.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Launch Standards Navigator", key="navigator", use_container_width=True):
            with st.spinner("🚀 Launching Standards Navigator..."):
                success, process = launch_application("standards_navigator", 8502)
                if success:
                    st.success("✅ Standards Navigator launched successfully!")
                    st.info("🌐 Opening at http://localhost:8502")
                    st.balloons()
                else:
                    st.error("❌ Failed to launch Standards Navigator")
    
    with col2:
        st.markdown("""
        <div class="app-card">
            <div class="app-title">🏢 Client Portal</div>
            <div class="app-description">
                Manage clients and conduct security assessments.<br>
                Evaluate security posture and generate professional reports.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Launch Client Portal", key="portal", use_container_width=True):
            with st.spinner("🚀 Launching Client Portal..."):
                success, process = launch_application("client_portal", 8503)
                if success:
                    st.success("✅ Client Portal launched successfully!")
                    st.info("🌐 Opening at http://localhost:8503")
                    st.balloons()
                else:
                    st.error("❌ Failed to launch Client Portal")
    
    # Instructions
    st.markdown("---")
    st.markdown("""
    ### 📋 Instructions
    
    1. **Click either button above** to launch the respective application
    2. **Applications will open** in new browser tabs automatically
    3. **Keep this page open** to launch additional applications
    4. **Use the navigation** within each application to switch between them
    
    ### 🛠️ Troubleshooting
    
    - If applications don't launch, ensure you're running from the TCP directory
    - Make sure the virtual environment is set up: `python -m venv venv`
    - Install dependencies: `pip install -r requirements.txt`
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🛡️ TCP Cybersecurity Compliance Hub - Your Complete Consulting Solution</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()