#!/usr/bin/env python3
"""
Cyber Tonic Cybersecurity Compliance Hub - Master Launcher
A comprehensive script to easily launch the entire application suite.

Usage:
    python launch.py                    # Launch main app only
    python launch.py --all              # Launch all apps simultaneously
    python launch.py --setup            # Set up virtual environment
    python launch.py --clean            # Clean up temporary files
    python launch.py --test             # Run pytest tests
    python launch.py --help             # Show help
"""

import subprocess
import sys
import platform
import time
import webbrowser
import signal
import os
import argparse
from pathlib import Path

class CyberTonicLauncher:
    def __init__(self):
        self.processes = []
        self.ports = {
            'main': 8501,
            'standards_navigator': 8502,
            'client_portal': 8503
        }
        self.project_root = Path.cwd()
        
    def print_banner(self):
        """Print the application banner."""
        print("🛡️" + "=" * 58 + "🛡️")
        print("    Cyber Tonic Cybersecurity Compliance Hub")
        print("    Master Launcher - Complete Application Suite")
        print("🛡️" + "=" * 58 + "🛡️")
        print()
    
    def check_python_version(self):
        """Check if Python version is compatible."""
        if sys.version_info < (3, 9):
            print("❌ Error: Python 3.9 or higher is required.")
            print(f"   Current version: {sys.version}")
            return False
        return True
    
    def setup_virtual_environment(self):
        """Set up virtual environment and install dependencies."""
        print("🔧 Setting up virtual environment...")
        
        venv_path = self.project_root / "venv"
        
        # Create virtual environment
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print("✅ Virtual environment created")
        except subprocess.CalledProcessError:
            print("❌ Failed to create virtual environment")
            return False
        
        # Get the appropriate pip command
        if platform.system() == "Windows":
            pip_cmd = venv_path / "Scripts" / "pip"
        else:
            pip_cmd = venv_path / "bin" / "pip"
        
        # Install dependencies
        try:
            subprocess.run([str(pip_cmd), "install", "-r", "requirements.txt"], check=True)
            print("✅ Dependencies installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False
        
        print("🎉 Setup completed successfully!")
        print("💡 You can now run: python launch.py")
        return True
    
    def get_streamlit_command(self):
        """Get the appropriate streamlit command for the current platform."""
        venv_path = self.project_root / "venv"
        
        if venv_path.exists():
            if platform.system() == "Windows":
                return [str(venv_path / "Scripts" / "streamlit.exe")]
            else:
                return [str(venv_path / "bin" / "streamlit")]
        else:
            # Fallback to system streamlit
            return ["python3", "-m", "streamlit"]
    
    def check_prerequisites(self):
        """Check if all prerequisites are met."""
        print("🔍 Checking prerequisites...")
        
        # Check if virtual environment exists
        venv_path = self.project_root / "venv"
        if not venv_path.exists():
            print("❌ Virtual environment not found.")
            print("💡 Run: python launch.py --setup")
            return False
        
        # Check if streamlit is available
        try:
            streamlit_cmd = self.get_streamlit_command()
            result = subprocess.run(streamlit_cmd + ["--version"], 
                                  capture_output=True, text=True, check=True)
            print("✅ Streamlit is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Streamlit not found. Please run: python launch.py --setup")
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
            print(f"🚀 Launching {app_name.replace('_', ' ').title()} on port {port}...")
            
            # Launch the application
            process = subprocess.Popen(
                streamlit_cmd + ["run", app_file, 
                "--server.port", str(port),
                "--server.headless", "true",
                "--server.runOnSave", "false"],
                cwd=self.project_root
            )
            
            # Wait a moment for the app to start
            time.sleep(2)
            
            # Check if process is still running
            if process.poll() is None:
                print(f"✅ {app_name.replace('_', ' ').title()} launched successfully (PID: {process.pid})")
                return process
            else:
                print(f"❌ {app_name.replace('_', ' ').title()} failed to start (exit code: {process.poll()})")
                return None
                
        except Exception as e:
            print(f"❌ Error launching {app_name}: {str(e)}")
            return None
    
    def launch_main_only(self):
        """Launch only the main application."""
        if not self.check_prerequisites():
            return False
        
        print("🚀 Launching Cyber Tonic Cybersecurity Compliance Hub...")
        
        # Launch main application
        main_process = self.launch_app('main', self.ports['main'])
        if main_process:
            self.processes.append(('main', main_process))
            
            # Open in browser
            time.sleep(3)
            print(f"🌐 Opening application in browser...")
            webbrowser.open(f"http://localhost:{self.ports['main']}")
            
            print(f"\n✅ Application is running at: http://localhost:{self.ports['main']}")
            print("📝 Press Ctrl+C to stop the application")
            return True
        else:
            print("❌ Failed to launch application")
            return False
    
    def launch_all_apps(self):
        """Launch all applications simultaneously."""
        if not self.check_prerequisites():
            return False
        
        print("🚀 Launching all applications...")
        
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
    
    def cleanup_processes(self):
        """Clean up all running processes."""
        print("\n🛑 Shutting down all applications...")
        
        for app_name, process in self.processes:
            try:
                print(f"🛑 Stopping {app_name.replace('_', ' ').title()}...")
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {app_name.replace('_', ' ').title()} stopped")
            except subprocess.TimeoutExpired:
                print(f"⚠️ Force killing {app_name.replace('_', ' ').title()}...")
                process.kill()
                process.wait()
            except Exception as e:
                print(f"❌ Error stopping {app_name}: {e}")
        
        self.processes.clear()
        print("✅ All applications stopped")
    
    def run_tests(self):
        """Run pytest tests for the application."""
        print("🧪 Running pytest tests...")
        
        try:
            # Check if pytest is available
            result = subprocess.run([sys.executable, "-m", "pytest", "--version"], 
                                  capture_output=True, text=True, cwd=self.project_root)
            if result.returncode != 0:
                print("❌ pytest not found. Please install it with: pip install pytest")
                return 1
            
            # Run tests
            test_result = subprocess.run([
                sys.executable, "-m", "pytest", 
                "tests/", 
                "-v", 
                "--tb=short"
            ], cwd=self.project_root)
            
            if test_result.returncode == 0:
                print("✅ All tests passed!")
                return 0
            else:
                print("❌ Some tests failed. Check output above for details.")
                return 1
                
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            return 1
    
    def cleanup_files(self):
        """Clean up temporary files and cache."""
        print("🧹 Cleaning up temporary files...")
        
        # Run the existing cleanup script
        cleanup_script = self.project_root / "scripts" / "cleanup.py"
        if cleanup_script.exists():
            try:
                subprocess.run([sys.executable, str(cleanup_script)], check=True)
                print("✅ Cleanup completed")
            except subprocess.CalledProcessError:
                print("❌ Cleanup script failed")
        else:
            print("⚠️ Cleanup script not found")
    
    def run_interactive(self):
        """Run the launcher interactively."""
        # Set up signal handlers for graceful shutdown
        def signal_handler(signum, frame):
            print(f"\n🛑 Received signal {signum}, shutting down...")
            self.cleanup_processes()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            if self.launch_all_apps():
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
                            print(f"⚠️ {app_name.replace('_', ' ').title()} has stopped unexpectedly")
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
            self.cleanup_processes()
        
        return 0

def main():
    parser = argparse.ArgumentParser(
        description='Cyber Tonic Cybersecurity Compliance Hub - Master Launcher',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch.py                    # Launch main app only
  python launch.py --all              # Launch all apps simultaneously
  python launch.py --setup            # Set up virtual environment
  python launch.py --clean            # Clean up temporary files
        """
    )
    
    parser.add_argument('--all', action='store_true',
                       help='Launch all applications simultaneously')
    parser.add_argument('--setup', action='store_true',
                       help='Set up virtual environment and install dependencies')
    parser.add_argument('--clean', action='store_true',
                       help='Clean up temporary files and cache')
    parser.add_argument('--test', action='store_true',
                       help='Run pytest tests')
    
    args = parser.parse_args()
    
    launcher = CyberTonicLauncher()
    launcher.print_banner()
    
    if not launcher.check_python_version():
        return 1
    
    if args.setup:
        return 0 if launcher.setup_virtual_environment() else 1
    elif args.clean:
        launcher.cleanup_files()
        return 0
    elif args.test:
        return launcher.run_tests()
    elif args.all:
        return launcher.run_interactive()
    else:
        # Default: launch main app only
        if launcher.launch_main_only():
            try:
                # Keep running until interrupted
                while True:
                    time.sleep(1)
                    # Check if process has died
                    if launcher.processes:
                        app_name, process = launcher.processes[0]
                        if process.poll() is not None:
                            print(f"⚠️ Application has stopped unexpectedly")
                            break
            except KeyboardInterrupt:
                print("\n🛑 Keyboard interrupt received")
            finally:
                launcher.cleanup_processes()
            return 0
        else:
            return 1

if __name__ == "__main__":
    sys.exit(main())
