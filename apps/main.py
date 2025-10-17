import streamlit as st
import subprocess
import sys
import platform
import time
import webbrowser
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Cybersecurity Compliance Hub",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Minimal CSS
st.markdown("""
<style>
    .stButton > button {
        height: 4rem;
        font-size: 1.2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def get_streamlit_command():
    """Get the appropriate streamlit command for the current platform."""
    # Use python3 -m streamlit for better compatibility across platforms
    return ["python3", "-m", "streamlit"]

def launch_application(app_name, port):
    """Launch the specified application."""
    streamlit_cmd = get_streamlit_command()
    
    app_file = f"apps/{app_name}.py"
    if not Path(app_file).exists():
        st.error(f"❌ Application file {app_file} not found.")
        return False, None
    
    try:
        # Launch the application using python3 -m streamlit
        process = subprocess.Popen(
            streamlit_cmd + ["run", app_file, 
            "--server.port", str(port),
            "--server.headless", "true"],
            cwd=Path.cwd()
        )
        
        # Wait a moment for the app to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            # Open in browser
            url = f"http://localhost:{port}"
            webbrowser.open(url)
            return True, process
        else:
            st.error(f"❌ {app_name} failed to start (exit code: {process.poll()})")
            return False, None
        
    except Exception as e:
        st.error(f"❌ Error launching {app_name}: {str(e)}")
        return False, None

def main():
    # Simple header
    st.markdown('<h1 style="text-align: center; color: #1f77b4; margin-bottom: 3rem;">🛡️ Cybersecurity Compliance Hub</h1>', unsafe_allow_html=True)
    
    # Two options
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 **Standards Navigator**", key="navigator", use_container_width=True):
            with st.spinner("Opening..."):
                success, process = launch_application("standards_navigator", 8502)
                if success:
                    st.success("✅ Standards Navigator opened!")
                else:
                    st.error("❌ Unable to open Standards Navigator")
    
    with col2:
        if st.button("🏢 **Client Portal**", key="portal", use_container_width=True):
            with st.spinner("Opening..."):
                success, process = launch_application("client_portal", 8503)
                if success:
                    st.success("✅ Client Portal opened!")
                else:
                    st.error("❌ Unable to open Client Portal")
    

if __name__ == "__main__":
    main()