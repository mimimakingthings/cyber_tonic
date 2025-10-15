"""
Standards Data Loader Module

This module handles loading and managing cybersecurity standards data from JSON files.
It provides functions to load individual standards, all standards, and perform
cross-standard analysis and mapping.
"""

import json
import os
from typing import Dict, List, Optional, Any
from pathlib import Path

class StandardsLoader:
    """Class to handle loading and managing cybersecurity standards data."""
    
    def __init__(self, standards_dir: str = "data/standards_data"):
        """
        Initialize the StandardsLoader.
        
        Args:
            standards_dir: Directory containing the standards JSON files
        """
        self.standards_dir = Path(standards_dir)
        self._standards_cache = {}
        self._index_cache = None
    
    def load_index(self) -> Dict[str, Any]:
        """
        Load the standards index file.
        
        Returns:
            Dictionary containing the standards index
        """
        if self._index_cache is None:
            index_file = self.standards_dir / "standards_index.json"
            if index_file.exists():
                with open(index_file, 'r', encoding='utf-8') as f:
                    self._index_cache = json.load(f)
            else:
                raise FileNotFoundError(f"Standards index file not found: {index_file}")
        
        return self._index_cache
    
    def load_standard(self, standard_id: str) -> Dict[str, Any]:
        """
        Load a specific standard by its ID.
        
        Args:
            standard_id: The ID of the standard to load
            
        Returns:
            Dictionary containing the standard data
        """
        if standard_id in self._standards_cache:
            return self._standards_cache[standard_id]
        
        index = self.load_index()
        if standard_id not in index["standards"]:
            raise ValueError(f"Standard '{standard_id}' not found in index")
        
        file_name = index["standards"][standard_id]["file"]
        file_path = self.standards_dir / file_name
        
        if not file_path.exists():
            raise FileNotFoundError(f"Standard file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            standard_data = json.load(f)
        
        self._standards_cache[standard_id] = standard_data
        return standard_data
    
    def load_all_standards(self) -> Dict[str, Dict[str, Any]]:
        """
        Load all available standards.
        
        Returns:
            Dictionary containing all standards data
        """
        index = self.load_index()
        all_standards = {}
        
        for standard_id in index["standards"]:
            all_standards[standard_id] = self.load_standard(standard_id)
        
        return all_standards
    
    def get_standards_by_region(self, region: str) -> List[str]:
        """
        Get list of standard IDs for a specific region.
        
        Args:
            region: The region to filter by (e.g., 'USA', 'EU', 'UK', 'Global')
            
        Returns:
            List of standard IDs for the specified region
        """
        index = self.load_index()
        return index.get("regions", {}).get(region, [])
    
    def get_standards_by_type(self, standard_type: str) -> List[str]:
        """
        Get list of standard IDs for a specific type.
        
        Args:
            standard_type: The type to filter by (e.g., 'Framework', 'Standard', 'Regulation')
            
        Returns:
            List of standard IDs for the specified type
        """
        index = self.load_index()
        return index.get("categories", {}).get(standard_type, [])
    
    def get_standard_metadata(self, standard_id: str) -> Dict[str, Any]:
        """
        Get metadata for a specific standard.
        
        Args:
            standard_id: The ID of the standard
            
        Returns:
            Dictionary containing standard metadata
        """
        index = self.load_index()
        return index["standards"].get(standard_id, {})
    
    def search_controls(self, search_term: str, standard_ids: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
        """
        Search for controls across standards.
        
        Args:
            search_term: The term to search for
            standard_ids: Optional list of standard IDs to search in. If None, searches all.
            
        Returns:
            Dictionary containing search results organized by standard and function
        """
        if standard_ids is None:
            index = self.load_index()
            standard_ids = list(index["standards"].keys())
        
        results = {}
        
        for standard_id in standard_ids:
            try:
                standard_data = self.load_standard(standard_id)
                standard_results = {}
                
                for func_name, func_data in standard_data.get("functions", {}).items():
                    func_results = {}
                    
                    for control_id, control_data in func_data.get("subcategories", {}).items():
                        # Search in description, examples, use_cases, and tech_recommendations
                        searchable_text = f"{control_id} {control_data.get('description', '')} {control_data.get('examples', '')} {control_data.get('use_cases', '')} {' '.join(control_data.get('tech_recommendations', []))}".lower()
                        
                        if search_term.lower() in searchable_text:
                            func_results[control_id] = control_data
                    
                    if func_results:
                        standard_results[func_name] = func_results
                
                if standard_results:
                    results[standard_id] = standard_results
                    
            except Exception as e:
                print(f"Error loading standard {standard_id}: {e}")
                continue
        
        return results
    
    def get_cross_mappings(self, control_id: str, standard_id: str) -> Dict[str, str]:
        """
        Get cross-mappings for a specific control.
        
        Args:
            control_id: The control ID to get mappings for
            standard_id: The standard ID containing the control
            
        Returns:
            Dictionary of cross-mappings to other standards
        """
        try:
            standard_data = self.load_standard(standard_id)
            
            for func_name, func_data in standard_data.get("functions", {}).items():
                for ctrl_id, control_data in func_data.get("subcategories", {}).items():
                    if ctrl_id == control_id:
                        return control_data.get("mappings", {})
            
            return {}
            
        except Exception as e:
            print(f"Error getting cross-mappings for {control_id} in {standard_id}: {e}")
            return {}
    
    def get_all_cross_mappings(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        """
        Get all cross-mappings across all standards.
        
        Returns:
            Dictionary organized by standard_id -> control_id -> mappings
        """
        all_mappings = {}
        index = self.load_index()
        
        for standard_id in index["standards"]:
            try:
                standard_data = self.load_standard(standard_id)
                standard_mappings = {}
                
                for func_name, func_data in standard_data.get("functions", {}).items():
                    for control_id, control_data in func_data.get("subcategories", {}).items():
                        mappings = control_data.get("mappings", {})
                        if mappings:
                            standard_mappings[control_id] = mappings
                
                if standard_mappings:
                    all_mappings[standard_id] = standard_mappings
                    
            except Exception as e:
                print(f"Error processing cross-mappings for {standard_id}: {e}")
                continue
        
        return all_mappings
    
    def validate_standards_data(self) -> Dict[str, List[str]]:
        """
        Validate the standards data for consistency and completeness.
        
        Returns:
            Dictionary of validation results with any issues found
        """
        issues = {}
        index = self.load_index()
        
        for standard_id in index["standards"]:
            standard_issues = []
            
            try:
                standard_data = self.load_standard(standard_id)
                
                # Check required fields
                required_fields = ["standard_id", "name", "overview", "region", "functions"]
                for field in required_fields:
                    if field not in standard_data:
                        standard_issues.append(f"Missing required field: {field}")
                
                # Check functions structure
                if "functions" in standard_data:
                    for func_name, func_data in standard_data["functions"].items():
                        if "subcategories" not in func_data:
                            standard_issues.append(f"Function {func_name} missing subcategories")
                        else:
                            for control_id, control_data in func_data["subcategories"].items():
                                control_required = ["description", "examples", "use_cases", "regional_relevance", "tech_recommendations"]
                                for field in control_required:
                                    if field not in control_data:
                                        standard_issues.append(f"Control {control_id} missing field: {field}")
                
                # Check cross-mappings
                for func_name, func_data in standard_data.get("functions", {}).items():
                    for control_id, control_data in func_data.get("subcategories", {}).items():
                        mappings = control_data.get("mappings", {})
                        for mapped_standard, mapped_control in mappings.items():
                            if mapped_standard not in index["standards"]:
                                standard_issues.append(f"Control {control_id} maps to unknown standard: {mapped_standard}")
                
            except Exception as e:
                standard_issues.append(f"Error loading standard: {e}")
            
            if standard_issues:
                issues[standard_id] = standard_issues
        
        return issues
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the standards data.
        
        Returns:
            Dictionary containing various statistics
        """
        index = self.load_index()
        stats = {
            "total_standards": len(index["standards"]),
            "standards_by_type": {},
            "standards_by_region": {},
            "total_controls": 0,
            "total_functions": 0,
            "total_mappings": 0
        }
        
        # Count by type and region
        for standard_id, metadata in index["standards"].items():
            std_type = metadata.get("type", "Unknown")
            region = metadata.get("region", "Unknown")
            
            stats["standards_by_type"][std_type] = stats["standards_by_type"].get(std_type, 0) + 1
            stats["standards_by_region"][region] = stats["standards_by_region"].get(region, 0) + 1
        
        # Count controls, functions, and mappings
        for standard_id in index["standards"]:
            try:
                standard_data = self.load_standard(standard_id)
                stats["total_functions"] += len(standard_data.get("functions", {}))
                
                for func_data in standard_data.get("functions", {}).values():
                    controls = func_data.get("subcategories", {})
                    stats["total_controls"] += len(controls)
                    
                    for control_data in controls.values():
                        mappings = control_data.get("mappings", {})
                        stats["total_mappings"] += len(mappings)
                        
            except Exception as e:
                print(f"Error processing statistics for {standard_id}: {e}")
        
        return stats

# Global instance for easy access
standards_loader = StandardsLoader()

# Convenience functions
def load_standard(standard_id: str) -> Dict[str, Any]:
    """Load a specific standard by ID."""
    return standards_loader.load_standard(standard_id)

def load_all_standards() -> Dict[str, Dict[str, Any]]:
    """Load all available standards."""
    return standards_loader.load_all_standards()

def search_controls(search_term: str, standard_ids: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
    """Search for controls across standards."""
    return standards_loader.search_controls(search_term, standard_ids)

def get_cross_mappings(control_id: str, standard_id: str) -> Dict[str, str]:
    """Get cross-mappings for a specific control."""
    return standards_loader.get_cross_mappings(control_id, standard_id)

def get_standards_by_region(region: str) -> List[str]:
    """Get standards for a specific region."""
    return standards_loader.get_standards_by_region(region)

def get_standards_by_type(standard_type: str) -> List[str]:
    """Get standards for a specific type."""
    return standards_loader.get_standards_by_type(standard_type)
