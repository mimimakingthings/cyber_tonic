"""
Enhanced Assessment Utilities for Cyber Tonic

This module provides advanced assessment features including:
- Customizable scoring weights
- Enhanced evidence management
- Advanced gap analysis with prioritization
- Trend analysis and version control preparation
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import json
import uuid
from pathlib import Path
import numpy as np
import logging

logger = logging.getLogger(__name__)

class AssessmentWeights:
    """Manage customizable scoring weights for NIST functions."""
    
    def __init__(self):
        """Initialize with default weights."""
        self.default_function_weights = {
            "ID": 1.0,  # Identify
            "PR": 1.0,  # Protect
            "DE": 1.0,  # Detect
            "RS": 1.0,  # Respond
            "RC": 1.0   # Recover
        }
        
    def get_weights(self, client_id: str) -> Dict[str, float]:
        """Get weights for a specific client."""
        # This would load from persistent storage
        return self.default_function_weights.copy()
    
    def set_weights(self, client_id: str, weights: Dict[str, float]) -> bool:
        """Set weights for a specific client."""
        # This would save to persistent storage
        return True
    
    def render_weights_interface(self, client_industry: str, current_weights: Dict[str, float] = None) -> Dict[str, float]:
        """Render Streamlit interface for weight configuration."""
        st.markdown("### ⚖️ Scoring Weights Configuration")
        
        # Use default weights if none provided
        if current_weights is None:
            current_weights = self.default_function_weights.copy()
        
        # Weight sliders
        new_weights = {}
        col1, col2 = st.columns(2)
        
        function_names = {
            "ID": "Identify", 
            "PR": "Protect",
            "DE": "Detect",
            "RS": "Respond",
            "RC": "Recover"
        }
        
        for i, (func_id, func_name) in enumerate(function_names.items()):
            with col1 if i % 2 == 0 else col2:
                weight = st.slider(
                    f"{func_name} ({func_id})",
                    min_value=0.1,
                    max_value=2.0,
                    value=current_weights.get(func_id, 1.0),
                    step=0.1,
                    help=f"Weight for {func_name} function. Higher values increase importance in overall score.",
                    key=f"weight_{func_id}"
                )
                new_weights[func_id] = weight
        
        # Reset to defaults
        if st.button("🔄 Reset to Defaults", key="reset_weights"):
            new_weights = self.default_function_weights.copy()
            st.rerun()
        
        return new_weights

class EnhancedEvidenceManager:
    """Enhanced evidence management with search and tagging capabilities."""
    
    def __init__(self):
        """Initialize evidence manager."""
        self.evidence_data = {}
    
    def add_evidence(self, client_id: str, subcategory_id: str, file_path: str, 
                    tags: List[str] = None, notes: str = "") -> str:
        """Add evidence file with metadata."""
        evidence_id = str(uuid.uuid4())
        
        evidence_entry = {
            "id": evidence_id,
            "client_id": client_id,
            "subcategory_id": subcategory_id,
            "file_path": file_path,
            "tags": tags or [],
            "notes": notes,
            "upload_date": datetime.now().isoformat(),
            "file_size": 0,  # Would be calculated
            "file_type": Path(file_path).suffix.lower()
        }
        
        if client_id not in self.evidence_data:
            self.evidence_data[client_id] = {}
        
        self.evidence_data[client_id][evidence_id] = evidence_entry
        return evidence_id
    
    def search_evidence(self, client_id: str, query: str = "", tags: List[str] = None) -> List[Dict[str, Any]]:
        """Search evidence files by query and tags."""
        if client_id not in self.evidence_data:
            return []
        
        results = []
        for evidence in self.evidence_data[client_id].values():
            # Search in notes and tags
            if query.lower() in evidence.get("notes", "").lower():
                results.append(evidence)
            elif any(tag.lower() in [t.lower() for t in evidence.get("tags", [])] for tag in (tags or [])):
                results.append(evidence)
        
        return results
    
    def get_evidence_stats(self, client_id: str) -> Dict[str, Any]:
        """Get evidence statistics for a client."""
        if client_id not in self.evidence_data:
            return {"total_files": 0, "total_size": 0, "file_types": {}}
        
        evidence_list = list(self.evidence_data[client_id].values())
        total_files = len(evidence_list)
        total_size = sum(evidence.get("file_size", 0) for evidence in evidence_list)
        
        file_types = {}
        for evidence in evidence_list:
            file_type = evidence.get("file_type", "unknown")
            file_types[file_type] = file_types.get(file_type, 0) + 1
        
        return {
            "total_files": total_files,
            "total_size": total_size,
            "file_types": file_types
        }
    
    def render_evidence_interface(self, client_id: str, subcategory_id: str) -> Dict[str, Any]:
        """Render evidence upload interface for a specific subcategory."""
        st.markdown("#### 📁 Evidence Management")
        
        # File upload
        uploaded_files = st.file_uploader(
            "Upload Evidence Files",
            type=["pdf", "docx", "doc", "png", "jpg", "jpeg", "txt"],
            accept_multiple_files=True,
            key=f"evidence_upload_{subcategory_id}",
            help="Upload evidence files for this subcategory"
        )
        
        if uploaded_files:
                # Tagging interface
            tags_input = st.text_input(
                    "Add tags (comma-separated)",
                    key=f"evidence_tags_{subcategory_id}",
                    placeholder="e.g., policy, screenshot, audit, compliance"
                )
                
            # Notes
            notes = st.text_area(
                "Evidence notes",
                key=f"evidence_notes_{subcategory_id}",
                placeholder="Add notes about this evidence..."
            )
            
            # Process uploaded files
            evidence_metadata = {
                "files": [file.name for file in uploaded_files],
                "tags": [tag.strip() for tag in tags_input.split(",") if tag.strip()] if tags_input else [],
                "notes": notes,
                "upload_date": datetime.now().isoformat(),
                "subcategory_id": subcategory_id
            }
            
            return evidence_metadata
        
        return None
    
    def render_evidence_search(self, evidence_df: pd.DataFrame):
        """Render evidence search interface."""
        if evidence_df.empty:
            st.warning("No evidence files match your search criteria.")
            return
        
        st.markdown(f"**Found {len(evidence_df)} evidence files**")
        
        # Display evidence files
        for _, evidence in evidence_df.iterrows():
            with st.expander(f"📄 {evidence['file_path']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Subcategory:** {evidence['subcategory_id']}")
                    st.write(f"**Upload Date:** {evidence['upload_date']}")
                    if evidence['notes']:
                        st.write(f"**Notes:** {evidence['notes']}")
                
                with col2:
                    st.write(f"**Size:** {evidence['file_size']} bytes")
                    st.write(f"**Type:** {evidence['file_type']}")
                    if evidence['tags']:
                        st.write("**Tags:**")
                        for tag in evidence['tags']:
                            st.write(f"- {tag}")

class AdvancedGapAnalysis:
    """Advanced gap analysis with prioritization and trend analysis."""
    
    def __init__(self):
        """Initialize gap analysis."""
        self.priority_thresholds = {
            "Critical": 3,    # Score < 3
            "High": 5,        # Score 3-4
            "Medium": 7,      # Score 5-6
            "Low": 10         # Score 7-10
        }
    
    def calculate_priority_score(self, score: float, weights: Dict[str, float] = None) -> str:
        """Calculate priority level based on score and weights."""
        if weights:
            # Apply weight adjustment
            adjusted_score = score * (weights.get("function_weight", 1.0))
        else:
            adjusted_score = score
        
        if adjusted_score < 3:
            return "Critical"
        elif adjusted_score < 5:
            return "High"
        elif adjusted_score < 7:
            return "Medium"
        else:
            return "Low"
    
    def analyze_gaps_with_weights(self, assessments: Dict[str, Any], weights: Dict[str, float], 
                                nist_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze gaps considering function weights."""
        gap_data = []
        
        for function in nist_data["functions"]:
            function_id = function["id"]
            function_weight = weights.get(function_id, 1.0)
            
            for category in function["categories"]:
                for subcategory in category["subcategories"]:
                    subcat_id = subcategory["id"]
                    
                    if subcat_id in assessments:
                        assessment = assessments[subcat_id]
                        score = assessment.get("score", 0)
                        status = assessment.get("status", "Not Implemented")
                        
                        # Calculate weighted priority
                        priority = self.calculate_priority_score(score, {"function_weight": function_weight})
                        
                        # Determine if this is a gap
                        is_gap = (
                            status in ["Not Implemented", "Partially Implemented"] or
                            score < 5 or
                            priority in ["Critical", "High"]
                        )
                        
                        if is_gap:
                            gap_data.append({
                                "Priority": priority,
                                "Function": function["name"],
                                "Function_ID": function_id,
                                "Category": category["name"],
                                "Subcategory_ID": subcat_id,
                                "Description": subcategory["description"],
                                "Current_Status": status,
                                "Current_Score": score,
                                "Weighted_Score": score * function_weight,
                                "Function_Weight": function_weight,
                                "Remediation_Urgency": self._get_remediation_urgency(priority, score),
                                "Notes": assessment.get("notes", "")
                            })
        
        return gap_data
    
    def _get_remediation_urgency(self, priority: str, score: float) -> str:
        """Get remediation urgency based on priority and score."""
        if priority == "Critical" or score < 2:
            return "Immediate"
        elif priority == "High" or score < 4:
            return "High"
        elif priority == "Medium":
            return "Medium"
        else:
            return "Low"
    
    def create_priority_pie_chart(self, gap_data: List[Dict[str, Any]]) -> go.Figure:
        """Create priority distribution pie chart with pastel colors."""
        if not gap_data:
            return self._create_empty_chart("No gaps found!")
        
        df = pd.DataFrame(gap_data)
        priority_counts = df["Priority"].value_counts()
        
        # Sort by priority order for consistent display
        priority_order = ["Critical", "High", "Medium", "Low"]
        priority_counts = priority_counts.reindex([p for p in priority_order if p in priority_counts.index])
        
        # Pastel colors
        pastel_colors = {
            "Critical": "#FF9999",  # Pastel Red
            "High": "#FFCC99",      # Pastel Orange
            "Medium": "#FFFF99",    # Pastel Yellow
            "Low": "#99FF99"        # Pastel Green
        }
        
        # Create pull effect for Critical slice
        pull_values = [0.1 if priority == "Critical" else 0 for priority in priority_counts.index]
        
        fig = go.Figure(data=[go.Pie(
            labels=priority_counts.index,
            values=priority_counts.values,
            marker_colors=[pastel_colors.get(p, "#CCCCCC") for p in priority_counts.index],
            textinfo='percent+label',
            textposition='inside',
            pull=pull_values,
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(
                text="🔴 Priority Distribution",
                x=0.5,
                font=dict(size=16, color="#1F2937")
            ),
            margin=dict(l=20, r=20, t=40, b=20),
            font=dict(size=12),
            showlegend=False,
            height=400
        )
        
        return fig
    
    def create_function_bar_chart(self, gap_data: List[Dict[str, Any]]) -> go.Figure:
        """Create gaps by function bar chart with pastel gradient coloring."""
        if not gap_data:
            return self._create_empty_chart("No gaps found!")
        
        df = pd.DataFrame(gap_data)
        function_counts = df["Function"].value_counts().sort_values(ascending=True)
        
        # Calculate average priority per function for gradient coloring
        function_avg_priority = df.groupby("Function")["Current_Score"].mean()
        
        # Pastel colors
        pastel_colors = {
            "Critical": "#FF9999",  # Pastel Red
            "High": "#FFCC99",      # Pastel Orange
            "Medium": "#FFFF99",    # Pastel Yellow
            "Low": "#99FF99"        # Pastel Green
        }
        
        # Create gradient colors based on average priority
        colors = []
        for func in function_counts.index:
            avg_score = function_avg_priority[func]
            if avg_score < 3:
                colors.append(pastel_colors["Critical"])
            elif avg_score < 5:
                colors.append(pastel_colors["High"])
            elif avg_score < 7:
                colors.append(pastel_colors["Medium"])
            else:
                colors.append(pastel_colors["Low"])
        
        fig = go.Figure(data=[go.Bar(
            y=function_counts.index,
            x=function_counts.values,
            marker_color=colors,
            text=function_counts.values,
            textposition='outside',
            orientation='h',
            hovertemplate='<b>%{y}</b><br>Gap Count: %{x}<br>Avg Score: %{customdata:.1f}<extra></extra>',
            customdata=[function_avg_priority[func] for func in function_counts.index]
        )])
        
        fig.update_layout(
            title=dict(
                text="📊 Gaps by NIST Function",
                x=0.5,
                font=dict(size=16, color="#1F2937")
            ),
            margin=dict(l=160, r=20, t=40, b=20),
            font=dict(size=12),
            bargap=0.2,
            height=400
        )
        
        return fig
    
    def create_score_histogram(self, gap_data: List[Dict[str, Any]]) -> go.Figure:
        """Create score distribution histogram with pastel colors."""
        if not gap_data:
            return self._create_empty_chart("No gaps found!")
        
        df = pd.DataFrame(gap_data)
        
        fig = go.Figure(data=[go.Histogram(
            x=df["Current_Score"],
            nbinsx=15,
            marker_color="#FFFF99",  # Pastel Yellow
            opacity=0.7,
            hovertemplate='<b>Score Range</b><br>Count: %{y}<br>Score: %{x}<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(
                text="📈 Score Distribution",
                x=0.5,
                font=dict(size=16, color="#1F2937")
            ),
            margin=dict(l=20, r=20, t=40, b=20),
            font=dict(size=12),
            bargap=0.1,
            height=400
        )
        
        return fig
    
    def create_urgency_bar_chart(self, gap_data: List[Dict[str, Any]]) -> go.Figure:
        """Create remediation urgency bar chart with pastel colors."""
        if not gap_data:
            return self._create_empty_chart("No gaps found!")
        
        df = pd.DataFrame(gap_data)
        urgency_counts = df["Remediation_Urgency"].value_counts()
        
        # Sort by urgency order
        urgency_order = ["Immediate", "High", "Medium", "Low"]
        urgency_counts = urgency_counts.reindex([u for u in urgency_order if u in urgency_counts.index])
        
        # Pastel colors
        pastel_colors = {
            "Critical": "#FF9999",  # Pastel Red
            "High": "#FFCC99",      # Pastel Orange
            "Medium": "#FFFF99",    # Pastel Yellow
            "Low": "#99FF99"        # Pastel Green
        }
        
        # Map urgency to pastel colors
        urgency_colors = {
            "Immediate": pastel_colors["Critical"],
            "High": pastel_colors["High"],
            "Medium": pastel_colors["Medium"],
            "Low": pastel_colors["Low"]
        }
        
        fig = go.Figure(data=[go.Bar(
            x=urgency_counts.index,
            y=urgency_counts.values,
            marker_color=[urgency_colors.get(u, "#CCCCCC") for u in urgency_counts.index],
            text=urgency_counts.values,
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(
                text="⚡ Remediation Urgency",
                x=0.5,
                font=dict(size=16, color="#1F2937")
            ),
            margin=dict(l=20, r=20, t=40, b=20),
            font=dict(size=12),
            bargap=0.2,
            height=400
        )
        
        return fig
    
    def create_gap_analysis_chart(self, gap_data: List[Dict[str, Any]]) -> go.Figure:
        """Create enhanced gap analysis visualization with improved aesthetics and interactivity."""
        if not gap_data:
            # Return empty chart with better styling
            fig = go.Figure()
            fig.add_annotation(
                text="🎉 No gaps found!<br>Your security posture looks excellent!",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=24, color="#10b981"),
                bgcolor="rgba(16, 185, 129, 0.1)",
                bordercolor="#10b981",
                borderwidth=2
            )
            fig.update_layout(
                height=400,
                paper_bgcolor="white",
                plot_bgcolor="white"
            )
            return fig
        
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame(gap_data)
        
        # Enhanced color palette - colorblind friendly
        priority_colors = {
            "Critical": "#DC2626",  # Red
            "High": "#EA580C",      # Orange  
            "Medium": "#D97706",    # Amber
            "Low": "#059669"        # Green
        }
        
        urgency_colors = {
            "Immediate": "#DC2626",
            "High": "#EA580C", 
            "Medium": "#D97706",
            "Low": "#059669"
        }
        
        # Create subplot figure with better spacing
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "🔴 Priority Distribution",
                "📊 Gaps by NIST Function", 
                "📈 Score Distribution",
                "⚡ Remediation Urgency"
            ),
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "histogram"}, {"type": "bar"}]],
            vertical_spacing=0.12,
            horizontal_spacing=0.08
        )
        
        # 1. Enhanced Priority pie chart
        priority_counts = df["Priority"].value_counts()
        # Sort by priority order for consistent display
        priority_order = ["Critical", "High", "Medium", "Low"]
        priority_counts = priority_counts.reindex([p for p in priority_order if p in priority_counts.index])
        
        # Create pull effect for largest slice
        pull_values = [0.1 if i == 0 else 0 for i in range(len(priority_counts))]
        
        fig.add_trace(
            go.Pie(
                labels=priority_counts.index,
                values=priority_counts.values,
                name="Priority",
                marker_colors=[priority_colors.get(p, "#6B7280") for p in priority_counts.index],
                textinfo='label+percent',
                textposition='outside',
                pull=pull_values,
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # 2. Enhanced Gaps by function - sorted and with gradient coloring
        function_counts = df["Function"].value_counts().sort_values(ascending=True)
        
        # Calculate average priority per function for gradient coloring
        function_avg_priority = df.groupby("Function")["Current_Score"].mean()
        function_colors = []
        for func in function_counts.index:
            avg_score = function_avg_priority[func]
            if avg_score < 3:
                color = "#DC2626"  # Critical
            elif avg_score < 5:
                color = "#EA580C"  # High
            elif avg_score < 7:
                color = "#D97706"  # Medium
            else:
                color = "#059669"  # Low
            function_colors.append(color)
        
        fig.add_trace(
            go.Bar(
                y=function_counts.index,
                x=function_counts.values,
                name="Function Gaps",
                marker_color=function_colors,
                text=function_counts.values,
                textposition='outside',
                orientation='h',
                hovertemplate='<b>%{y}</b><br>Gap Count: %{x}<br>Avg Score: %{customdata:.1f}<extra></extra>',
                customdata=[function_avg_priority[func] for func in function_counts.index]
            ),
            row=1, col=2
        )
        
        # 3. Enhanced Score distribution with KDE overlay
        fig.add_trace(
            go.Histogram(
                x=df["Current_Score"],
                nbinsx=15,
                name="Score Distribution",
                marker_color="#3B82F6",
                opacity=0.7,
                hovertemplate='<b>Score Range</b><br>Count: %{y}<br>Score: %{x}<extra></extra>'
            ),
            row=2, col=1
        )
        
        # 4. Enhanced Remediation urgency - stacked by priority
        urgency_priority = df.groupby(["Remediation_Urgency", "Priority"]).size().unstack(fill_value=0)
        urgency_order = ["Immediate", "High", "Medium", "Low"]
        urgency_priority = urgency_priority.reindex([u for u in urgency_order if u in urgency_priority.index])
        
        for priority in priority_order:
            if priority in urgency_priority.columns:
                fig.add_trace(
                    go.Bar(
                        x=urgency_priority.index,
                        y=urgency_priority[priority],
                        name=f"{priority} Priority",
                        marker_color=priority_colors[priority],
                        hovertemplate=f'<b>{priority} Priority</b><br>Urgency: %{{x}}<br>Count: %{{y}}<extra></extra>'
                    ),
                    row=2, col=2
                )
        
        # Enhanced layout with professional styling
        fig.update_layout(
            height=900,
            title=dict(
                text="🔍 Advanced Gap Analysis Dashboard",
                x=0.5,
                font=dict(size=24, color="#1F2937")
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(family="Arial, sans-serif", size=12, color="#374151")
        )
        
        # Update axes for better readability
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)')
        
        # Update subplot titles
        fig.update_annotations(font_size=14, font_color="#1F2937")
        
        return fig
    
    def create_nist_maturity_radar(self, assessments: Dict[str, Any], nist_data: Dict[str, Any], 
                                 target_scores: Dict[str, float] = None) -> go.Figure:
        """Create radar chart showing NIST function maturity vs targets."""
        # Calculate average scores per function
        function_scores = {}
        function_names = {}
        
        for function in nist_data["functions"]:
            function_id = function["id"]
            function_name = function["name"]
            function_names[function_id] = function_name
            
            scores = []
            for category in function["categories"]:
                for subcategory in category["subcategories"]:
                    subcat_id = subcategory["id"]
                    if subcat_id in assessments:
                        scores.append(assessments[subcat_id].get("score", 0))
            
            function_scores[function_id] = sum(scores) / len(scores) if scores else 0
        
        # Set default target scores if not provided
        if not target_scores:
            target_scores = {func_id: 8.0 for func_id in function_scores.keys()}
        
        # Create radar chart
        fig = go.Figure()
        
        # Current scores
        fig.add_trace(go.Scatterpolar(
            r=[function_scores[func_id] for func_id in function_scores.keys()],
            theta=[function_names[func_id] for func_id in function_scores.keys()],
            fill='toself',
            name='Current Maturity',
            line_color='#3B82F6',
            fillcolor='rgba(59, 130, 246, 0.3)'
        ))
        
        # Target scores
        fig.add_trace(go.Scatterpolar(
            r=[target_scores.get(func_id, 8.0) for func_id in function_scores.keys()],
            theta=[function_names[func_id] for func_id in function_scores.keys()],
            fill='toself',
            name='Target Maturity',
            line_color='#10B981',
            fillcolor='rgba(16, 185, 129, 0.1)',
            line_dash='dash'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    tickvals=[0, 2, 4, 6, 8, 10],
                    ticktext=['0', '2', '4', '6', '8', '10'],
                    gridcolor='rgba(128, 128, 128, 0.3)'
                ),
                angularaxis=dict(
                    gridcolor='rgba(128, 128, 128, 0.3)'
                )
            ),
            title=dict(
                text="🎯 NIST Cybersecurity Framework Maturity",
                x=0.5,
                font=dict(size=20, color="#1F2937")
            ),
            height=500,
            paper_bgcolor="white",
            plot_bgcolor="white"
        )
        
        return fig
    
    def create_remediation_waterfall(self, gap_data: List[Dict[str, Any]]) -> go.Figure:
        """Create waterfall chart showing remediation impact on overall risk score."""
        if not gap_data:
            return self._create_empty_chart("No gaps to remediate!")
        
        df = pd.DataFrame(gap_data)
        
        # Calculate potential score improvements
        df['potential_improvement'] = df.apply(
            lambda row: min(10 - row['Current_Score'], 3), axis=1
        )
        
        # Group by priority for waterfall
        priority_impact = df.groupby('Priority')['potential_improvement'].sum().sort_index(
            key=lambda x: x.map({"Critical": 0, "High": 1, "Medium": 2, "Low": 3})
        )
        
        # Create waterfall data
        measures = ['relative'] * len(priority_impact) + ['total']
        values = list(priority_impact.values) + [priority_impact.sum()]
        text = [f"{priority}<br>+{val:.1f}" for priority, val in priority_impact.items()] + [f"Total<br>+{priority_impact.sum():.1f}"]
        
        fig = go.Figure(go.Waterfall(
            name="Remediation Impact",
            orientation="v",
            measure=measures,
            x=[f"Fix {priority}" for priority in priority_impact.index] + ["Total Impact"],
            textposition="outside",
            text=text,
            y=values,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": "#10B981"}},
            decreasing={"marker": {"color": "#EF4444"}},
            totals={"marker": {"color": "#3B82F6"}}
        ))
        
        fig.update_layout(
            title=dict(
                text="💧 Remediation Impact Analysis",
                x=0.5,
                font=dict(size=20, color="#1F2937")
            ),
            height=500,
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis_title="Remediation Actions",
            yaxis_title="Score Improvement"
        )
        
        return fig
    
    def create_trend_analysis(self, assessment_history: List[Dict[str, Any]]) -> go.Figure:
        """Create trend analysis chart showing progress over time."""
        if len(assessment_history) < 2:
            return self._create_empty_chart("Insufficient data for trend analysis")
        
        # Convert to DataFrame
        df = pd.DataFrame(assessment_history)
        df['date'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('date')
        
        # Create trend chart
        fig = go.Figure()
        
        # Overall trend
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['overall_score'],
            mode='lines+markers',
            name='Overall Score',
            line=dict(color='#3B82F6', width=3),
            marker=dict(size=8, color='#3B82F6')
        ))
        
        # Add trend line
        z = np.polyfit(range(len(df)), df['overall_score'], 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=p(range(len(df))),
            mode='lines',
            name='Trend Line',
            line=dict(color='#EF4444', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title=dict(
                text="📈 Security Maturity Trends",
                x=0.5,
                font=dict(size=20, color="#1F2937")
            ),
            height=400,
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis_title="Assessment Date",
            yaxis_title="Overall Score",
            hovermode='x unified'
        )
        
        return fig
    
    def _create_empty_chart(self, message: str) -> go.Figure:
        """Create an empty chart with a message."""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="#6B7280")
        )
        fig.update_layout(
            height=400,
            paper_bgcolor="white",
            plot_bgcolor="white"
        )
        return fig
    
    def analyze_trends(self, assessment_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze trends across assessment history."""
        if len(assessment_history) < 2:
            return {"message": "Insufficient data for trend analysis"}
        
        # Convert to DataFrame
        df = pd.DataFrame(assessment_history)
        df['date'] = pd.to_datetime(df['timestamp'])
        
        # Calculate trends
        trends = {}
        
        # Overall score trend
        if 'overall_score' in df.columns:
            trend_slope = df['overall_score'].diff().mean()
            trends['overall_trend'] = {
                'direction': 'improving' if trend_slope > 0 else 'declining' if trend_slope < 0 else 'stable',
                'rate': abs(trend_slope),
                'latest_score': df['overall_score'].iloc[-1]
            }
        
        # Function-level trends
        function_columns = [col for col in df.columns if col.startswith('function_')]
        for func_col in function_columns:
            if func_col in df.columns:
                trend_slope = df[func_col].diff().mean()
                trends[func_col] = {
                    'direction': 'improving' if trend_slope > 0 else 'declining' if trend_slope < 0 else 'stable',
                    'rate': abs(trend_slope)
                }
        
        return trends


# Global instances for easy access
assessment_weights = AssessmentWeights()
evidence_manager = EnhancedEvidenceManager()
gap_analyzer = AdvancedGapAnalysis()
