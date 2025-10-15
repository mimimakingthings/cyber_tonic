#!/usr/bin/env python3
"""
TCP Cybersecurity Compliance Hub - Multi-App Launcher
Launches all applications simultaneously for easy access.
"""

import subprocess
import sys
import platform
import time
import webbrowser
import signal
import os
from pathlib import Path

class TCPLauncher:
    def __init__(self):
        self.processes = []
        self.ports = {
            'main': 8501,
            'standards_navigator': 8502,
            'client_portal': 8503
        }
        
    def get_streamlit_command(self):
        """Get the appropriate streamlit command for the current platform."""
        if platform.system() == "Windows":
            return Path("venv/Scripts/streamlit.exe")
        else:
            return Path("venv/bin/streamlit")
    
    def check_prerequisites(self):
        """Check if all prerequisites are met."""
        print("🔍 Checking prerequisites...")
        
        # Check if virtual environment exists
        venv_path = Path("venv")
        if not venv_path.exists():
            print("❌ Virtual environment not found. Please run setup first.")
            return False
        
        # Check if streamlit is available
        streamlit_cmd = self.get_streamlit_command()
        if not streamlit_cmd.exists():
            print("❌ Streamlit not found in virtual environment.")
            return False
        
        # Check if all app files exist
        required_files = ['apps/main.py', 'apps/standards_navigator.py', 'apps/client_portal.py']
        for file in required_files:
            if not Path(file).exists():
                print(f"❌ Required file not found: {file}")
                return False
        
        print("✅ All prerequisites met!")
        return True
    
    def launch_app(self, app_name, port):
        """Launch a single application."""
        streamlit_cmd = self.get_streamlit_command()
        app_file = f"apps/{app_name}.py"
        
        try:
            print(f"🚀 Launching {app_name} on port {port}...")
            
            # Launch the application
            process = subprocess.Popen([
                str(streamlit_cmd), "run", app_file, 
                "--server.port", str(port),
                "--server.headless", "true",
                "--server.runOnSave", "false"
            ], cwd=Path.cwd())
            
            # Wait a moment for the app to start
            time.sleep(2)
            
            # Check if process is still running
            if process.poll() is None:
                print(f"✅ {app_name} launched successfully (PID: {process.pid})")
                return process
            else:
                print(f"❌ {app_name} failed to start (exit code: {process.poll()})")
                return None
                
        except Exception as e:
            print(f"❌ Error launching {app_name}: {str(e)}")
            return None
    
    def launch_all(self):
        """Launch all applications."""
        print("🛡️ TCP Cybersecurity Compliance Hub - Multi-App Launcher")
        print("=" * 60)
        
        if not self.check_prerequisites():
            return False
        
        print("\n🚀 Launching all applications...")
        
        # Launch main application first
        main_process = self.launch_app('main', self.ports['main'])
        if main_process:
            self.processes.append(('main', main_process))
            time.sleep(1)
        
        # Launch standards navigator
        nav_process = self.launch_app('standards_navigator', self.ports['standards_navigator'])
        if nav_process:
            self.processes.append(('standards_navigator', nav_process))
            time.sleep(1)
        
        # Launch client portal
        portal_process = self.launch_app('client_portal', self.ports['client_portal'])
        if portal_process:
            self.processes.append(('client_portal', portal_process))
        
        if not self.processes:
            print("❌ No applications were launched successfully.")
            return False
        
        print(f"\n✅ Successfully launched {len(self.processes)} applications!")
        print("\n🌐 Applications are now running at:")
        for app_name, process in self.processes:
            port = self.ports[app_name]
            print(f"   • {app_name.replace('_', ' ').title()}: http://localhost:{port}")
        
        # Open main application in browser
        time.sleep(3)
        print(f"\n🌐 Opening main application in browser...")
        webbrowser.open(f"http://localhost:{self.ports['main']}")
        
        return True
    
    def cleanup(self):
        """Clean up all running processes."""
        print("\n🛑 Shutting down all applications...")
        
        for app_name, process in self.processes:
            try:
                print(f"🛑 Stopping {app_name}...")
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {app_name} stopped")
            except subprocess.TimeoutExpired:
                print(f"⚠️ Force killing {app_name}...")
                process.kill()
                process.wait()
            except Exception as e:
                print(f"❌ Error stopping {app_name}: {e}")
        
        self.processes.clear()
        print("✅ All applications stopped")
    
    def run(self):
        """Main run method with signal handling."""
        # Set up signal handlers for graceful shutdown
        def signal_handler(signum, frame):
            print(f"\n🛑 Received signal {signum}, shutting down...")
            self.cleanup()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            if self.launch_all():
                print("\n" + "=" * 60)
                print("🎉 All applications are running!")
                print("📋 Instructions:")
                print("   • Use the main application to launch individual apps")
                print("   • Or access them directly via the URLs above")
                print("   • Press Ctrl+C to stop all applications")
                print("=" * 60)
                
                # Keep the script running
                while True:
                    time.sleep(1)
                    # Check if any process has died
                    for app_name, process in self.processes[:]:
                        if process.poll() is not None:
                            print(f"⚠️ {app_name} has stopped unexpectedly")
                            self.processes.remove((app_name, process))
                    
                    if not self.processes:
                        print("❌ All applications have stopped")
                        break
            else:
                print("❌ Failed to launch applications")
                return 1
                
        except KeyboardInterrupt:
            print("\n🛑 Keyboard interrupt received")
        finally:
            self.cleanup()
        
        return 0

if __name__ == "__main__":
    launcher = TCPLauncher()
    sys.exit(launcher.run())
