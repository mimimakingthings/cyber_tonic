"""
Pytest tests for assessment enhancements.

Tests for:
- Customizable scoring weights
- Enhanced evidence management
- Advanced gap analysis
- Data persistence enhancements
"""

import pytest
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from assessment_enhancements import (
    AssessmentWeights,
    EnhancedEvidenceManager,
    AdvancedGapAnalysis
)
from data_persistence import DataPersistence


class TestAssessmentWeights:
    """Test cases for AssessmentWeights class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.weights = AssessmentWeights()
    
    def test_default_weights(self):
        """Test default weights initialization."""
        assert len(self.weights.default_function_weights) == 6
        assert all(weight == 1.0 for weight in self.weights.default_function_weights.values())
    
    def test_industry_presets(self):
        """Test industry-specific weight presets."""
        finance_weights = self.weights.get_weights_for_industry("Finance")
        assert finance_weights["PR"] > 1.0  # Protection should be higher for finance
        assert finance_weights["GV"] > 1.0  # Governance should be higher for finance
        
        healthcare_weights = self.weights.get_weights_for_industry("Healthcare")
        assert healthcare_weights["ID"] > 1.0  # Asset identification important for healthcare
    
    def test_unknown_industry(self):
        """Test handling of unknown industry."""
        unknown_weights = self.weights.get_weights_for_industry("UnknownIndustry")
        assert unknown_weights == self.weights.default_function_weights
    
    def test_calculate_weighted_score(self):
        """Test weighted score calculation."""
        scores = {"GV": 8.0, "ID": 6.0, "PR": 4.0}
        weights = {"GV": 1.0, "ID": 1.2, "PR": 1.5}
        
        weighted_score = self.weights.calculate_weighted_score(scores, weights)
        expected = (8.0 * 1.0 + 6.0 * 1.2 + 4.0 * 1.5) / (1.0 + 1.2 + 1.5)
        assert abs(weighted_score - expected) < 0.01
    
    def test_calculate_weighted_score_empty(self):
        """Test weighted score calculation with empty inputs."""
        assert self.weights.calculate_weighted_score({}, {}) == 0.0
        assert self.weights.calculate_weighted_score(None, None) == 0.0


class TestEnhancedEvidenceManager:
    """Test cases for EnhancedEvidenceManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.evidence_manager = EnhancedEvidenceManager()
    
    def test_supported_formats(self):
        """Test supported file formats."""
        expected_formats = [".pdf", ".docx", ".doc", ".png", ".jpg", ".jpeg", ".txt"]
        assert self.evidence_manager.supported_formats == expected_formats
    
    def test_max_file_size(self):
        """Test maximum file size limit."""
        assert self.evidence_manager.max_file_size == 20 * 1024 * 1024  # 20MB
    
    def test_create_evidence_dataframe(self):
        """Test evidence DataFrame creation."""
        evidence_data = {
            "client1": {
                "GV.OC-01": {
                    "files": ["policy.pdf", "audit.docx"],
                    "tags": ["policy", "compliance"],
                    "upload_date": "2025-01-01T10:00:00",
                    "subcategory_id": "GV.OC-01"
                }
            }
        }
        
        df = self.evidence_manager.create_evidence_dataframe(evidence_data)
        
        assert not df.empty
        assert len(df) == 1
        assert df.iloc[0]["File"] == "policy.pdf"
        assert df.iloc[0]["Tags"] == "policy, compliance"
        assert df.iloc[0]["Subcategory"] == "GV.OC-01"
    
    def test_create_evidence_dataframe_empty(self):
        """Test evidence DataFrame creation with empty data."""
        df = self.evidence_manager.create_evidence_dataframe({})
        assert df.empty
    
    def test_create_evidence_dataframe_multiple_files(self):
        """Test evidence DataFrame creation with multiple files."""
        evidence_data = {
            "client1": {
                "GV.OC-01": {
                    "files": ["file1.pdf", "file2.docx", "file3.png"],
                    "tags": ["policy", "audit"],
                    "upload_date": "2025-01-01T10:00:00",
                    "subcategory_id": "GV.OC-01"
                }
            }
        }
        
        df = self.evidence_manager.create_evidence_dataframe(evidence_data)
        
        assert not df.empty
        assert df.iloc[0]["File Count"] == 3


class TestAdvancedGapAnalysis:
    """Test cases for AdvancedGapAnalysis class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.gap_analyzer = AdvancedGapAnalysis()
    
    def test_priority_thresholds(self):
        """Test priority threshold configuration."""
        expected_thresholds = {
            "Critical": 3,
            "High": 5,
            "Medium": 7,
            "Low": 10
        }
        assert self.gap_analyzer.priority_thresholds == expected_thresholds
    
    def test_calculate_priority_score(self):
        """Test priority score calculation."""
        assert self.gap_analyzer.calculate_priority_score(2.0) == "Critical"
        assert self.gap_analyzer.calculate_priority_score(4.0) == "High"
        assert self.gap_analyzer.calculate_priority_score(6.0) == "Medium"
        assert self.gap_analyzer.calculate_priority_score(8.0) == "Low"
    
    def test_calculate_priority_score_with_weights(self):
        """Test priority score calculation with weights."""
        weights = {"function_weight": 1.5}
        # Score 2.0 * weight 1.5 = 3.0, which is still Critical
        assert self.gap_analyzer.calculate_priority_score(2.0, weights) == "Critical"
    
    def test_get_remediation_urgency(self):
        """Test remediation urgency calculation."""
        assert self.gap_analyzer._get_remediation_urgency("Critical", 1.0) == "Immediate"
        assert self.gap_analyzer._get_remediation_urgency("High", 3.0) == "High"
        assert self.gap_analyzer._get_remediation_urgency("Medium", 5.0) == "Medium"
        assert self.gap_analyzer._get_remediation_urgency("Low", 7.0) == "Low"
    
    def test_analyze_gaps_with_weights(self):
        """Test gap analysis with weights."""
        assessments = {
            "GV.OC-01": {
                "score": 2.0,
                "status": "Not Implemented",
                "notes": "Test notes"
            }
        }
        
        weights = {"GV": 1.2}
        
        nist_data = {
            "functions": [
                {
                    "id": "GV",
                    "name": "Govern",
                    "categories": [
                        {
                            "id": "GV.OC",
                            "name": "Organizational Context",
                            "subcategories": [
                                {
                                    "id": "GV.OC-01",
                                    "description": "Test subcategory"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        gap_data = self.gap_analyzer.analyze_gaps_with_weights(assessments, weights, nist_data)
        
        assert len(gap_data) == 1
        assert gap_data[0]["Priority"] == "Critical"
        assert gap_data[0]["Function_Weight"] == 1.2
        assert gap_data[0]["Weighted_Score"] == 2.4  # 2.0 * 1.2
    
    def test_analyze_trends_insufficient_data(self):
        """Test trend analysis with insufficient data."""
        history = [{"timestamp": "2025-01-01", "overall_score": 5.0}]
        trends = self.gap_analyzer.analyze_trends(history)
        assert "message" in trends
        assert "Insufficient data" in trends["message"]
    
    def test_analyze_trends_sufficient_data(self):
        """Test trend analysis with sufficient data."""
        history = [
            {"timestamp": "2025-01-01", "overall_score": 5.0, "function_GV": 4.0},
            {"timestamp": "2025-01-02", "overall_score": 6.0, "function_GV": 5.0},
            {"timestamp": "2025-01-03", "overall_score": 7.0, "function_GV": 6.0}
        ]
        
        trends = self.gap_analyzer.analyze_trends(history)
        
        assert "overall_trend" in trends
        assert trends["overall_trend"]["direction"] == "improving"
        assert trends["overall_trend"]["latest_score"] == 7.0


class TestDataPersistenceEnhancements:
    """Test cases for enhanced data persistence functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Use a temporary directory for testing
        self.test_dir = Path(__file__).parent / "test_data"
        self.test_dir.mkdir(exist_ok=True)
        self.data_persistence = DataPersistence(str(self.test_dir))
    
    def teardown_method(self):
        """Clean up test data."""
        import shutil
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_save_assessment_weights(self):
        """Test saving assessment weights."""
        client_id = "test_client"
        weights = {"GV": 1.2, "ID": 1.0, "PR": 1.5}
        
        result = self.data_persistence.save_assessment_weights(client_id, weights)
        assert result is True
        
        # Verify weights were saved
        loaded_weights = self.data_persistence.load_assessment_weights(client_id)
        assert loaded_weights == weights
    
    def test_load_assessment_weights_nonexistent(self):
        """Test loading weights for non-existent client."""
        weights = self.data_persistence.load_assessment_weights("nonexistent_client")
        assert weights == {}
    
    def test_save_evidence_metadata(self):
        """Test saving evidence metadata."""
        client_id = "test_client"
        subcategory_id = "GV.OC-01"
        metadata = {
            "files": ["test.pdf"],
            "tags": ["policy", "compliance"],
            "upload_date": "2025-01-01T10:00:00"
        }
        
        result = self.data_persistence.save_evidence_metadata(client_id, subcategory_id, metadata)
        assert result is True
    
    def test_create_assessment_snapshot(self):
        """Test creating assessment snapshot."""
        client_id = "test_client"
        snapshot_data = {
            "overall_score": 6.5,
            "function_scores": {"GV": 7.0, "ID": 6.0}
        }
        
        result = self.data_persistence.create_assessment_snapshot(client_id, snapshot_data)
        assert result is True
        
        # Verify snapshot was created
        assessments = self.data_persistence.load_assessments()
        assert "snapshots" in assessments[client_id]
        assert len(assessments[client_id]["snapshots"]) == 1
        assert assessments[client_id]["snapshots"][0]["data"] == snapshot_data


class TestIntegration:
    """Integration tests for assessment enhancements."""
    
    def test_weights_and_gap_analysis_integration(self):
        """Test integration between weights and gap analysis."""
        weights_manager = AssessmentWeights()
        gap_analyzer = AdvancedGapAnalysis()
        
        # Test with finance industry weights
        finance_weights = weights_manager.get_weights_for_industry("Finance")
        
        # Simulate assessment data
        assessments = {
            "PR.AC-01": {"score": 3.0, "status": "Partially Implemented"},
            "GV.OC-01": {"score": 2.0, "status": "Not Implemented"}
        }
        
        nist_data = {
            "functions": [
                {
                    "id": "PR",
                    "name": "Protect",
                    "categories": [
                        {
                            "id": "PR.AC",
                            "name": "Access Control",
                            "subcategories": [
                                {"id": "PR.AC-01", "description": "Test access control"}
                            ]
                        }
                    ]
                },
                {
                    "id": "GV",
                    "name": "Govern",
                    "categories": [
                        {
                            "id": "GV.OC",
                            "name": "Organizational Context",
                            "subcategories": [
                                {"id": "GV.OC-01", "description": "Test governance"}
                            ]
                        }
                    ]
                }
            ]
        }
        
        gap_data = gap_analyzer.analyze_gaps_with_weights(assessments, finance_weights, nist_data)
        
        assert len(gap_data) == 2
        
        # Check that PR (Protect) has higher weight in finance
        pr_gap = next(g for g in gap_data if g["Function_ID"] == "PR")
        gv_gap = next(g for g in gap_data if g["Function_ID"] == "GV")
        
        assert pr_gap["Function_Weight"] > gv_gap["Function_Weight"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
