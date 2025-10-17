"""
Enhanced Sidebar Component for Cyber Tonic Client Portal

A comprehensive sidebar component that provides clear client context, navigation,
and data management features with improved UX and accessibility.
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Any, Optional
import json

class CyberTonicSidebar:
    """Enhanced sidebar component for Cyber Tonic application."""
    
    def __init__(self):
        """Initialize the sidebar component."""
        self.industry_icons = {
            "Finance": "🏦",
            "Healthcare": "🏥", 
            "Manufacturing": "🏭",
            "IT": "💻",
            "Government": "🏛️",
            "Education": "🎓",
            "Retail": "🛍️",
            "Other": "🏢"
        }
        
        self.navigation_items = [
            {"id": "assessment", "label": "Assessment Dashboard", "icon": "📊", "page": "Assessment Dashboard"},
            {"id": "onboarding", "label": "Client Onboarding", "icon": "👥", "page": "Client Onboarding"},
            {"id": "data_management", "label": "Data Management", "icon": "💼", "page": "Data Management"}
        ]
        
        self.data_actions = [
            {"id": "export_all", "label": "Export All Data", "icon": "📥"},
            {"id": "export_clients", "label": "Export Clients", "icon": "👥"},
            {"id": "export_assessments", "label": "Export Assessments", "icon": "📊"},
            {"id": "storage_info", "label": "Storage Info", "icon": "💾"}
        ]
    
    def render(self, current_page: str = "Assessment Dashboard"):
        """
        Render the complete sidebar component.
        
        Args:
            current_page: The currently active page
        """
        # Initialize sidebar state
        self._initialize_sidebar_state()
        
        # Render sidebar sections
        self._render_header()
        self._render_client_context()
        self._render_deletion_confirmation()  # Add deletion confirmation dialog
        self._render_navigation(current_page)
        self._render_data_actions()
        self._render_collapse_toggle()
        
        # Add custom CSS for enhanced styling
        self._inject_custom_css()
    
    def _initialize_sidebar_state(self):
        """Initialize sidebar-specific session state variables."""
        if "sidebar_collapsed" not in st.session_state:
            st.session_state.sidebar_collapsed = False
        if "client_info_expanded" not in st.session_state:
            st.session_state.client_info_expanded = False
        if "navigation_search" not in st.session_state:
            st.session_state.navigation_search = ""
    
    def _render_header(self):
        """Render the app header with logo and title."""
        st.markdown("""
        <div class="sidebar-header">
            <h1 class="app-title">
                <a href="#" onclick="window.location.reload()" class="app-link">
                    🛡️ Cyber Tonic
                </a>
            </h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    def _render_client_context(self):
        """Render the client context section with selector and info."""
        st.markdown("### 🏢 Client Context")
        
        # Get clients from session state
        clients = st.session_state.get("clients", [])
        
        if not clients:
            st.warning("No clients available")
            if st.button("➕ Add New Client", key="add_client_from_sidebar", use_container_width=True):
                st.session_state.onboarding_step = 0
                st.rerun()
            return
        
        # Client selector with enhanced display
        selected_client_id = st.session_state.get("selected_client")
        if not selected_client_id or selected_client_id not in [c["id"] for c in clients]:
            selected_client_id = clients[0]["id"] if clients else None
            st.session_state.selected_client = selected_client_id
        
        if selected_client_id:
            selected_client = next((c for c in clients if c["id"] == selected_client_id), None)
            
            if selected_client:
                # Client selector dropdown
                client_options = {}
                for client in clients:
                    industry_icon = self.industry_icons.get(client.get("industry", "Other"), "🏢")
                    display_name = f"{industry_icon} {client['name']} ({client.get('industry', 'Unknown')})"
                    client_options[client["id"]] = display_name
                
                new_selection = st.selectbox(
                    "Select Active Client",
                    options=list(client_options.keys()),
                    format_func=lambda x: client_options[x],
                    index=list(client_options.keys()).index(selected_client_id) if selected_client_id in client_options else 0,
                    key="client_selector_sidebar"
                )
                
                # Update selected client if changed
                if new_selection != selected_client_id:
                    st.session_state.selected_client = new_selection
                    st.rerun()
                
                # Client info card
                self._render_client_info_card(selected_client, selected_client_id)
                
                # Last saved indicator
                self._render_last_saved_indicator()
        
        st.markdown("---")
    
    def _render_client_info_card(self, client: Dict[str, Any], client_id: str):
        """Render client information card with delete functionality."""
        industry_icon = self.industry_icons.get(client.get("industry", "Other"), "🏢")
        
        # Expandable client info
        with st.expander(f"📋 {client['name']} Details", expanded=st.session_state.client_info_expanded):
            st.markdown(f"""
            <div class="client-info-card">
                <div class="client-info-row">
                    <span class="client-info-label">Name:</span>
                    <span class="client-info-value">{client['name']}</span>
                </div>
                <div class="client-info-row">
                    <span class="client-info-label">Industry:</span>
                    <span class="client-info-value">{industry_icon} {client.get('industry', 'Unknown')}</span>
                </div>
                <div class="client-info-row">
                    <span class="client-info-label">Size:</span>
                    <span class="client-info-value">{client.get('size', 'Unknown')}</span>
                </div>
                <div class="client-info-row">
                    <span class="client-info-label">Contact:</span>
                    <span class="client-info-value">{client.get('contact', {}).get('email', 'N/A')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick actions
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✏️ Edit", key="edit_client_sidebar", use_container_width=True):
                    self._handle_client_edit(client, client_id)
            
            with col2:
                if st.button("🆕 New Assessment", key="new_assessment_sidebar", use_container_width=True):
                    self._handle_new_assessment(client_id)
            
            with col3:
                if st.button("🗑️ Delete", key=f"delete_client_{client_id}", use_container_width=True, type="secondary"):
                    self._handle_client_deletion(client, client_id)
    
    def _handle_client_edit(self, client: Dict[str, Any], client_id: str):
        """Handle client editing by setting up the form with existing data."""
        # Set up edit mode
        st.session_state.editing_client_id = client_id
        st.session_state.editing_client = True
        
        # Populate form data with existing client data
        st.session_state.client_form_data = {
            "name": client.get("name", ""),
            "industry": client.get("industry", "Finance"),
            "contact": {
                "email": client.get("contact", {}).get("email", ""),
                "phone": client.get("contact", {}).get("phone", ""),
                "primary": client.get("contact", {}).get("primary", "")
            },
            "size": client.get("size", "Small (<50)"),
            "documents": client.get("documents", []),
            "notes": client.get("notes", "")
        }
        
        # Navigate to onboarding page and reset to first step
        st.session_state.onboarding_step = 0
        st.session_state.current_page = "Client Onboarding"
        st.rerun()
    
    def _handle_new_assessment(self, client_id: str):
        """Handle creating a new assessment for the client."""
        # Initialize assessment data if it doesn't exist
        if client_id not in st.session_state.assessments:
            st.session_state.assessments[client_id] = {}
        
        # Navigate to assessment dashboard
        st.session_state.current_page = "Assessment Dashboard"
        st.session_state.selected_client = client_id
        
        # Show success message
        st.success("🆕 New assessment initialized! You can now start your NIST CSF 2.0 assessment.")
        st.rerun()
    
    def _handle_client_deletion(self, client: Dict[str, Any], client_id: str):
        """Handle client deletion with confirmation dialog."""
        # Set up deletion confirmation state
        st.session_state.deleting_client_id = client_id
        st.session_state.deleting_client_name = client.get('name', 'Unknown Client')
        st.rerun()
    
    def _render_deletion_confirmation(self):
        """Render the deletion confirmation dialog."""
        if not st.session_state.get("deleting_client_id"):
            return
        
        client_id = st.session_state.deleting_client_id
        client_name = st.session_state.deleting_client_name
        
        # Import here to avoid circular imports
        from data_persistence import delete_client_from_session
        
        # Show confirmation dialog
        st.warning(f"⚠️ **Delete Client Confirmation**")
        st.markdown(f"""
        You are about to delete **{client_name}** and all associated data including:
        - All assessment data
        - All evidence files
        - All historical records
        
        **This action cannot be undone!**
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Confirm Delete", key=f"confirm_delete_{client_id}", type="primary", use_container_width=True):
                # Perform deletion
                success = delete_client_from_session(client_id)
                
                # Clear deletion state
                st.session_state.deleting_client_id = None
                st.session_state.deleting_client_name = None
                
                if success:
                    st.success(f"✅ Successfully deleted {client_name}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ Failed to delete {client_name}. Please try again.")
        
        with col2:
            if st.button("❌ Cancel", key=f"cancel_delete_{client_id}", use_container_width=True):
                # Clear deletion state
                st.session_state.deleting_client_id = None
                st.session_state.deleting_client_name = None
                st.info("Deletion cancelled.")
                st.rerun()
    
    def _render_last_saved_indicator(self):
        """Render the last saved timestamp indicator."""
        last_save_time = st.session_state.get("last_save_time")
        if last_save_time:
            try:
                last_save = datetime.fromisoformat(last_save_time)
                formatted_time = last_save.strftime("%Y-%m-%d %H:%M:%S")
                st.markdown(f"""
                <div class="last-saved-indicator">
                    <span class="saved-icon">💾</span>
                    <span class="saved-text">Last Saved: {formatted_time}</span>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.caption("💾 Data saved")
        else:
            st.caption("💾 No recent saves")
    
    def _render_navigation(self, current_page: str):
        """Render the navigation section with search and menu items."""
        st.markdown("### 📊 Navigation")
        
        # Search bar for navigation
        search_term = st.text_input(
            "🔍 Search pages",
            value=st.session_state.navigation_search,
            placeholder="Search navigation...",
            key="nav_search_sidebar"
        )
        st.session_state.navigation_search = search_term
        
        # Filter navigation items based on search
        filtered_items = self.navigation_items
        if search_term:
            filtered_items = [
                item for item in self.navigation_items 
                if search_term.lower() in item["label"].lower()
            ]
        
        # Render navigation items
        for item in filtered_items:
            is_active = item["page"] == current_page
            self._render_navigation_item(item, is_active)
    
    def _render_navigation_item(self, item: Dict[str, Any], is_active: bool):
        """Render a single navigation item with active state styling."""
        item_id = item["id"]
        label = item["label"]
        icon = item["icon"]
        page = item["page"]
        
        # Active state styling
        if is_active:
            st.markdown(f"""
            <div class="nav-item nav-item-active">
                <span class="nav-icon">{icon}</span>
                <span class="nav-label nav-label-active">{label}</span>
                <span class="nav-indicator">●</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Clickable navigation item
            if st.button(
                f"{icon} {label}",
                key=f"nav_{item_id}",
                use_container_width=True,
                type="secondary" if not is_active else "primary"
            ):
                # Handle navigation
                if page == "Assessment Dashboard":
                    st.session_state.current_page = "Assessment Dashboard"
                elif page == "Client Onboarding":
                    st.session_state.onboarding_step = 0
                    st.session_state.current_page = "Client Onboarding"
                elif page == "Data Management":
                    st.session_state.current_page = "Data Management"
                st.rerun()
    
    def _render_data_actions(self):
        """Render the data actions section."""
        st.markdown("---")
        st.markdown("### 💾 Data Actions")
        
        # Manual save button
        if st.button("💾 Save All Data", key="manual_save_sidebar", use_container_width=True):
            from data_persistence import save_session_data
            with st.spinner("Saving data..."):
                if save_session_data():
                    st.success("✅ Data saved successfully!")
                else:
                    st.error("❌ Failed to save data")
        
        # Export options
        st.markdown("**Export Options:**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 All Data", key="export_all_sidebar", use_container_width=True):
                self._handle_export_all()
        
        with col2:
            if st.button("👥 Clients", key="export_clients_sidebar", use_container_width=True):
                self._handle_export_clients()
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("📊 Assessments", key="export_assessments_sidebar", use_container_width=True):
                self._handle_export_assessments()
        
        with col4:
            if st.button("💾 Storage Info", key="storage_info_sidebar", use_container_width=True):
                self._handle_storage_info()
    
    def _handle_export_all(self):
        """Handle export all data functionality."""
        clients = st.session_state.get("clients", [])
        assessments = st.session_state.get("assessments", {})
        evidence_files = st.session_state.get("evidence_files", {})
        
        if clients or assessments:
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
            
            export_json = json.dumps(export_data, indent=2, default=str)
            st.download_button(
                "Download Complete Export",
                data=export_json,
                file_name=f"cyber_tonic_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key="download_all_export"
            )
        else:
            st.warning("No data to export")
    
    def _handle_export_clients(self):
        """Handle export clients functionality."""
        clients = st.session_state.get("clients", [])
        if clients:
            clients_json = json.dumps({"clients": clients}, indent=2)
            st.download_button(
                "Download Clients JSON",
                data=clients_json,
                file_name="clients_export.json",
                mime="application/json",
                key="download_clients_export"
            )
        else:
            st.warning("No clients to export")
    
    def _handle_export_assessments(self):
        """Handle export assessments functionality."""
        assessments = st.session_state.get("assessments", {})
        if assessments:
            assessments_json = json.dumps(assessments, indent=2)
            st.download_button(
                "Download Assessments JSON",
                data=assessments_json,
                file_name="assessments_export.json",
                mime="application/json",
                key="download_assessments_export"
            )
        else:
            st.warning("No assessments to export")
    
    def _handle_storage_info(self):
        """Handle storage info display."""
        from data_persistence import data_persistence
        storage_info = data_persistence.get_storage_info()
        st.json(storage_info)
    
    def _render_collapse_toggle(self):
        """Render the collapse/expand toggle at the bottom."""
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("📱 Mobile", key="mobile_view", use_container_width=True):
                st.info("Mobile view - sidebar will collapse on small screens")
        
        with col2:
            collapse_text = "⬆️ Collapse" if not st.session_state.sidebar_collapsed else "⬇️ Expand"
            if st.button(collapse_text, key="sidebar_toggle", use_container_width=True):
                st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed
                st.rerun()
    
    def _inject_custom_css(self):
        """Inject custom CSS for enhanced sidebar styling."""
        css = """
        <style>
        /* Sidebar Header */
        .sidebar-header {
            text-align: center;
            padding: 1rem 0;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 1rem;
        }
        
        .app-title {
            margin: 0;
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary-color);
        }
        
        .app-link {
            text-decoration: none;
            color: inherit;
            transition: color 0.2s ease;
        }
        
        .app-link:hover {
            color: var(--primary-hover);
        }
        
        /* Client Info Card */
        .client-info-card {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .client-info-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.25rem 0;
            border-bottom: 1px solid var(--border-color);
        }
        
        .client-info-row:last-child {
            border-bottom: none;
        }
        
        .client-info-label {
            font-weight: 600;
            color: var(--text-secondary);
            font-size: 0.875rem;
        }
        
        .client-info-value {
            color: var(--text-primary);
            font-size: 0.875rem;
        }
        
        /* Last Saved Indicator */
        .last-saved-indicator {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem;
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            margin: 0.5rem 0;
            font-size: 0.8rem;
        }
        
        .saved-icon {
            font-size: 1rem;
        }
        
        .saved-text {
            color: var(--text-secondary);
        }
        
        /* Navigation Items */
        .nav-item {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 1rem;
            margin: 0.25rem 0;
            border-radius: var(--radius-md);
            transition: all 0.2s ease;
            cursor: pointer;
        }
        
        .nav-item:hover {
            background-color: var(--bg-tertiary);
        }
        
        .nav-item-active {
            background-color: var(--primary-color);
            color: white;
            box-shadow: var(--shadow-sm);
        }
        
        .nav-icon {
            font-size: 1.1rem;
        }
        
        .nav-label {
            flex: 1;
            font-weight: 500;
            font-size: 0.9rem;
        }
        
        .nav-label-active {
            font-weight: 600;
        }
        
        .nav-indicator {
            font-size: 0.8rem;
            opacity: 0.8;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .sidebar-header {
                padding: 0.5rem 0;
            }
            
            .app-title {
                font-size: 1.25rem;
            }
            
            .client-info-card {
                padding: 0.75rem;
            }
            
            .nav-item {
                padding: 0.5rem 0.75rem;
            }
            
            .nav-label {
                font-size: 0.8rem;
            }
        }
        
        /* Animation for smooth transitions */
        .nav-item,
        .client-info-card,
        .last-saved-indicator {
            transition: all 0.2s ease;
        }
        
        /* Focus indicators for accessibility */
        .nav-item:focus {
            outline: 2px solid var(--primary-color);
            outline-offset: 2px;
        }
        
        /* High contrast mode support */
        @media (prefers-contrast: high) {
            .nav-item-active {
                background-color: #000000;
                color: #ffffff;
            }
            
            .client-info-card {
                border: 2px solid #000000;
            }
        }
        
        /* Reduced motion support */
        @media (prefers-reduced-motion: reduce) {
            .nav-item,
            .client-info-card,
            .last-saved-indicator {
                transition: none;
            }
        }
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)


# Global instance for easy access
cyber_tonic_sidebar = CyberTonicSidebar()

def render_enhanced_sidebar(current_page: str = "Assessment Dashboard"):
    """
    Convenience function to render the enhanced sidebar.
    
    Args:
        current_page: The currently active page
    """
    cyber_tonic_sidebar.render(current_page)
