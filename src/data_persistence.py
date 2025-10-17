"""
Data Persistence Module for Cyber Tonic Client Portal

This module handles saving and loading client data and assessment data between sessions.
It provides automatic persistence functionality with JSON file storage.
"""

import json
import os
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import streamlit as st
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataPersistence:
    """Handles data persistence for client and assessment data."""
    
    def __init__(self, storage_dir: str = None):
        """
        Initialize data persistence with storage directory.
        
        Args:
            storage_dir: Directory to store data files. Defaults to data/storage
        """
        if storage_dir is None:
            # Default to data/storage relative to the project root
            self.storage_dir = Path(__file__).parent.parent / "data" / "storage"
        else:
            self.storage_dir = Path(storage_dir)
        
        # Ensure storage directory exists
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # File paths
        self.clients_file = self.storage_dir / "clients.json"
        self.assessments_file = self.storage_dir / "assessments.json"
        self.evidence_files_file = self.storage_dir / "evidence_files.json"
        self.backup_dir = self.storage_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
    
    def save_clients(self, clients: List[Dict[str, Any]]) -> bool:
        """
        Save clients data to JSON file.
        
        Args:
            clients: List of client dictionaries
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create backup before saving
            if self.clients_file.exists():
                self._create_backup(self.clients_file, "clients")
            
            # Prepare data with metadata
            data = {
                "clients": clients,
                "metadata": {
                    "last_updated": datetime.now().isoformat(),
                    "total_clients": len(clients),
                    "version": "1.0"
                }
            }
            
            # Save to file
            with open(self.clients_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            
            logger.info(f"Successfully saved {len(clients)} clients to {self.clients_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving clients: {e}")
            return False
    
    def load_clients(self) -> List[Dict[str, Any]]:
        """
        Load clients data from JSON file.
        
        Returns:
            List of client dictionaries
        """
        try:
            if not self.clients_file.exists():
                logger.info("Clients file does not exist, returning empty list")
                return []
            
            with open(self.clients_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle both old format (direct list) and new format (with metadata)
            if isinstance(data, list):
                clients = data
            elif isinstance(data, dict) and "clients" in data:
                clients = data["clients"]
            else:
                logger.warning("Unexpected data format in clients file")
                return []
            
            logger.info(f"Successfully loaded {len(clients)} clients from {self.clients_file}")
            return clients
            
        except Exception as e:
            logger.error(f"Error loading clients: {e}")
            return []
    
    def save_assessments(self, assessments: Dict[str, Any]) -> bool:
        """
        Save assessments data to JSON file with enhanced schema support.
        
        Args:
            assessments: Dictionary of assessments by client ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create backup before saving
            if self.assessments_file.exists():
                self._create_backup(self.assessments_file, "assessments")
            
            # Prepare data with enhanced metadata
            data = {
                "assessments": assessments,
                "metadata": {
                    "last_updated": datetime.now().isoformat(),
                    "total_clients": len(assessments),
                    "version": "2.0",  # Updated version for enhanced features
                    "schema_version": "2.0",
                    "features": {
                        "weights": True,
                        "evidence_tags": True,
                        "trend_analysis": True,
                        "version_control": True
                    }
                }
            }
            
            # Save to file
            with open(self.assessments_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            
            logger.info(f"Successfully saved assessments for {len(assessments)} clients to {self.assessments_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving assessments: {e}")
            return False
    
    def load_assessments(self) -> Dict[str, Any]:
        """
        Load assessments data from JSON file.
        
        Returns:
            Dictionary of assessments by client ID
        """
        try:
            if not self.assessments_file.exists():
                logger.info("Assessments file does not exist, returning empty dict")
                return {}
            
            with open(self.assessments_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle both old format (direct dict) and new format (with metadata)
            if isinstance(data, dict) and "assessments" in data:
                assessments = data["assessments"]
            elif isinstance(data, dict):
                assessments = data
            else:
                logger.warning("Unexpected data format in assessments file")
                return {}
            
            logger.info(f"Successfully loaded assessments for {len(assessments)} clients from {self.assessments_file}")
            return assessments
            
        except Exception as e:
            logger.error(f"Error loading assessments: {e}")
            return {}
    
    def save_evidence_files(self, evidence_files: Dict[str, Any]) -> bool:
        """
        Save evidence files data to JSON file.
        
        Args:
            evidence_files: Dictionary of evidence files by client ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create backup before saving
            if self.evidence_files_file.exists():
                self._create_backup(self.evidence_files_file, "evidence_files")
            
            # Prepare data with metadata
            data = {
                "evidence_files": evidence_files,
                "metadata": {
                    "last_updated": datetime.now().isoformat(),
                    "total_clients": len(evidence_files),
                    "version": "1.0"
                }
            }
            
            # Save to file
            with open(self.evidence_files_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            
            logger.info(f"Successfully saved evidence files for {len(evidence_files)} clients to {self.evidence_files_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving evidence files: {e}")
            return False
    
    def load_evidence_files(self) -> Dict[str, Any]:
        """
        Load evidence files data from JSON file.
        
        Returns:
            Dictionary of evidence files by client ID
        """
        try:
            if not self.evidence_files_file.exists():
                logger.info("Evidence files file does not exist, returning empty dict")
                return {}
            
            with open(self.evidence_files_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle both old format (direct dict) and new format (with metadata)
            if isinstance(data, dict) and "evidence_files" in data:
                evidence_files = data["evidence_files"]
            elif isinstance(data, dict):
                evidence_files = data
            else:
                logger.warning("Unexpected data format in evidence files file")
                return {}
            
            logger.info(f"Successfully loaded evidence files for {len(evidence_files)} clients from {self.evidence_files_file}")
            return evidence_files
            
        except Exception as e:
            logger.error(f"Error loading evidence files: {e}")
            return {}
    
    def save_all_data(self, clients: List[Dict[str, Any]], assessments: Dict[str, Any], evidence_files: Dict[str, Any]) -> bool:
        """
        Save all data (clients, assessments, evidence files) in a single operation.
        
        Args:
            clients: List of client dictionaries
            assessments: Dictionary of assessments by client ID
            evidence_files: Dictionary of evidence files by client ID
            
        Returns:
            True if all saves successful, False otherwise
        """
        success = True
        
        # Save each data type
        if not self.save_clients(clients):
            success = False
        
        if not self.save_assessments(assessments):
            success = False
        
        if not self.save_evidence_files(evidence_files):
            success = False
        
        if success:
            logger.info("Successfully saved all data")
        else:
            logger.error("Some data failed to save")
        
        return success
    
    def load_all_data(self) -> tuple[List[Dict[str, Any]], Dict[str, Any], Dict[str, Any]]:
        """
        Load all data (clients, assessments, evidence files) in a single operation.
        
        Returns:
            Tuple of (clients, assessments, evidence_files)
        """
        clients = self.load_clients()
        assessments = self.load_assessments()
        evidence_files = self.load_evidence_files()
        
        logger.info("Successfully loaded all data")
        return clients, assessments, evidence_files
    
    def _create_backup(self, file_path: Path, data_type: str) -> None:
        """
        Create a backup of the given file.
        
        Args:
            file_path: Path to the file to backup
            data_type: Type of data for backup naming
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{data_type}_backup_{timestamp}.json"
            backup_path = self.backup_dir / backup_filename
            
            # Copy file to backup location
            import shutil
            shutil.copy2(file_path, backup_path)
            
            logger.info(f"Created backup: {backup_path}")
            
            # Clean up old backups (keep last 10)
            self._cleanup_old_backups(data_type)
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
    
    def _cleanup_old_backups(self, data_type: str) -> None:
        """
        Clean up old backup files, keeping only the most recent 10.
        
        Args:
            data_type: Type of data for backup cleanup
        """
        try:
            # Get all backup files for this data type
            backup_files = list(self.backup_dir.glob(f"{data_type}_backup_*.json"))
            
            # Sort by modification time (newest first)
            backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Remove files beyond the 10 most recent
            for old_backup in backup_files[10:]:
                old_backup.unlink()
                logger.info(f"Removed old backup: {old_backup}")
                
        except Exception as e:
            logger.error(f"Error cleaning up old backups: {e}")
    
    def get_storage_info(self) -> Dict[str, Any]:
        """
        Get information about stored data.
        
        Returns:
            Dictionary with storage information
        """
        info = {
            "storage_directory": str(self.storage_dir),
            "files": {},
            "backups": {}
        }
        
        # Check main files
        for file_path, name in [
            (self.clients_file, "clients"),
            (self.assessments_file, "assessments"),
            (self.evidence_files_file, "evidence_files")
        ]:
            if file_path.exists():
                stat = file_path.stat()
                info["files"][name] = {
                    "path": str(file_path),
                    "size_bytes": stat.st_size,
                    "size_mb": round(stat.st_size / (1024 * 1024), 2),
                    "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                }
            else:
                info["files"][name] = {"exists": False}
        
        # Check backup files
        backup_files = list(self.backup_dir.glob("*.json"))
        info["backups"]["count"] = len(backup_files)
        info["backups"]["directory"] = str(self.backup_dir)
        
        return info
    
    def export_data(self, export_path: str) -> bool:
        """
        Export all data to a single JSON file.
        
        Args:
            export_path: Path where to save the export file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            clients, assessments, evidence_files = self.load_all_data()
            
            export_data = {
                "export_info": {
                    "export_date": datetime.now().isoformat(),
                    "version": "1.0",
                    "source": "Cyber Tonic Client Portal"
                },
                "clients": clients,
                "assessments": assessments,
                "evidence_files": evidence_files
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            logger.info(f"Successfully exported all data to {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            return False
    
    def import_data(self, import_path: str) -> bool:
        """
        Import data from a JSON file.
        
        Args:
            import_path: Path to the import file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # Extract data (handle different formats)
            if "clients" in import_data:
                clients = import_data["clients"]
            else:
                clients = []
            
            if "assessments" in import_data:
                assessments = import_data["assessments"]
            else:
                assessments = {}
            
            if "evidence_files" in import_data:
                evidence_files = import_data["evidence_files"]
            else:
                evidence_files = {}
            
            # Save imported data
            success = self.save_all_data(clients, assessments, evidence_files)
            
            if success:
                logger.info(f"Successfully imported data from {import_path}")
            else:
                logger.error("Failed to save imported data")
            
            return success
            
        except Exception as e:
            logger.error(f"Error importing data: {e}")
            return False
    
    def save_assessment_weights(self, client_id: str, weights: Dict[str, float]) -> bool:
        """
        Save assessment weights for a specific client.
        
        Args:
            client_id: Client identifier
            weights: Dictionary of function weights
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load current assessments
            assessments = self.load_assessments()
            
            # Initialize client assessments if not exists
            if client_id not in assessments:
                assessments[client_id] = {}
            
            # Add weights to client data
            assessments[client_id]["weights"] = weights
            assessments[client_id]["weights_updated"] = datetime.now().isoformat()
            
            # Save updated assessments
            return self.save_assessments(assessments)
            
        except Exception as e:
            logger.error(f"Error saving assessment weights: {e}")
            return False
    
    def load_assessment_weights(self, client_id: str) -> Dict[str, float]:
        """
        Load assessment weights for a specific client.
        
        Args:
            client_id: Client identifier
            
        Returns:
            Dictionary of function weights
        """
        try:
            assessments = self.load_assessments()
            return assessments.get(client_id, {}).get("weights", {})
            
        except Exception as e:
            logger.error(f"Error loading assessment weights: {e}")
            return {}
    
    def save_evidence_metadata(self, client_id: str, subcategory_id: str, evidence_metadata: Dict[str, Any]) -> bool:
        """
        Save evidence metadata for a specific subcategory.
        
        Args:
            client_id: Client identifier
            subcategory_id: Subcategory identifier
            evidence_metadata: Evidence metadata dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load current assessments
            assessments = self.load_assessments()
            
            # Initialize client assessments if not exists
            if client_id not in assessments:
                assessments[client_id] = {}
            
            # Initialize subcategory if not exists
            if subcategory_id not in assessments[client_id]:
                assessments[client_id][subcategory_id] = {}
            
            # Add evidence metadata
            assessments[client_id][subcategory_id]["evidence"] = evidence_metadata
            
            # Save updated assessments
            return self.save_assessments(assessments)
            
        except Exception as e:
            logger.error(f"Error saving evidence metadata: {e}")
            return False
    
    def create_assessment_snapshot(self, client_id: str, snapshot_data: Dict[str, Any]) -> bool:
        """
        Create an assessment snapshot for version control.
        
        Args:
            client_id: Client identifier
            snapshot_data: Snapshot data dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load current assessments
            assessments = self.load_assessments()
            
            # Initialize client assessments if not exists
            if client_id not in assessments:
                assessments[client_id] = {}
            
            # Initialize snapshots if not exists
            if "snapshots" not in assessments[client_id]:
                assessments[client_id]["snapshots"] = []
            
            # Add snapshot with timestamp
            snapshot = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "data": snapshot_data
            }
            
            assessments[client_id]["snapshots"].append(snapshot)
            
            # Keep only last 10 snapshots
            assessments[client_id]["snapshots"] = assessments[client_id]["snapshots"][-10:]
            
            # Save updated assessments
            return self.save_assessments(assessments)
            
        except Exception as e:
            logger.error(f"Error creating assessment snapshot: {e}")
            return False
    
    def delete_client(self, client_id: str) -> bool:
        """
        Delete a client and all associated data (assessments, evidence files).
        
        Args:
            client_id: Client identifier to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create backup before deletion
            self._create_backup(self.clients_file, "clients")
            self._create_backup(self.assessments_file, "assessments")
            self._create_backup(self.evidence_files_file, "evidence_files")
            
            # Load current data
            clients = self.load_clients()
            assessments = self.load_assessments()
            evidence_files = self.load_evidence_files()
            
            # Find and remove client
            original_count = len(clients)
            clients = [client for client in clients if client.get("id") != client_id]
            
            if len(clients) == original_count:
                logger.warning(f"Client {client_id} not found for deletion")
                return False
            
            # Remove associated assessments
            if client_id in assessments:
                del assessments[client_id]
                logger.info(f"Removed assessments for client {client_id}")
            
            # Remove associated evidence files
            if client_id in evidence_files:
                del evidence_files[client_id]
                logger.info(f"Removed evidence files for client {client_id}")
            
            # Save updated data
            success = self.save_all_data(clients, assessments, evidence_files)
            
            if success:
                logger.info(f"Successfully deleted client {client_id} and associated data")
            else:
                logger.error(f"Failed to save data after deleting client {client_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error deleting client {client_id}: {e}")
            return False
    
    def get_client_count(self) -> int:
        """
        Get the total number of clients.
        
        Returns:
            Number of clients
        """
        try:
            clients = self.load_clients()
            return len(clients)
        except Exception as e:
            logger.error(f"Error getting client count: {e}")
            return 0


# Global instance for easy access
data_persistence = DataPersistence()

# Convenience functions for Streamlit integration
def save_session_data():
    """Save current session state data to persistent storage."""
    try:
        clients = st.session_state.get("clients", [])
        assessments = st.session_state.get("assessments", {})
        evidence_files = st.session_state.get("evidence_files", {})
        
        success = data_persistence.save_all_data(clients, assessments, evidence_files)
        
        if success:
            st.session_state["last_save_time"] = datetime.now().isoformat()
            return True
        else:
            return False
            
    except Exception as e:
        logger.error(f"Error saving session data: {e}")
        return False

def load_session_data():
    """Load data from persistent storage into session state."""
    try:
        clients, assessments, evidence_files = data_persistence.load_all_data()
        
        st.session_state["clients"] = clients
        st.session_state["assessments"] = assessments
        st.session_state["evidence_files"] = evidence_files
        st.session_state["data_loaded"] = True
        
        logger.info("Successfully loaded session data")
        return True
        
    except Exception as e:
        logger.error(f"Error loading session data: {e}")
        return False

def auto_save_data():
    """Automatically save data when changes are detected."""
    try:
        # Check if data has changed since last save
        current_data_hash = hash(str(st.session_state.get("clients", [])) + 
                               str(st.session_state.get("assessments", {})) + 
                               str(st.session_state.get("evidence_files", {})))
        
        last_hash = st.session_state.get("data_hash", None)
        
        if current_data_hash != last_hash:
            if save_session_data():
                st.session_state["data_hash"] = current_data_hash
                logger.info("Auto-saved data due to changes")
                return True
        
        return False
        
    except Exception as e:
        logger.error(f"Error in auto-save: {e}")
        return False

def delete_client_from_session(client_id: str) -> bool:
    """
    Delete a client from session state and persistent storage.
    
    Args:
        client_id: Client identifier to delete
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Delete from persistent storage
        success = data_persistence.delete_client(client_id)
        
        if success:
            # Update session state
            clients = st.session_state.get("clients", [])
            assessments = st.session_state.get("assessments", {})
            evidence_files = st.session_state.get("evidence_files", {})
            
            # Remove from session state
            st.session_state["clients"] = [client for client in clients if client.get("id") != client_id]
            
            if client_id in assessments:
                del assessments[client_id]
                st.session_state["assessments"] = assessments
            
            if client_id in evidence_files:
                del evidence_files[client_id]
                st.session_state["evidence_files"] = evidence_files
            
            # Clear selected client if it was the deleted one
            if st.session_state.get("selected_client") == client_id:
                remaining_clients = st.session_state.get("clients", [])
                if remaining_clients:
                    st.session_state["selected_client"] = remaining_clients[0]["id"]
                else:
                    st.session_state["selected_client"] = None
            
            # Update data hash to trigger auto-save
            st.session_state["data_hash"] = None
            
            logger.info(f"Successfully deleted client {client_id} from session")
        
        return success
        
    except Exception as e:
        logger.error(f"Error deleting client {client_id} from session: {e}")
        return False
