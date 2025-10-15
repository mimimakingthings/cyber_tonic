#!/usr/bin/env python3
"""
TCP Cybersecurity Compliance Hub - Cleanup Script
Removes unnecessary files and cleans up the project directory.
"""

import os
import shutil
import sys
from pathlib import Path
import subprocess

class TCPCleanup:
    def __init__(self):
        self.project_root = Path.cwd()
        self.files_to_remove = [
            'test_launch.py',  # Test file that's no longer needed
        ]
        
        self.directories_to_clean = [
            '__pycache__',
            '.pytest_cache',
            '.mypy_cache',
            '*.egg-info',
            '.coverage',
            'htmlcov',
            '.tox',
            '.cache',
            'dist',
            'build'
        ]
        
        self.patterns_to_remove = [
            '*.pyc',
            '*.pyo',
            '*.pyd',
            '*.log',
            '*.tmp',
            '.DS_Store',
            'Thumbs.db',
            '*.swp',
            '*.swo',
            '*~'
        ]
    
    def find_files_by_pattern(self, pattern):
        """Find files matching a pattern."""
        files = []
        for root, dirs, filenames in os.walk(self.project_root):
            for filename in filenames:
                if filename.endswith(pattern.replace('*', '')):
                    files.append(Path(root) / filename)
        return files
    
    def find_directories_by_pattern(self, pattern):
        """Find directories matching a pattern."""
        dirs = []
        for root, dirnames, filenames in os.walk(self.project_root):
            for dirname in dirnames:
                if dirname == pattern or (pattern.endswith('*') and dirname.startswith(pattern[:-1])):
                    dirs.append(Path(root) / dirname)
        return dirs
    
    def stop_running_processes(self):
        """Stop any running Streamlit processes."""
        print("🛑 Stopping any running Streamlit processes...")
        
        try:
            if sys.platform == "win32":
                # Windows
                subprocess.run(['taskkill', '/F', '/IM', 'streamlit.exe'], 
                             capture_output=True, check=False)
            else:
                # Unix-like systems
                subprocess.run(['pkill', '-f', 'streamlit'], 
                             capture_output=True, check=False)
            print("✅ Streamlit processes stopped")
        except Exception as e:
            print(f"⚠️ Could not stop processes: {e}")
    
    def remove_files(self):
        """Remove specific files."""
        print("🗑️ Removing unnecessary files...")
        
        removed_count = 0
        for file_pattern in self.files_to_remove:
            file_path = self.project_root / file_pattern
            if file_path.exists():
                try:
                    file_path.unlink()
                    print(f"✅ Removed: {file_pattern}")
                    removed_count += 1
                except Exception as e:
                    print(f"❌ Could not remove {file_pattern}: {e}")
        
        return removed_count
    
    def remove_pattern_files(self):
        """Remove files matching patterns."""
        print("🗑️ Removing files matching patterns...")
        
        removed_count = 0
        for pattern in self.patterns_to_remove:
            files = self.find_files_by_pattern(pattern)
            for file_path in files:
                try:
                    file_path.unlink()
                    print(f"✅ Removed: {file_path.relative_to(self.project_root)}")
                    removed_count += 1
                except Exception as e:
                    print(f"❌ Could not remove {file_path}: {e}")
        
        return removed_count
    
    def remove_directories(self):
        """Remove unnecessary directories."""
        print("🗑️ Removing unnecessary directories...")
        
        removed_count = 0
        for dir_pattern in self.directories_to_clean:
            dirs = self.find_directories_by_pattern(dir_pattern)
            for dir_path in dirs:
                try:
                    shutil.rmtree(dir_path)
                    print(f"✅ Removed directory: {dir_path.relative_to(self.project_root)}")
                    removed_count += 1
                except Exception as e:
                    print(f"❌ Could not remove directory {dir_path}: {e}")
        
        return removed_count
    
    def clean_python_cache(self):
        """Clean Python cache files."""
        print("🐍 Cleaning Python cache files...")
        
        removed_count = 0
        for root, dirs, files in os.walk(self.project_root):
            # Remove __pycache__ directories
            if '__pycache__' in dirs:
                cache_dir = Path(root) / '__pycache__'
                try:
                    shutil.rmtree(cache_dir)
                    print(f"✅ Removed: {cache_dir.relative_to(self.project_root)}")
                    removed_count += 1
                except Exception as e:
                    print(f"❌ Could not remove {cache_dir}: {e}")
            
            # Remove .pyc files
            for file in files:
                if file.endswith('.pyc') or file.endswith('.pyo'):
                    file_path = Path(root) / file
                    try:
                        file_path.unlink()
                        print(f"✅ Removed: {file_path.relative_to(self.project_root)}")
                        removed_count += 1
                    except Exception as e:
                        print(f"❌ Could not remove {file_path}: {e}")
        
        return removed_count
    
    def get_directory_size(self, path):
        """Get the size of a directory in bytes."""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        total_size += os.path.getsize(filepath)
        except Exception:
            pass
        return total_size
    
    def format_size(self, size_bytes):
        """Format size in human readable format."""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def show_cleanup_summary(self):
        """Show summary of what can be cleaned."""
        print("📊 Cleanup Summary:")
        print("=" * 50)
        
        # Check virtual environment size
        venv_path = self.project_root / 'venv'
        if venv_path.exists():
            venv_size = self.get_directory_size(venv_path)
            print(f"📦 Virtual environment: {self.format_size(venv_size)}")
        
        # Check for cache files
        cache_files = []
        for pattern in self.patterns_to_remove:
            cache_files.extend(self.find_files_by_pattern(pattern))
        
        if cache_files:
            print(f"🗑️ Cache files to remove: {len(cache_files)}")
        
        # Check for Python cache
        pycache_dirs = []
        for root, dirs, files in os.walk(self.project_root):
            if '__pycache__' in dirs:
                pycache_dirs.append(Path(root) / '__pycache__')
        
        if pycache_dirs:
            print(f"🐍 Python cache directories: {len(pycache_dirs)}")
        
        print("=" * 50)
    
    def run_cleanup(self, dry_run=False):
        """Run the cleanup process."""
        print("🧹 TCP Cybersecurity Compliance Hub - Cleanup")
        print("=" * 60)
        
        if dry_run:
            print("🔍 DRY RUN MODE - No files will be deleted")
            print()
            self.show_cleanup_summary()
            return
        
        # Stop running processes first
        self.stop_running_processes()
        
        print()
        total_removed = 0
        
        # Remove specific files
        total_removed += self.remove_files()
        
        # Remove pattern files
        total_removed += self.remove_pattern_files()
        
        # Remove directories
        total_removed += self.remove_directories()
        
        # Clean Python cache
        total_removed += self.clean_python_cache()
        
        print()
        print("=" * 60)
        print(f"✅ Cleanup completed! Removed {total_removed} items")
        print("🎉 Project directory is now clean!")
        print("=" * 60)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Clean up TCP project directory')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be cleaned without actually deleting')
    
    args = parser.parse_args()
    
    cleanup = TCPCleanup()
    cleanup.run_cleanup(dry_run=args.dry_run)

if __name__ == "__main__":
    main()
